from __future__ import annotations

import unittest

from chess_gantry.config import BoardGeometry, PlannerSettings, Workspace
from chess_gantry.errors import PlanningError
from chess_gantry.kinematics import grid_to_machine
from chess_gantry.models import GridPosition, MachinePoint
from chess_gantry.path_planning import astar_path, segment_is_clear


class KinematicsTests(unittest.TestCase):
    def test_flip_and_swap(self) -> None:
        geometry = BoardGeometry(
            width=8,
            height=8,
            square_size_mm=20.0,
            origin_x_mm=10.0,
            origin_y_mm=10.0,
            flip_x=True,
            flip_y=False,
            swap_xy=True,
        )
        # logical (1, 2) -> flipped indices (6, 2) -> swapped (2, 6)
        self.assertEqual(grid_to_machine(GridPosition(1, 2), geometry), MachinePoint(50.0, 130.0))


class AStarTests(unittest.TestCase):
    def settings(self, keepout: float = 15.0) -> PlannerSettings:
        return PlannerSettings(
            kind="astar",
            grid_step_mm=10.0,
            obstacle_keepout_mm=keepout,
            allow_diagonal=True,
            simplify_path=True,
            max_expanded_nodes=10000,
        )

    def test_routes_around_obstacle(self) -> None:
        workspace = Workspace(0.0, 100.0, 0.0, 100.0)
        obstacle = MachinePoint(50.0, 50.0)
        path = astar_path(
            MachinePoint(10.0, 50.0),
            MachinePoint(90.0, 50.0),
            [obstacle],
            workspace,
            self.settings(),
        )
        self.assertEqual(path[0], MachinePoint(10.0, 50.0))
        self.assertEqual(path[-1], MachinePoint(90.0, 50.0))
        self.assertGreater(len(path), 2)
        for start, end in zip(path, path[1:]):
            self.assertTrue(segment_is_clear(start, end, [obstacle], 15.0))

    def test_reports_no_path_when_keepout_blocks_workspace(self) -> None:
        workspace = Workspace(0.0, 100.0, 0.0, 20.0)
        with self.assertRaisesRegex(PlanningError, "no collision-free path"):
            astar_path(
                MachinePoint(0.0, 10.0),
                MachinePoint(100.0, 10.0),
                [MachinePoint(50.0, 10.0)],
                workspace,
                self.settings(keepout=30.0),
            )


if __name__ == "__main__":
    unittest.main()
