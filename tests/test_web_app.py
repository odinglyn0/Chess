from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import json
import threading
import unittest
import urllib.error
import urllib.request

from chess_gantry.config import AppConfig
from chess_gantry.controller import GantryController
from chess_gantry.errors import ValidationError
from chess_gantry.models import BoardState
from chess_gantry.operations import OperationManager, OperationSpec
from chess_gantry.persistence import atomic_write_json
from chess_gantry.service import GantryService
from chess_gantry.web_app import GantryHTTPServer, RequestHandler, validate_web_access

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
        self.server.operation_manager = OperationManager(
            root,
            self.controller,
            (
                OperationSpec(
                    "web-test",
                    "Web test",
                    "Print one line.",
                    "Checks",
                    ("/usr/bin/env", "true"),
                ),
            ),
        )
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
        self.assertIn("G1 X163 Y137 Z190", plan["gcode"])
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

    def test_live_position_and_keyboard_jog_api(self) -> None:
        self.request("/api/connect", {})
        self.request("/api/home", {"confirm_motion": True})
        _, position = self.request("/api/position", {})
        self.assertEqual(
            position["status"]["machine_position_mm"],
            {"x": 2.0, "y": 298.0, "z": 328.0},
        )
        _, jogged = self.request(
            "/api/jog",
            {
                "delta_x_mm": -5,
                "delta_y_mm": 0,
                "feed_mm_min": 600,
                "confirm_motion": True,
            },
        )
        self.assertEqual(jogged["status"]["position_mm"], {"x": 323.0, "y": 298.0})
        self.assertEqual(
            jogged["status"]["machine_position_mm"],
            {"x": 2.0, "y": 298.0, "z": 323.0},
        )

    def test_operations_catalog_and_task_api(self) -> None:
        _, catalog = self.request("/api/operations")
        self.assertEqual(catalog["operations"][0]["id"], "web-test")
        _, started = self.request(
            "/api/tasks/start",
            {"operation_id": "web-test", "confirmations": {}},
        )
        self.assertIn(started["run"]["state"], {"starting", "running", "completed"})
        for _ in range(100):
            _, status = self.request("/api/tasks/status")
            if status["run"]["state"] == "completed":
                break
            threading.Event().wait(0.01)
        self.assertEqual(status["run"]["state"], "completed")
        self.assertEqual(status["run"]["returncode"], 0)

    def test_dashboard_page_contains_operations_controls(self) -> None:
        request = urllib.request.Request(self.base + "/")
        with urllib.request.urlopen(request, timeout=3) as response:
            html = response.read().decode("utf-8")
        self.assertIn("Operations dashboard", html)
        self.assertIn('id="taskStop"', html)
        self.assertIn("/api/tasks/start", html)
        self.assertIn('id="keyboardArm"', html)
        self.assertIn('id="machineZ"', html)
        self.assertIn("ArrowLeft", html)
        self.assertIn("/api/jog", html)

    def test_network_bind_requires_explicit_flag_and_strong_token(self) -> None:
        with self.assertRaisesRegex(ValidationError, "--allow-network"):
            validate_web_access("0.0.0.0", False, "a" * 32)
        with self.assertRaisesRegex(ValidationError, "at least 24"):
            validate_web_access("0.0.0.0", True, None)
        with self.assertRaisesRegex(ValidationError, "at least 24"):
            validate_web_access("0.0.0.0", True, "short")
        self.assertTrue(validate_web_access("0.0.0.0", True, "a" * 32))
        self.assertFalse(validate_web_access("127.0.0.1", False, None))

    def test_authenticated_server_protects_page_and_apis(self) -> None:
        token = "network-dashboard-test-token-123456"
        self.server.auth_token_hash = hashlib.sha256(token.encode()).digest()
        cookie_jar = urllib.request.HTTPCookieProcessor()
        opener = urllib.request.build_opener(cookie_jar)
        with self.assertRaises(urllib.error.HTTPError) as unauthorized:
            opener.open(self.base + "/api/status", timeout=3)
        self.assertEqual(unauthorized.exception.code, 401)
        unauthorized.exception.close()

        with self.assertRaises(urllib.error.HTTPError) as bad_token:
            opener.open(self.base + "/?token=wrong", timeout=3)
        self.assertEqual(bad_token.exception.code, 401)
        bad_token.exception.close()

        with opener.open(self.base + f"/?token={token}", timeout=3) as response:
            html = response.read().decode("utf-8")
        self.assertIn("Operations dashboard", html)
        cookie = next(iter(cookie_jar.cookiejar))
        self.assertEqual(cookie.name, "gantry_session")
        self.assertTrue(cookie.has_nonstandard_attr("HttpOnly"))
        self.assertEqual(cookie.get_nonstandard_attr("SameSite"), "Strict")

        with opener.open(self.base + "/api/status", timeout=3) as response:
            payload = json.loads(response.read())
        self.assertTrue(payload["ok"])


if __name__ == "__main__":
    unittest.main()
