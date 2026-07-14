from __future__ import annotations

from pathlib import Path
from typing import Any, AsyncIterator, Dict, List

import chess
from fastapi.testclient import TestClient

from chess_stream import hub as hub_module
from chess_stream.app import create_app
from chess_stream.config import Settings

SCHEMA_PATH = (
    Path(__file__).resolve().parents[3] / "schemas" / "board_state.schema.json"
)


def _messages() -> List[Dict[str, Any]]:
    board = chess.Board()
    start = board.fen()
    board.push_uci("e2e4")
    after_e4 = board.fen()
    return [
        {
            "id": "abcd1234",
            "variant": {"key": "standard"},
            "speed": "blitz",
            "players": {"white": {}, "black": {}},
            "fen": start,
            "status": {"name": "started"},
        },
        {"fen": after_e4, "lm": "e2e4", "wc": 300, "bc": 300},
        {
            "players": {},
            "fen": after_e4,
            "status": {"name": "resign"},
            "winner": "black",
        },
    ]


class _FakeClient:
    payload: List[Dict[str, Any]] = []

    def __init__(self, **_kwargs: Any) -> None:
        pass

    async def aclose(self) -> None:
        return None

    async def stream_game(self, _game_id: str) -> AsyncIterator[Dict[str, Any]]:
        for message in _FakeClient.payload:
            yield message


def test_websocket_delivers_snapshot_move_and_game_over(monkeypatch) -> None:
    _FakeClient.payload = _messages()
    monkeypatch.setattr(hub_module, "LichessStreamClient", _FakeClient)

    app = create_app(Settings(schema_path=SCHEMA_PATH, validate_snapshots=True))
    with TestClient(app) as client:
        with client.websocket_connect("/ws/abcd1234") as ws:
            received: List[Dict[str, Any]] = []
            for _ in range(12):
                message = ws.receive_json()
                received.append(message)
                if message["type"] == "game_over":
                    break

    types = [m["type"] for m in received]
    assert "snapshot" in types
    assert "move" in types
    assert types[-1] == "game_over"

    move = next(m for m in received if m["type"] == "move")
    assert move["move"]["san"] == "e4"
    assert move["move"]["piece"] == "white_pawn_e2"
    assert len(move["state"]["pieces"]) == 32

    game_over = received[-1]
    assert game_over["winner"] == "black"


def test_invalid_game_id_rejected() -> None:
    app = create_app(Settings(schema_path=SCHEMA_PATH, validate_snapshots=True))
    with TestClient(app) as client:
        response = client.get("/games/!!/state")
        assert response.status_code == 422


def test_healthz_ok() -> None:
    app = create_app(Settings(schema_path=SCHEMA_PATH, validate_snapshots=True))
    with TestClient(app) as client:
        response = client.get("/healthz")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
