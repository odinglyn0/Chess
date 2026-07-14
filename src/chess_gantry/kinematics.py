"""Conversion between logical chess-board coordinates and machine millimetres."""

from __future__ import annotations

from typing import Iterable, Tuple

from .config import BoardGeometry, Workspace
from .errors import ConfigurationError, PlanningError
from .models import GridPosition, MachinePoint


def grid_to_machine(position: GridPosition, geometry: BoardGeometry) -> MachinePoint:
    """Convert a zero-based square coordinate to the square centre in machine space.

    ``origin_x_mm``/``origin_y_mm`` describe the centre of physical index (0, 0).
    Flips are applied before an optional axis swap, allowing any board orientation.
    """

    if not 0 <= position.x < geometry.width or not 0 <= position.y < geometry.height:
        raise PlanningError(f"grid position ({position.x}, {position.y}) is outside configured board")

    ix = geometry.width - 1 - position.x if geometry.flip_x else position.x
    iy = geometry.height - 1 - position.y if geometry.flip_y else position.y
    if geometry.swap_xy:
        ix, iy = iy, ix

    return MachinePoint(
        x=geometry.origin_x_mm + ix * geometry.square_size_mm,
        y=geometry.origin_y_mm + iy * geometry.square_size_mm,
    )


def validate_board_inside_workspace(geometry: BoardGeometry, workspace: Workspace) -> None:
    """Reject a configuration whose square centres exceed the motion envelope."""

    points = (
        grid_to_machine(GridPosition(0, 0), geometry),
        grid_to_machine(GridPosition(geometry.width - 1, 0), geometry),
        grid_to_machine(GridPosition(0, geometry.height - 1), geometry),
        grid_to_machine(GridPosition(geometry.width - 1, geometry.height - 1), geometry),
    )
    outside = [point for point in points if not workspace.contains(point)]
    if outside:
        formatted = ", ".join(f"({p.x:.3f}, {p.y:.3f})" for p in outside)
        raise ConfigurationError(f"one or more board corner square centres are outside the workspace: {formatted}")


def board_piece_points(positions: Iterable[GridPosition], geometry: BoardGeometry) -> Tuple[MachinePoint, ...]:
    return tuple(grid_to_machine(position, geometry) for position in positions)
