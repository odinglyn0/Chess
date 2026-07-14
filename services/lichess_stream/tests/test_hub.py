from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import chess

from chess_stream.config import Settings
from chess_stream.hub import GameSession, Subscriber
from chess_stream.schema import BoardStateValidator

SCHEMA_PATH = (
    Path(__file__).resolve().parents[3] / "schemas" / "board_state.schema.json"
)


def _settings() -> Settings:
    return Settings(schema_path=SCHEMA_PATH, validate_snapshots=True)


def _drain(subscriber: Subscriber) -> List[Dict[str, Any]]:
    messages: List[Dict[str, Any]] = []
    while True:
        try:
            messages.append(subscriber.queue.get_nowait())
        except Exception:
            break
    return messages


def _session_with_subscriber() -> tuple[GameSession, Subscriber]:
    settings = _settings()
    session = GameSession("abcd1234", settings, BoardStateValidator(SCHEMA_PATH))
    subscriber = Subscriber(settings.subscriber_queue_size)
    session._subscribers.add(subscriber)
    return session, subscriber


def test_description_initializes_and_snapshots() -> None:
    session, subscriber = _session_with_subscriber()
    data = {
        "id": "abcd1234",
        "variant": {"key": "standard"},
        "speed": "blitz",
        "rated": True,
        "players": {"white": {"user": {"name": "a"}}, "black": {"user": {"name": "b"}}},
        "fen": chess.Board().fen(),
        "status": {"name": "started"},
    }
    over = session._dispatch(data)
    assert over is False
    messages = _drain(subscriber)
    types = [m["type"] for m in messages]
    assert "game_info" in types
    assert "snapshot" in types
    snapshot = next(m for m in messages if m["type"] == "snapshot")
    assert len(snapshot["state"]["pieces"]) == 32


def test_move_message_emits_move() -> None:
    session, subscriber = _session_with_subscriber()
    board = chess.Board()
    session._dispatch(
        {
            "players": {"white": {}, "black": {}},
            "fen": board.fen(),
            "status": {"name": "started"},
        }
    )
    _drain(subscriber)
    board.push_uci("e2e4")
    session._dispatch({"fen": board.fen(), "lm": "e2e4", "wc": 300, "bc": 300})
    messages = _drain(subscriber)
    move_messages = [m for m in messages if m["type"] == "move"]
    assert len(move_messages) == 1
    move = move_messages[0]
    assert move["move"]["san"] == "e4"
    assert move["move"]["piece"] == "white_pawn_e2"
    assert move["clocks"] == {"wc": 300, "bc": 300}
    assert move["move"]["ply"] == 1
    assert move["state"]["revision"] == 2


def test_move_message_without_lm_uses_fen_inference() -> None:
    session, subscriber = _session_with_subscriber()
    board = chess.Board()
    session._dispatch(
        {"players": {}, "fen": board.fen(), "status": {"name": "started"}}
    )
    _drain(subscriber)
    board.push_uci("d2d4")
    session._dispatch({"fen": board.fen()})
    messages = _drain(subscriber)
    move_messages = [m for m in messages if m["type"] == "move"]
    assert len(move_messages) == 1
    assert move_messages[0]["move"]["uci"] == "d2d4"


def test_game_over_detected() -> None:
    session, subscriber = _session_with_subscriber()
    session._dispatch(
        {"players": {}, "fen": chess.Board().fen(), "status": {"name": "started"}}
    )
    _drain(subscriber)
    over = session._dispatch(
        {
            "players": {},
            "fen": chess.Board().fen(),
            "status": {"name": "mate"},
            "winner": "white",
        }
    )
    assert over is True
    messages = _drain(subscriber)
    game_over = [m for m in messages if m["type"] == "game_over"]
    assert len(game_over) == 1
    assert game_over[0]["winner"] == "white"


def test_resync_on_position_jump() -> None:
    session, subscriber = _session_with_subscriber()
    session._dispatch(
        {"players": {}, "fen": chess.Board().fen(), "status": {"name": "started"}}
    )
    _drain(subscriber)
    jumped = chess.Board()
    for uci in ("e2e4", "e7e5", "g1f3"):
        jumped.push_uci(uci)
    session._dispatch({"fen": jumped.fen()})
    messages = _drain(subscriber)
    assert any(m["type"] == "resync" for m in messages)
