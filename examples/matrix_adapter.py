from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

Cell = Optional[str]
Matrix = Sequence[Sequence[Cell]]


def _positions(matrix: Matrix) -> Dict[str, Tuple[int, int]]:
    if len(matrix) != 8 or any(len(row) != 8 for row in matrix):
        raise ValueError("matrix must be exactly 8 rows of 8 cells")
    result: Dict[str, Tuple[int, int]] = {}
    for y, row in enumerate(matrix):
        for x, piece_id in enumerate(row):
            if piece_id is None:
                continue
            if not isinstance(piece_id, str) or not piece_id:
                raise ValueError(f"matrix[{y}][{x}] must be a piece id string or None")
            if piece_id in result:
                raise ValueError(f"piece id {piece_id!r} appears more than once")
            result[piece_id] = (x, y)
    return result


def diff_matrices(old: Matrix, new: Matrix, event_prefix: str = "matrix") -> List[dict]:

    old_positions = _positions(old)
    new_positions = _positions(new)
    unexpected = set(new_positions) - set(old_positions)
    if unexpected:
        raise ValueError(
            "new matrix introduced unknown piece id(s): "
            + ", ".join(sorted(unexpected))
        )

    surviving = set(old_positions) & set(new_positions)
    changed = [
        piece_id
        for piece_id in sorted(surviving)
        if old_positions[piece_id] != new_positions[piece_id]
    ]
    removed = sorted(set(old_positions) - set(new_positions))
    if not changed:
        if removed:
            raise ValueError(
                "piece(s) disappeared without a moving piece: " + ", ".join(removed)
            )
        return []
    if len(removed) > 1:
        raise ValueError("more than one captured/disappearing piece was detected")
    if len(changed) > 1 and removed:
        raise ValueError(
            "a multi-piece move plus capture is ambiguous; send explicit deltas"
        )

    deltas = []
    for index, piece_id in enumerate(changed, start=1):
        px, py = old_positions[piece_id]
        nx, ny = new_positions[piece_id]
        delta = {
            "event_id": f"{event_prefix}-{index}",
            "position": piece_id,
            "px": px,
            "py": py,
            "nx": nx,
            "ny": ny,
        }
        if len(changed) == 1 and removed:
            captured_id = removed[0]
            cx, cy = old_positions[captured_id]
            delta["capture"] = {"id": captured_id, "x": cx, "y": cy}
        deltas.append(delta)
    return deltas
