from __future__ import annotations

from typing import Any, Mapping

from .errors import ValidationError
from .models import BoardState, GridPosition, MoveDelta


def stream_event_to_move(
    raw: Mapping[str, Any],
    width: int = 8,
    height: int = 8,
    state: BoardState | None = None,
) -> MoveDelta:
    if not isinstance(raw, Mapping):
        raise ValidationError("Lichess stream event must be a JSON object")
    if raw.get("type") != "move":
        raise ValidationError("Lichess stream event type must be 'move'")
    event = raw.get("move")
    if not isinstance(event, Mapping):
        raise ValidationError("Lichess stream move event is missing")
    if event.get("castle") is not None:
        raise ValidationError(
            "castling needs two physical transfers; submit king and rook moves separately"
        )
    if event.get("promotion") is not None:
        raise ValidationError(
            "promotion needs a physical piece-replacement workflow and is not supported"
        )
    source = event.get("from")
    destination = event.get("to")
    if not isinstance(source, Mapping) or not isinstance(destination, Mapping):
        raise ValidationError("Lichess stream move requires from and to coordinates")
    event_id = event.get("event_id")
    if not isinstance(event_id, str):
        raise ValidationError("Lichess stream move requires a string event_id field")
    if state is None:
        piece_id = event.get("piece")
        if not isinstance(piece_id, str):
            raise ValidationError("Lichess stream move requires a string piece field")
    else:
        piece = state.piece_at(
            GridPosition.validated(
                source.get("x"), source.get("y"), width, height, "from"
            )
        )
        if piece is None:
            raise ValidationError(
                "stored gantry board has no piece at the Lichess move source square"
            )
        piece_id = piece.piece_id
    payload: dict[str, Any] = {
        "event_id": event_id,
        "position": piece_id,
        "px": source.get("x"),
        "py": source.get("y"),
        "nx": destination.get("x"),
        "ny": destination.get("y"),
    }
    capture = event.get("capture")
    if capture is not None:
        if not isinstance(capture, Mapping):
            raise ValidationError("Lichess stream capture must be an object or null")
        if state is None:
            captured_id = capture.get("piece")
            if not isinstance(captured_id, str):
                raise ValidationError("Lichess stream capture requires a piece id")
        else:
            captured_piece = state.piece_at(
                GridPosition.validated(
                    capture.get("x"), capture.get("y"), width, height, "capture"
                )
            )
            if captured_piece is None:
                raise ValidationError(
                    "stored gantry board has no piece at the Lichess capture square"
                )
            captured_id = captured_piece.piece_id
        payload["capture"] = {
            "id": captured_id,
            "x": capture.get("x"),
            "y": capture.get("y"),
        }
    return MoveDelta.from_mapping(payload, width, height)
