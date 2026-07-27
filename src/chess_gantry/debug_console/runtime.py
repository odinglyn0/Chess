from __future__ import annotations

from collections import deque
from typing import Any, Deque, Dict, List, Optional, Sequence, Tuple
import secrets
import threading

from ..config import AppConfig
from ..controller import (
    MAX_RAW_COMMAND_CHARS,
    MAX_RAW_PROGRAM_COMMANDS,
    GantryController,
)
from ..errors import ConfigurationError
from ..persistence import AuditLog, utc_now

DEFAULT_LOG_CAPACITY = 400
MIN_TOKEN_CHARS = 12
TOKEN_HEADER = "X-Gantry-Token"
CLIENT_HEADER = "X-Gantry-Client"
TOKEN_ENVIRONMENT_KEY = "CHESS_GANTRY_DEBUG_TOKEN"
QUICK_COMMANDS: Tuple[Tuple[str, str], ...] = (
    ("M115", "firmware identity"),
    ("M114", "current position"),
    ("M119", "endstop states"),
    ("M105", "temperature report"),
    ("M400", "wait for moves to finish"),
    ("M84", "release the stepper motors"),
)


class ConsoleLog:
    def __init__(self, capacity: int = DEFAULT_LOG_CAPACITY) -> None:
        if capacity < 1:
            raise ConfigurationError("the console log capacity must be at least 1")
        self._events: Deque[Dict[str, Any]] = deque(maxlen=capacity)
        self._lock = threading.RLock()
        self._sequence = 0

    @property
    def capacity(self) -> int:
        return self._events.maxlen or DEFAULT_LOG_CAPACITY

    def append(
        self,
        *,
        kind: str,
        client: str,
        message: str,
        detail: Optional[Sequence[str]] = None,
    ) -> Dict[str, Any]:
        with self._lock:
            self._sequence += 1
            event: Dict[str, Any] = {
                "sequence": self._sequence,
                "timestamp": utc_now(),
                "kind": kind,
                "client": client,
                "message": message,
                "detail": list(detail or ()),
            }
            self._events.append(event)
            return dict(event)

    @property
    def latest_sequence(self) -> int:
        with self._lock:
            return self._sequence

    def since(self, sequence: int) -> Tuple[Tuple[Dict[str, Any], ...], int]:
        with self._lock:
            selected = [
                dict(event) for event in self._events if event["sequence"] > sequence
            ]
            return tuple(selected), self._sequence


class DebugRuntime:
    def __init__(
        self,
        *,
        config: AppConfig,
        controller: GantryController,
        token: str,
        audit: Optional[AuditLog] = None,
        log: Optional[ConsoleLog] = None,
        default_timeout_s: Optional[float] = None,
    ) -> None:
        if len(token) < MIN_TOKEN_CHARS:
            raise ConfigurationError(
                f"the access token must be at least {MIN_TOKEN_CHARS} characters"
            )
        self.config = config
        self.controller = controller
        self.token = token
        self.audit = audit
        self.log = log if log is not None else ConsoleLog()
        limit = config.serial.command_timeout_s
        resolved = (
            min(60.0, limit) if default_timeout_s is None else float(default_timeout_s)
        )
        if resolved <= 0 or resolved > limit:
            raise ConfigurationError(
                f"the default command timeout must be between 0 and {limit:g} seconds"
            )
        self.default_timeout_s = resolved

    def authorize(self, supplied: Optional[str]) -> bool:
        if not supplied:
            return False
        return secrets.compare_digest(supplied, self.token)

    def record(
        self,
        *,
        kind: str,
        client: str,
        message: str,
        detail: Optional[Sequence[str]] = None,
        audit: bool = False,
    ) -> Dict[str, Any]:
        event = self.log.append(
            kind=kind, client=client, message=message, detail=detail
        )
        if audit and self.audit is not None:
            self.audit.append(
                {
                    "action": f"debug_console.{kind}",
                    "client": client,
                    "message": message,
                    "detail": list(detail or ()),
                }
            )
        return event

    def limits(self) -> Dict[str, Any]:
        return {
            "max_command_chars": MAX_RAW_COMMAND_CHARS,
            "max_batch_commands": MAX_RAW_PROGRAM_COMMANDS,
            "default_timeout_s": self.default_timeout_s,
            "max_timeout_s": self.config.serial.command_timeout_s,
            "log_capacity": self.log.capacity,
        }

    def profile(self) -> Dict[str, Any]:
        return {
            "quick_commands": [
                {"command": command, "description": description}
                for command, description in QUICK_COMMANDS
            ],
            "magnet_on_commands": list(self.config.magnet.on_commands),
            "magnet_off_commands": list(self.config.magnet.off_commands),
            "emergency_stop_command": self.config.safety.emergency_stop_command,
            "travel_feed_mm_min": self.config.motion.travel_feed_mm_min,
            "configured_port": self.config.serial.port,
            "configured_baudrate": self.config.serial.baudrate,
        }

    def snapshot(self) -> Dict[str, Any]:
        payload = dict(self.controller.status())
        payload["limits"] = self.limits()
        payload["profile"] = self.profile()
        return payload


_runtime: Optional[DebugRuntime] = None
_runtime_lock = threading.RLock()


def set_runtime(runtime: Optional[DebugRuntime]) -> None:
    global _runtime
    with _runtime_lock:
        _runtime = runtime


def current_runtime() -> DebugRuntime:
    with _runtime_lock:
        if _runtime is None:
            raise ConfigurationError(
                "the debug console runtime is not configured; start it with "
                "'chess-gantry debug-console'"
            )
        return _runtime


def generate_token(length: int = 18) -> str:
    if length < MIN_TOKEN_CHARS:
        raise ConfigurationError(
            f"a generated token must be at least {MIN_TOKEN_CHARS} characters"
        )
    return secrets.token_urlsafe(length)


def token_fingerprint(token: str) -> str:
    visible = token[:4]
    return f"{visible}{'*' * max(len(token) - 4, 0)}"


def client_names(events: Sequence[Dict[str, Any]]) -> List[str]:
    seen: List[str] = []
    for event in events:
        name = str(event.get("client", ""))
        if name and name not in seen:
            seen.append(name)
    return seen
