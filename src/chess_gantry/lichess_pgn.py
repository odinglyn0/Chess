from __future__ import annotations

from io import StringIO
from typing import Iterator
from urllib.request import Request, urlopen

from .errors import ConfigurationError, ValidationError
from .models import BoardState, GridPosition, MoveDelta


def fetch_pgn(game_id: str) -> str:
    request = Request(
        f"https://lichess.org/game/export/{game_id}",
        headers={"Accept": "application/x-chess-pgn", "User-Agent": "chess-gantry/0.2"},
    )
    try:
        with urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8")
    except OSError as exc:
        raise ConfigurationError(f"could not fetch Lichess game {game_id!r}: {exc}") from exc


def pgn_moves(game_id: str, pgn_text: str, state: BoardState) -> Iterator[MoveDelta]:
    try:
        import chess
        import chess.pgn
    except ImportError as exc:  # pragma: no cover - installation error path.
        raise ConfigurationError("python-chess is not installed; run 'python -m pip install -e .'") from exc
    game = chess.pgn.read_game(StringIO(pgn_text))
    if game is None:
        raise ValidationError("Lichess export did not contain a readable PGN game")
    board = game.board()
    simulated = state
    for ply, move in enumerate(game.mainline_moves(), start=1):
        if board.is_castling(move):
            raise ValidationError(f"Lichess ply {ply} is castling, which needs a two-transfer workflow")
        if move.promotion is not None:
            raise ValidationError(f"Lichess ply {ply} is a promotion, which needs physical replacement")
        source = GridPosition(chess.square_file(move.from_square), chess.square_rank(move.from_square))
        destination = GridPosition(chess.square_file(move.to_square), chess.square_rank(move.to_square))
        moving = simulated.piece_at(source)
        if moving is None:
            raise ValidationError(f"local board has no piece at source for Lichess ply {ply}")
        payload = {
            "event_id": f"{game_id}.{ply}",
            "position": moving.piece_id,
            "px": source.x,
            "py": source.y,
            "nx": destination.x,
            "ny": destination.y,
        }
        if board.is_capture(move):
            capture_square = (
                chess.square(chess.square_file(move.to_square), chess.square_rank(move.from_square))
                if board.is_en_passant(move) else move.to_square
            )
            capture_position = GridPosition(chess.square_file(capture_square), chess.square_rank(capture_square))
            captured = simulated.piece_at(capture_position)
            if captured is None:
                raise ValidationError(f"local board has no capture target for Lichess ply {ply}")
            payload["capture"] = {"id": captured.piece_id, "x": capture_position.x, "y": capture_position.y}
        result = MoveDelta.from_mapping(payload)
        # Keep a parallel physical state so subsequent PGN plies resolve piece IDs correctly.
        capture_slot = None
        if result.capture is not None:
            used_slots = set(simulated.used_capture_slots())
            capture_slot = next(slot for slot in range(32) if slot not in used_slots)
        simulated = simulated.applied(result, capture_slot)
        board.push(move)
        yield result
