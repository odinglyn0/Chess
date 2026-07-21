from __future__ import annotations

from typing import Any, Dict, Optional
import re

from .errors import ValidationError
from .models import BoardState, GridPosition, MoveDelta, PieceState


_UCI_RE = re.compile(r"^[a-h][1-8][a-h][1-8][qrbn]?$", re.IGNORECASE)


def _square_to_grid(square: str) -> tuple[int, int]:
    return ord(square[0]) - ord("a"), ord(square[1]) - ord("1")


def _piece_kind(piece: PieceState) -> Optional[str]:
    value = piece.metadata.get("kind")
    return value if isinstance(value, str) else None


def uci_to_move(
    uci: str,
    state: BoardState,
    *,
    event_id: Optional[str] = None,
    en_passant: bool = False,
    width: int = 8,
    height: int = 8,
) -> MoveDelta:
    normalized = uci.strip().lower()
    if not _UCI_RE.fullmatch(normalized):
        raise ValidationError("UCI move must look like e2e4 or e7e8q")
    if len(normalized) == 5:
        raise ValidationError(
            "promotions need a physical piece-replacement workflow and are not supported"
        )

    source_x, source_y = _square_to_grid(normalized[:2])
    destination_x, destination_y = _square_to_grid(normalized[2:4])
    source = GridPosition(source_x, source_y)
    destination = GridPosition(destination_x, destination_y)
    moving = state.piece_at(source)
    if moving is None:
        raise ValidationError(f"no tracked piece is present at {normalized[:2]}")
    if _piece_kind(moving) == "king" and abs(destination.x - source.x) == 2:
        raise ValidationError(
            "castling needs two physical transfers; submit the king and rook moves separately"
        )

    captured = state.piece_at(destination)
    raw: Dict[str, Any] = {
        "position": moving.piece_id,
        "px": source.x,
        "py": source.y,
        "nx": destination.x,
        "ny": destination.y,
    }
    if event_id is not None:
        raw["event_id"] = event_id

    if captured is not None:
        raw["capture"] = {
            "id": captured.piece_id,
            "x": destination.x,
            "y": destination.y,
        }
    elif en_passant:
        if _piece_kind(moving) != "pawn" or source.x == destination.x:
            raise ValidationError("--en-passant requires a diagonal pawn move")
        capture_position = GridPosition(destination.x, source.y)
        victim = state.piece_at(capture_position)
        if victim is None or _piece_kind(victim) != "pawn":
            raise ValidationError("no pawn is present at the requested en-passant capture square")
        raw["capture"] = {"id": victim.piece_id, "x": capture_position.x, "y": capture_position.y}

    return MoveDelta.from_mapping(raw, width, height)
