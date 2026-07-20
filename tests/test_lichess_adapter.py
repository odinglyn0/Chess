from __future__ import annotations

import unittest

from chess_gantry.errors import ValidationError
from chess_gantry.lichess_adapter import stream_event_to_move
from chess_gantry.models import BoardState, GridPosition


def event(**overrides):
    move = {
        "event_id": "game-1.1", "piece": "white_pawn_e",
        "from": {"x": 4, "y": 1}, "to": {"x": 4, "y": 3},
        "capture": None, "castle": None, "promotion": None,
    }
    move.update(overrides)
    return {"type": "move", "move": move}


class LichessAdapterTests(unittest.TestCase):
    def test_converts_stream_event(self) -> None:
        move = stream_event_to_move(event())
        self.assertEqual(move.piece_id, "white_pawn_e")
        self.assertEqual(move.event_id, "game-1.1")
        self.assertEqual(move.previous, GridPosition(4, 1))
        self.assertEqual(move.new, GridPosition(4, 3))

    def test_resolves_upstream_ids_against_local_physical_state(self) -> None:
        state = BoardState.from_mapping({
            "schema_version": 1, "revision": 0, "processed_events": [],
            "pieces": {"white_pawn_e": {"status": "board", "x": 4, "y": 1}},
        })
        move = stream_event_to_move(event(piece="white_pawn_e2"), state=state)
        self.assertEqual(move.piece_id, "white_pawn_e")

    def test_converts_en_passant_capture(self) -> None:
        move = stream_event_to_move(event(capture={"piece": "black_pawn_d", "x": 3, "y": 4}))
        assert move.capture is not None
        self.assertEqual(move.capture.piece_id, "black_pawn_d")
        self.assertEqual(move.capture.position, GridPosition(3, 4))

    def test_rejects_special_moves_needing_physical_workflow(self) -> None:
        with self.assertRaisesRegex(ValidationError, "castling"):
            stream_event_to_move(event(castle={"rook": "white_rook_h"}))
        with self.assertRaisesRegex(ValidationError, "promotion"):
            stream_event_to_move(event(promotion="queen"))


if __name__ == "__main__":
    unittest.main()
