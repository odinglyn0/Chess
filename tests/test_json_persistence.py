from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from chess_gantry.models import BoardState, GridPosition, MoveDelta
from chess_gantry.persistence import BoardStore


class JsonPersistenceTests(unittest.TestCase):
    def test_game_state_survives_restart_in_local_json(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "games" / "6RkOwfp1" / "board_state.json"
            first = BoardStore(path)
            initial = BoardState.standard()
            first.initialize(initial)
            move = MoveDelta.from_mapping(
                {
                    "event_id": "6RkOwfp1.1",
                    "position": "white_pawn_e",
                    "px": 4,
                    "py": 1,
                    "nx": 4,
                    "ny": 3,
                }
            )
            first.save(initial.applied(move, None))

            restarted = BoardStore(path)
            loaded = restarted.load()
            self.assertEqual(loaded.revision, 1)
            self.assertEqual(
                loaded.pieces["white_pawn_e"].board_position, GridPosition(4, 3)
            )
            self.assertEqual(loaded.processed_events, ("6RkOwfp1.1",))


if __name__ == "__main__":
    unittest.main()
