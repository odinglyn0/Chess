from __future__ import annotations

from pathlib import Path

import chess
import pytest

from chess_stream.schema import BoardStateValidator, SchemaValidationError
from chess_stream.tracker import BoardTracker, TrackerError

SCHEMA_PATH = (
    Path(__file__).resolve().parents[3] / "schemas" / "board_state.schema.json"
)


@pytest.fixture(scope="module")
def validator() -> BoardStateValidator:
    return BoardStateValidator(SCHEMA_PATH)


def test_initial_snapshot_matches_schema(validator: BoardStateValidator) -> None:
    tracker = BoardTracker("abcd1234")
    snapshot = tracker.snapshot()
    validator.validate(snapshot)
    assert snapshot["schema_version"] == 1
    assert snapshot["revision"] == 0
    assert len(snapshot["pieces"]) == 32
    assert snapshot["pieces"]["white_pawn_e2"] == {
        "status": "board",
        "x": 4,
        "y": 1,
        "metadata": {"color": "white", "kind": "pawn"},
    }


def test_simple_pawn_move(validator: BoardStateValidator) -> None:
    tracker = BoardTracker("abcd1234")
    event = tracker.apply_uci("e2e4")
    assert event["piece"] == "white_pawn_e2"
    assert event["from"] == {"x": 4, "y": 1}
    assert event["to"] == {"x": 4, "y": 3}
    assert event["capture"] is None
    assert event["color"] == "white"
    assert event["san"] == "e4"
    assert event["event_id"] == "abcd1234.1"
    snapshot = tracker.snapshot()
    validator.validate(snapshot)
    assert snapshot["pieces"]["white_pawn_e2"]["y"] == 3
    assert snapshot["revision"] == 1


def test_capture_assigns_capture_slot(validator: BoardStateValidator) -> None:
    tracker = BoardTracker("abcd1234")
    for uci in ("e2e4", "d7d5"):
        tracker.apply_uci(uci)
    event = tracker.apply_uci("e4d5")
    assert event["capture"] is not None
    assert event["capture"]["piece"] == "black_pawn_d7"
    assert event["capture"]["capture_slot"] == 0
    assert event["capture"]["x"] == 3 and event["capture"]["y"] == 4
    snapshot = tracker.snapshot()
    validator.validate(snapshot)
    captured = snapshot["pieces"]["black_pawn_d7"]
    assert captured["status"] == "captured"
    assert captured["x"] is None and captured["y"] is None
    assert captured["capture_slot"] == 0


def test_en_passant_capture_square(validator: BoardStateValidator) -> None:
    tracker = BoardTracker("abcd1234")
    for uci in ("e2e4", "a7a6", "e4e5", "d7d5"):
        tracker.apply_uci(uci)
    event = tracker.apply_uci("e5d6")
    assert event["capture"] is not None
    assert event["capture"]["piece"] == "black_pawn_d7"
    assert event["capture"]["x"] == 3 and event["capture"]["y"] == 4
    assert event["to"] == {"x": 3, "y": 5}
    validator.validate(tracker.snapshot())


def test_castling_moves_rook(validator: BoardStateValidator) -> None:
    tracker = BoardTracker("abcd1234")
    for uci in ("e2e4", "e7e5", "g1f3", "b8c6", "f1c4", "f8c5"):
        tracker.apply_uci(uci)
    event = tracker.apply_uci("e1g1")
    assert event["castle"] is not None
    assert event["castle"]["rook"] == "white_rook_h1"
    assert event["castle"]["from"] == {"x": 7, "y": 0}
    assert event["castle"]["to"] == {"x": 5, "y": 0}
    snapshot = tracker.snapshot()
    validator.validate(snapshot)
    assert snapshot["pieces"]["white_rook_h1"] == {
        "status": "board",
        "x": 5,
        "y": 0,
        "metadata": {"color": "white", "kind": "rook"},
    }
    assert snapshot["pieces"]["white_king_e1"]["x"] == 6


def test_promotion_preserves_id_updates_kind(validator: BoardStateValidator) -> None:
    tracker = BoardTracker("abcd1234")
    tracker.reset_from_fen("8/P6k/8/8/8/8/7K/8 w - - 0 1")
    piece_id = "white_pawn_a7"
    assert piece_id in tracker.snapshot()["pieces"]
    event = tracker.apply_uci("a7a8q")
    assert event["promotion"] == "queen"
    assert event["piece"] == piece_id
    snapshot = tracker.snapshot()
    validator.validate(snapshot)
    assert snapshot["pieces"][piece_id]["metadata"]["kind"] == "queen"


def test_checkmate_flag() -> None:
    tracker = BoardTracker("abcd1234")
    for uci in ("e2e4", "e7e5", "f1c4", "b8c6", "d1h5", "g8f6"):
        tracker.apply_uci(uci)
    event = tracker.apply_uci("h5f7")
    assert event["checkmate"] is True
    assert event["check"] is True
    assert event["capture"]["piece"] == "black_pawn_f7"


def test_infer_uci_from_fen() -> None:
    tracker = BoardTracker("abcd1234")
    after_e4 = chess.Board()
    after_e4.push_uci("e2e4")
    assert tracker.infer_uci_from_fen(after_e4.fen()) == "e2e4"
    assert tracker.infer_uci_from_fen(chess.Board().fen()) is None


def test_illegal_move_raises() -> None:
    tracker = BoardTracker("abcd1234")
    with pytest.raises(TrackerError):
        tracker.apply_uci("e2e5")


def test_invalid_snapshot_detected(validator: BoardStateValidator) -> None:
    with pytest.raises(SchemaValidationError):
        validator.validate({"schema_version": 1, "revision": 0, "pieces": {}})
