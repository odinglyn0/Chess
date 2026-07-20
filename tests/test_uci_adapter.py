from __future__ import annotations

import unittest

from chess_gantry.errors import ValidationError
from chess_gantry.models import BoardState, GridPosition
from chess_gantry.uci_adapter import uci_to_move


def state_with(*pieces):
    return BoardState.from_mapping(
        {
            "schema_version": 1,
            "revision": 0,
            "pieces": {piece_id: value for piece_id, value in pieces},
            "processed_events": [],
        }
    )


class UciAdapterTests(unittest.TestCase):
    def test_converts_normal_move(self) -> None:
        state = state_with(
            ("white_pawn_e", {"status": "board", "x": 4, "y": 1, "metadata": {"kind": "pawn"}})
        )
        move = uci_to_move("e2e4", state, event_id="game-1-ply-1")
        self.assertEqual(move.piece_id, "white_pawn_e")
        self.assertEqual(move.previous, GridPosition(4, 1))
        self.assertEqual(move.new, GridPosition(4, 3))
        self.assertEqual(move.event_id, "game-1-ply-1")

    def test_adds_destination_capture(self) -> None:
        state = state_with(
            ("white_pawn_e", {"status": "board", "x": 4, "y": 3, "metadata": {"kind": "pawn"}}),
            ("black_pawn_d", {"status": "board", "x": 3, "y": 4, "metadata": {"kind": "pawn"}}),
        )
        move = uci_to_move("e4d5", state)
        self.assertIsNotNone(move.capture)
        assert move.capture is not None
        self.assertEqual(move.capture.piece_id, "black_pawn_d")
        self.assertEqual(move.capture.position, GridPosition(3, 4))

    def test_adds_explicit_en_passant_capture(self) -> None:
        state = state_with(
            ("white_pawn_e", {"status": "board", "x": 4, "y": 4, "metadata": {"kind": "pawn"}}),
            ("black_pawn_d", {"status": "board", "x": 3, "y": 4, "metadata": {"kind": "pawn"}}),
        )
        move = uci_to_move("e5d6", state, en_passant=True)
        assert move.capture is not None
        self.assertEqual(move.capture.position, GridPosition(3, 4))

    def test_rejects_promotion_and_castling(self) -> None:
        pawn_state = state_with(
            ("white_pawn_e", {"status": "board", "x": 4, "y": 6, "metadata": {"kind": "pawn"}})
        )
        with self.assertRaisesRegex(ValidationError, "promotions"):
            uci_to_move("e7e8q", pawn_state)
        king_state = state_with(
            ("white_king_e", {"status": "board", "x": 4, "y": 0, "metadata": {"kind": "king"}})
        )
        with self.assertRaisesRegex(ValidationError, "castling"):
            uci_to_move("e1g1", king_state)


if __name__ == "__main__":
    unittest.main()
