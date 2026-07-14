"""Track stable piece identities across a chess game and emit schema-compliant state.

Coordinate convention matches the board-state schema and ``examples/matrix_adapter.py``:
``x`` is the file (0 = a) and ``y`` is the rank (0 = rank 1).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import chess

SCHEMA_VERSION = 1


class TrackerError(RuntimeError):
    """Raised when a move cannot be reconciled with the tracked position."""


def _color_name(color: chess.Color) -> str:
    return "white" if color == chess.WHITE else "black"


def _square_xy(square: chess.Square) -> Dict[str, int]:
    return {"x": chess.square_file(square), "y": chess.square_rank(square)}


@dataclass
class _Piece:
    piece_id: str
    color: str
    kind: str
    square: Optional[chess.Square]
    capture_slot: Optional[int] = None

    def to_state(self) -> Dict[str, Any]:
        metadata = {"color": self.color, "kind": self.kind}
        if self.square is not None:
            return {
                "status": "board",
                "x": chess.square_file(self.square),
                "y": chess.square_rank(self.square),
                "metadata": metadata,
            }
        return {
            "status": "captured",
            "x": None,
            "y": None,
            "capture_slot": self.capture_slot,
            "metadata": metadata,
        }


@dataclass
class BoardTracker:
    """Maintain per-piece identity and produce board-state snapshots and move events."""

    game_id: str
    max_processed_events: int = 1024
    board: chess.Board = field(init=False)
    revision: int = field(init=False, default=0)
    _pieces: Dict[str, _Piece] = field(init=False, default_factory=dict)
    _by_square: Dict[chess.Square, str] = field(init=False, default_factory=dict)
    _capture_counter: int = field(init=False, default=0)
    _processed: List[str] = field(init=False, default_factory=list)
    _processed_set: set[str] = field(init=False, default_factory=set)

    def __post_init__(self) -> None:
        self.board = chess.Board()
        self._rebuild_identities()

    def reset_from_fen(self, fen: str) -> None:
        self.board = chess.Board(fen)
        self.revision += 1
        self._capture_counter = 0
        self._rebuild_identities()

    def _rebuild_identities(self) -> None:
        self._pieces = {}
        self._by_square = {}
        used: set[str] = set()
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece is None:
                continue
            color = _color_name(piece.color)
            kind = chess.piece_name(piece.piece_type)
            base = f"{color}_{kind}_{chess.square_name(square)}"
            piece_id = base
            suffix = 1
            while piece_id in used:
                suffix += 1
                piece_id = f"{base}_{suffix}"
            used.add(piece_id)
            self._pieces[piece_id] = _Piece(
                piece_id=piece_id, color=color, kind=kind, square=square
            )
            self._by_square[square] = piece_id

    def event_id_for_next_move(self) -> str:
        return f"{self.game_id}.{len(self.board.move_stack) + 1}"

    def infer_uci_from_fen(self, target_fen: str) -> Optional[str]:
        target_placement = target_fen.split(" ", 1)[0]
        if self.board.board_fen() == target_placement:
            return None
        for move in self.board.legal_moves:
            self.board.push(move)
            matches = self.board.board_fen() == target_placement
            self.board.pop()
            if matches:
                return move.uci()
        return None

    def apply_uci(self, uci: str, event_id: Optional[str] = None) -> Dict[str, Any]:
        """Apply a UCI move, updating identities and returning a move event.

        Raises :class:`TrackerError` if the move is not legal in the tracked position.
        """

        try:
            move = chess.Move.from_uci(uci)
        except ValueError as exc:
            raise TrackerError(f"invalid UCI move {uci!r}: {exc}") from exc
        if move not in self.board.legal_moves:
            raise TrackerError(f"move {uci!r} is not legal in the current position")

        resolved_event = event_id or self.event_id_for_next_move()

        mover = self.board.piece_at(move.from_square)
        if mover is None:
            raise TrackerError(f"no piece on source square for move {uci!r}")
        color = _color_name(mover.color)

        moving_id = self._by_square[move.from_square]
        san = self.board.san(move)

        captured_id: Optional[str] = None
        captured_square: Optional[chess.Square] = None
        if self.board.is_capture(move):
            if self.board.is_en_passant(move):
                captured_square = chess.square(
                    chess.square_file(move.to_square),
                    chess.square_rank(move.from_square),
                )
            else:
                captured_square = move.to_square
            captured_id = self._by_square.get(captured_square)
            if captured_id is None:
                raise TrackerError(f"capture target square is empty for move {uci!r}")

        castle: Optional[Dict[str, Any]] = None
        rook_id: Optional[str] = None
        rook_from: Optional[chess.Square] = None
        rook_to: Optional[chess.Square] = None
        if self.board.is_castling(move):
            rank = chess.square_rank(move.from_square)
            if self.board.is_kingside_castling(move):
                rook_from = chess.square(7, rank)
                rook_to = chess.square(5, rank)
            else:
                rook_from = chess.square(0, rank)
                rook_to = chess.square(3, rank)
            rook_id = self._by_square.get(rook_from)
            if rook_id is None:
                raise TrackerError(f"castling rook missing for move {uci!r}")

        self.board.push(move)

        if captured_id is not None and captured_square is not None:
            captured = self._pieces[captured_id]
            self._by_square.pop(captured_square, None)
            captured.square = None
            captured.capture_slot = self._capture_counter
            self._capture_counter += 1

        moving = self._pieces[moving_id]
        self._by_square.pop(move.from_square, None)
        if self._by_square.get(move.to_square) not in (None, moving_id):
            self._by_square.pop(move.to_square, None)
        moving.square = move.to_square
        self._by_square[move.to_square] = moving_id

        promotion_kind: Optional[str] = None
        if move.promotion is not None:
            promotion_kind = chess.piece_name(move.promotion)
            moving.kind = promotion_kind

        if rook_id is not None and rook_from is not None and rook_to is not None:
            rook = self._pieces[rook_id]
            self._by_square.pop(rook_from, None)
            rook.square = rook_to
            self._by_square[rook_to] = rook_id
            castle = {
                "rook": rook_id,
                "from": _square_xy(rook_from),
                "to": _square_xy(rook_to),
            }

        self.revision += 1
        self._remember_event(resolved_event)

        event: Dict[str, Any] = {
            "type": "move",
            "event_id": resolved_event,
            "ply": len(self.board.move_stack),
            "move_number": (len(self.board.move_stack) + 1) // 2,
            "color": color,
            "san": san,
            "uci": uci,
            "piece": moving_id,
            "from": _square_xy(move.from_square),
            "to": _square_xy(move.to_square),
            "capture": None,
            "castle": castle,
            "promotion": promotion_kind,
            "check": self.board.is_check(),
            "checkmate": self.board.is_checkmate(),
            "stalemate": self.board.is_stalemate(),
            "fen": self.board.fen(),
        }
        if captured_id is not None and captured_square is not None:
            event["capture"] = {
                "piece": captured_id,
                "kind": self._pieces[captured_id].kind,
                **_square_xy(captured_square),
                "capture_slot": self._pieces[captured_id].capture_slot,
            }
        return event

    def _remember_event(self, event_id: str) -> None:
        if event_id in self._processed_set:
            return
        self._processed.append(event_id)
        self._processed_set.add(event_id)
        while len(self._processed) > self.max_processed_events:
            dropped = self._processed.pop(0)
            self._processed_set.discard(dropped)

    def has_processed(self, event_id: str) -> bool:
        return event_id in self._processed_set

    def snapshot(self) -> Dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "revision": self.revision,
            "pieces": {
                piece_id: self._pieces[piece_id].to_state()
                for piece_id in sorted(self._pieces)
            },
            "processed_events": list(self._processed),
        }
