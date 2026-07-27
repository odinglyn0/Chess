from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import json
import threading
import unittest
import urllib.request

from chess_gantry.config import AppConfig
from chess_gantry.controller import GantryController
from chess_gantry.models import BoardState
from chess_gantry.persistence import atomic_write_json
from chess_gantry.service import GantryService
from chess_gantry.web_app import GantryHTTPServer, RequestHandler

ROOT = Path(__file__).resolve().parents[1]


class WebAppTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        root = Path(self.temporary.name)
        raw = json.loads((ROOT / "config.example.json").read_text(encoding="utf-8"))
        raw["planner"]["kind"] = "direct"
        raw["capture"] = {"enabled": False, "slots": []}
        raw["safety"]["calibrated"] = True
        raw["safety"]["preflight_commands"] = []
        self.config = AppConfig.from_mapping(raw)
        state = BoardState.from_mapping(
            {
                "schema_version": 1,
                "revision": 0,
                "pieces": {"white_pawn_e": {"status": "board", "x": 4, "y": 1}},
                "processed_events": [],
            }
        )
        state_path = root / "state.json"
        atomic_write_json(state_path, state.to_dict())
        service = GantryService(
            self.config,
            state_path,
            root / "pending.json",
            root / "audit.jsonl",
        )
        self.controller = GantryController(self.config, service, demo=True)
        RequestHandler.controller = self.controller
        self.server = GantryHTTPServer(("127.0.0.1", 0), RequestHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.controller.disconnect()
        self.temporary.cleanup()

    def request(self, path, payload=None):
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self.base + path,
            data=data,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=3) as response:
            return response.status, json.loads(response.read())

    def test_plan_and_execute_api_share_integrated_workflow(self) -> None:
        move = {
            "event_id": "web-1",
            "position": "white_pawn_e",
            "px": 4,
            "py": 1,
            "nx": 4,
            "ny": 3,
        }
        _, plan = self.request("/api/plan", {"move": move})
        self.assertIn("G1 X280 Y70 E90", plan["gcode"])
        _, board_before = self.request("/api/board")
        self.assertEqual(board_before["board_state"]["revision"], 0)

        _, connected = self.request("/api/connect", {})
        self.assertTrue(connected["status"]["connected"])
        self.request("/api/home", {"confirm_motion": True})
        _, executed = self.request(
            "/api/execute",
            {"move": move, "confirm_motion": True},
        )
        self.assertEqual(executed["summary"]["next_revision"], 1)
        _, board_after = self.request("/api/board")
        self.assertEqual(board_after["board_state"]["revision"], 1)
        self.assertEqual(board_after["board_state"]["pieces"]["white_pawn_e"]["y"], 3)

    def test_manual_api_homes_then_moves(self) -> None:
        self.request("/api/connect", {})
        _, home = self.request("/api/home", {"confirm_motion": True})
        self.assertTrue(home["status"]["homed"])
        _, moved = self.request(
            "/api/move",
            {"x_mm": 20, "y_mm": 30, "feed_mm_min": 600, "confirm_motion": True},
        )
        self.assertEqual(moved["status"]["position_mm"], {"x": 20.0, "y": 30.0})


if __name__ == "__main__":
    unittest.main()
