from __future__ import annotations

import unittest

from chess_gantry.errors import StateError, ValidationError
from chess_gantry.models import BoardState, GridPosition, MoveDelta


class MoveDeltaTests(unittest.TestCase):
    def test_original_flat_format(self) -> None:
        move = MoveDelta.from_mapping(
            {"position": "white_pawn_e", "px": 4, "py": 1, "nx": 4, "ny": 3}
        )
        self.assertEqual(move.piece_id, "white_pawn_e")
        self.assertEqual(move.previous, GridPosition(4, 1))
        self.assertEqual(move.new, GridPosition(4, 3))

    def test_nested_format(self) -> None:
        move = MoveDelta.from_mapping(
            {
                "event_id": "game-1-ply-1",
                "position": {"id": "white_pawn_e", "px": 4, "py": 1, "nx": 4, "ny": 3},
            }
        )
        self.assertEqual(move.event_id, "game-1-ply-1")

    def test_id_alias(self) -> None:
        move = MoveDelta.from_mapping(
            {"id": "piece-1", "px": 0, "py": 0, "nx": 1, "ny": 1}
        )
        self.assertEqual(move.piece_id, "piece-1")

    def test_rejects_boolean_coordinate(self) -> None:
        with self.assertRaisesRegex(ValidationError, "must be an integer"):
            MoveDelta.from_mapping(
                {"position": "piece-1", "px": True, "py": 0, "nx": 1, "ny": 1}
            )

    def test_rejects_unknown_field(self) -> None:
        with self.assertRaisesRegex(ValidationError, "unknown move field"):
            MoveDelta.from_mapping(
                {"position": "piece-1", "px": 0, "py": 0, "nx": 1, "ny": 1, "nyy": 1}
            )

    def test_rejects_same_square(self) -> None:
        with self.assertRaisesRegex(ValidationError, "identical"):
            MoveDelta.from_mapping(
                {"position": "piece-1", "px": 0, "py": 0, "nx": 0, "ny": 0}
            )


class BoardStateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.state = BoardState.from_mapping(
            {
                "schema_version": 1,
                "revision": 2,
                "pieces": {
                    "white_pawn_e": {"status": "board", "x": 4, "y": 3},
                    "black_pawn_d": {"status": "board", "x": 3, "y": 4},
                },
                "processed_events": [],
            }
        )

    def test_apply_capture(self) -> None:
        move = MoveDelta.from_mapping(
            {
                "event_id": "capture-1",
                "position": "white_pawn_e",
                "px": 4,
                "py": 3,
                "nx": 3,
                "ny": 4,
            }
        )
        result = self.state.applied(move, capture_slot=0)
        self.assertEqual(result.revision, 3)
        self.assertEqual(
            result.pieces["white_pawn_e"].board_position, GridPosition(3, 4)
        )
        self.assertEqual(result.pieces["black_pawn_d"].status, "captured")
        self.assertEqual(result.pieces["black_pawn_d"].capture_slot, 0)
        self.assertIn("capture-1", result.processed_events)

    def test_source_mismatch_is_rejected(self) -> None:
        move = MoveDelta.from_mapping(
            {"position": "white_pawn_e", "px": 4, "py": 2, "nx": 4, "ny": 3}
        )
        with self.assertRaisesRegex(StateError, "stored at"):
            self.state.validate_move(move)

    def test_duplicate_occupancy_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValidationError, "both occupy"):
            BoardState.from_mapping(
                {
                    "schema_version": 1,
                    "revision": 0,
                    "pieces": {
                        "a": {"status": "board", "x": 0, "y": 0},
                        "b": {"status": "board", "x": 0, "y": 0},
                    },
                    "processed_events": [],
                }
            )

    def test_explicit_en_passant_capture(self) -> None:
        state = BoardState.from_mapping(
            {
                "schema_version": 1,
                "revision": 0,
                "pieces": {
                    "white_pawn_e": {"status": "board", "x": 4, "y": 4},
                    "black_pawn_d": {"status": "board", "x": 3, "y": 4},
                },
                "processed_events": [],
            }
        )
        move = MoveDelta.from_mapping(
            {
                "position": "white_pawn_e",
                "px": 4,
                "py": 4,
                "nx": 3,
                "ny": 5,
                "capture": {"id": "black_pawn_d", "x": 3, "y": 4},
            }
        )
        captured = state.validate_move(move)
        self.assertIsNotNone(captured)
        self.assertEqual(captured.piece_id, "black_pawn_d")
        result = state.applied(move, capture_slot=2)
        self.assertEqual(
            result.pieces["white_pawn_e"].board_position, GridPosition(3, 5)
        )
        self.assertEqual(result.pieces["black_pawn_d"].capture_slot, 2)

    def test_processed_event_is_rejected(self) -> None:
        state = BoardState.from_mapping(
            {
                **self.state.to_dict(),
                "processed_events": ["already-done"],
            }
        )
        move = MoveDelta.from_mapping(
            {
                "event_id": "already-done",
                "position": "white_pawn_e",
                "px": 4,
                "py": 3,
                "nx": 4,
                "ny": 4,
            }
        )
        with self.assertRaisesRegex(StateError, "already been applied"):
            state.validate_move(move)


if __name__ == "__main__":
    unittest.main()
