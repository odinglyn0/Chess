from __future__ import annotations

from pathlib import Path
import json
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DockerConfigurationTests(unittest.TestCase):
    def test_dockerfile_uses_ubuntu_builder_and_distroless_runtime(self) -> None:
        dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
        self.assertIn("FROM ubuntu:24.04 AS build", dockerfile)
        self.assertIn("FROM gcr.io/distroless/cc-debian12:latest", dockerfile)
        self.assertIn("uv python install 3.11", dockerfile)
        self.assertIn("uv sync --frozen", dockerfile)
        self.assertIn(
            "COPY --from=build /root/.local/bin/uv /opt/uv/bin/uv", dockerfile
        )
        self.assertIn('ENTRYPOINT ["/app/.venv/bin/python",', dockerfile)
        self.assertNotIn("apt-get", dockerfile.split("FROM gcr.io/distroless", 1)[1])

    def test_compose_passes_serial_persists_data_and_requires_token(self) -> None:
        compose = (ROOT / "docker-compose.pi.yml").read_text(encoding="utf-8")
        self.assertIn("CHESS_GANTRY_SERIAL_DEVICE", compose)
        self.assertIn("/dev/ttyUSB0", compose)
        self.assertIn("./config.json:/app/config.json:ro,Z", compose)
        self.assertIn("./data:/app/data:Z", compose)
        self.assertIn("CHESS_GANTRY_WEB_TOKEN:?", compose)
        self.assertIn("no-new-privileges:true", compose)
        self.assertIn("cap_drop", compose)
        self.assertNotIn("privileged: true", compose)
        self.assertIn("CHESS_GANTRY_DISTROLESS", compose)
        self.assertIn("healthcheck", compose)

    def test_python_entrypoint_runs_authenticated_network_ui_without_shell(
        self,
    ) -> None:
        entrypoint = (ROOT / "docker" / "entrypoint.py").read_text(encoding="utf-8")
        self.assertIn('"--host",', entrypoint)
        self.assertIn('"0.0.0.0",', entrypoint)
        self.assertIn('"--allow-network",', entrypoint)
        self.assertIn('"--auth-token",', entrypoint)
        self.assertFalse((ROOT / "docker" / "entrypoint.sh").exists())

    def test_pi_scripts_exist_and_are_executable(self) -> None:
        for path in (
            ROOT / "scripts" / "install_pi.sh",
            ROOT / "scripts" / "pi_docker.sh",
        ):
            self.assertTrue(path.exists())
            self.assertTrue(path.stat().st_mode & 0o111)

    def test_pi_update_script_rebuilds_after_git_pull(self) -> None:
        script = (ROOT / "scripts" / "pi_docker.sh").read_text(encoding="utf-8")
        self.assertIn("compose build --pull", script)
        self.assertIn("compose up -d --force-recreate", script)
        self.assertIn("distroless runtime intentionally has no shell", script)

    def test_config_serial_path_matches_container_device(self) -> None:
        config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
        self.assertEqual(config["serial"]["port"], "/dev/ttyUSB0")

    def test_dockerignore_excludes_large_local_directories(self) -> None:
        ignored = (ROOT / ".dockerignore").read_text(encoding="utf-8").splitlines()
        for value in (".git", ".venv", "node_modules", "data", "chicken/.pio"):
            self.assertIn(value, ignored)


if __name__ == "__main__":
    unittest.main()
