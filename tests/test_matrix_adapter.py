from __future__ import annotations

import unittest

from examples.matrix_adapter import diff_matrices


def empty_board():
    return [[None for _ in range(8)] for _ in range(8)]


class MatrixAdapterTests(unittest.TestCase):
    def test_normal_move(self) -> None:
        old = empty_board()
        new = empty_board()
        old[1][4] = "white_pawn_e"
        new[3][4] = "white_pawn_e"
        self.assertEqual(
            diff_matrices(old, new, "game-1"),
            [
                {
                    "event_id": "game-1-1",
                    "position": "white_pawn_e",
                    "px": 4,
                    "py": 1,
                    "nx": 4,
                    "ny": 3,
                }
            ],
        )

    def test_en_passant_includes_explicit_capture(self) -> None:
        old = empty_board()
        new = empty_board()
        old[4][4] = "white_pawn_e"
        old[4][3] = "black_pawn_d"
        new[5][3] = "white_pawn_e"
        delta = diff_matrices(old, new)[0]
        self.assertEqual(delta["capture"], {"id": "black_pawn_d", "x": 3, "y": 4})

    def test_castling_returns_two_deltas(self) -> None:
        old = empty_board()
        new = empty_board()
        old[0][4] = "white_king_e"
        old[0][7] = "white_rook_h"
        new[0][6] = "white_king_e"
        new[0][5] = "white_rook_h"
        deltas = diff_matrices(old, new)
        self.assertEqual(len(deltas), 2)
        self.assertEqual({d["position"] for d in deltas}, {"white_king_e", "white_rook_h"})


if __name__ == "__main__":
    unittest.main()
