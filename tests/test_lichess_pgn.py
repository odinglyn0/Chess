from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from chess_gantry.lichess_follow import FollowSession, _game_is_finished
from chess_gantry.lichess_pgn import pgn_moves
from chess_gantry.models import BoardState, GridPosition


class LichessPgnTests(unittest.TestCase):
    def standard_state(self) -> BoardState:
        pieces = {
            "white_pawn_e": {"status": "board", "x": 4, "y": 1},
            "white_pawn_d": {"status": "board", "x": 3, "y": 1},
            "black_pawn_d": {"status": "board", "x": 3, "y": 6},
        }
        return BoardState.from_mapping(
            {
                "schema_version": 1,
                "revision": 0,
                "pieces": pieces,
                "processed_events": [],
            }
        )

    def test_replays_pgn_to_stable_gantry_moves(self) -> None:
        moves = list(pgn_moves("game123", "1. e4 d5 2. exd5 *", self.standard_state()))
        self.assertEqual(
            [move.event_id for move in moves], ["game123.1", "game123.2", "game123.3"]
        )
        self.assertEqual(moves[0].piece_id, "white_pawn_e")
        self.assertEqual(moves[1].piece_id, "black_pawn_d")
        self.assertEqual(moves[2].previous, GridPosition(4, 3))
        assert moves[2].capture is not None
        self.assertEqual(moves[2].capture.piece_id, "black_pawn_d")

    def test_follow_session_persists_emitted_events(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "game.session.json"
            session = FollowSession(
                "game123", self.standard_state(), frozenset({"game123.1"})
            )
            session.save(path)
            loaded = FollowSession.load_or_create(
                path, "game123", self.standard_state(), reset=False
            )
            self.assertEqual(loaded.emitted_event_ids, frozenset({"game123.1"}))

    def test_finished_pgn_detection(self) -> None:
        self.assertTrue(_game_is_finished('[Result "1-0"]\n\n1. e4 1-0'))
        self.assertFalse(_game_is_finished('[Result "*"]\n\n1. e4 *'))


if __name__ == "__main__":
    unittest.main()
