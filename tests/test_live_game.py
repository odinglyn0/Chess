from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import time
import unittest

from chess_gantry.config import AppConfig
from chess_gantry.kinematics import grid_to_machine
from chess_gantry.live_game import LiveGameManager
from chess_gantry.models import GridPosition


EMPTY_PGN = '[Event "TV"]\n[Result "*"]\n\n*\n'
E4_PGN = '[Event "TV"]\n[Result "*"]\n\n1. e4 *\n'
CAPTURE_PGN = '[Event "TV"]\n[Result "*"]\n\n1. e4 d5 2. exd5 *\n'


class FakeGames:
    def __init__(self, events):
        self.events = events

    def stream_game_moves(self, game_id):
        yield from self.events


class FakeClient:
    def __init__(self, events):
        self.games = FakeGames(events)


class SequencedPgn:
    def __init__(self, values):
        self.values = list(values)

    def __call__(self, game_id, **kwargs):
        if len(self.values) > 1:
            return self.values.pop(0)
        return self.values[0]


class LiveGameTests(unittest.TestCase):
    def wait(self, manager: LiveGameManager):
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            value = manager.status()
            if value["status"]["state"] not in {
                "starting",
                "homing",
                "following",
                "executing",
            }:
                return value
            time.sleep(0.02)
        self.fail("live game did not finish")

    def test_h1_is_the_measured_nearest_home_center(self) -> None:
        config = AppConfig.load("config.json")
        point = grid_to_machine(GridPosition(7, 0), config.board)
        raw = (config.workspace.max_y_mm - point.y, point.y, point.x)
        self.assertEqual(raw, (2.0, 298.0, 320.0))

    def test_new_stream_move_executes_immediately_in_fresh_demo_state(self) -> None:
        with TemporaryDirectory() as directory:
            config = AppConfig.load("config.demo.json")
            fetcher = SequencedPgn((EMPTY_PGN, E4_PGN))
            manager = LiveGameManager(
                Path(directory),
                config,
                demo=True,
                client_factory=lambda token: FakeClient(({"moves": "e2e4"},)),
                pgn_fetcher=fetcher,
            )
            manager.start(
                "game1234",
                confirm_standard_position=True,
                confirm_motion=False,
            )
            result = self.wait(manager)
            self.assertEqual(result["status"]["state"], "finished")
            self.assertEqual(result["status"]["executed_count"], 1)
            self.assertEqual(result["status"]["last_event_id"], "game1234.1")
            self.assertIn("Executing game1234.1", result["logs"])

    def test_rejects_game_that_already_has_moves(self) -> None:
        with TemporaryDirectory() as directory:
            manager = LiveGameManager(
                Path(directory),
                AppConfig.load("config.demo.json"),
                demo=True,
                client_factory=lambda token: FakeClient(()),
                pgn_fetcher=SequencedPgn((E4_PGN,)),
            )
            manager.start(
                "game1234",
                confirm_standard_position=True,
                confirm_motion=False,
            )
            result = self.wait(manager)
            self.assertEqual(result["status"]["state"], "failed")
            self.assertIn("already has moves", result["status"]["error"])

    def test_each_start_uses_fresh_standard_state(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            manager = LiveGameManager(
                root,
                AppConfig.load("config.demo.json"),
                demo=True,
                client_factory=lambda token: FakeClient(({"moves": "e2e4"},)),
                pgn_fetcher=SequencedPgn((EMPTY_PGN, E4_PGN, EMPTY_PGN, E4_PGN)),
            )
            for _ in range(2):
                manager.start(
                    "game1234",
                    confirm_standard_position=True,
                    confirm_motion=False,
                )
                result = self.wait(manager)
                self.assertEqual(result["status"]["executed_count"], 1)
            runs = sorted((root / "data" / "web-live").glob("run-*-game1234"))
            self.assertEqual(len(runs), 2)
            self.assertNotEqual(runs[0], runs[1])

    def test_capture_stops_when_physical_capture_slots_are_disabled(self) -> None:
        with TemporaryDirectory() as directory:
            manager = LiveGameManager(
                Path(directory),
                AppConfig.load("config.demo.json"),
                demo=True,
                client_factory=lambda token: FakeClient(({"moves": "e2e4d7d5e4d5"},)),
                pgn_fetcher=SequencedPgn((EMPTY_PGN, CAPTURE_PGN)),
            )
            manager.start(
                "game1234",
                confirm_standard_position=True,
                confirm_motion=False,
            )
            result = self.wait(manager)
            self.assertEqual(result["status"]["state"], "failed")
            self.assertEqual(result["status"]["executed_count"], 2)
            self.assertIn("capture slots are disabled", result["status"]["error"])

    def test_validates_game_id_and_confirmations(self) -> None:
        manager = LiveGameManager(
            Path("/tmp"), AppConfig.load("config.demo.json"), demo=True
        )
        with self.assertRaisesRegex(Exception, "8-12"):
            manager.start("bad!", confirm_standard_position=True, confirm_motion=False)
        with self.assertRaisesRegex(Exception, "standard"):
            manager.start(
                "game1234", confirm_standard_position=False, confirm_motion=False
            )


if __name__ == "__main__":
    unittest.main()
