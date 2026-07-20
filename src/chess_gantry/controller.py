"""Shared controller used by the local browser interface.

This module joins the two workflows:

* manual X/Y checks that send direct Marlin coordinates; and
* validated JSON chess moves handled by :class:`GantryService`.

Both workflows share one serial connection, so two processes never compete for
exclusive ownership of the Ender controller's USB port.
"""

from __future__ import annotations

from dataclasses import replace
import math
import re
import threading
from typing import Any, Callable, Mapping, Optional

from .config import AppConfig, SerialSettings
from .errors import ConfigurationError, PendingTransactionError, SerialProtocolError, ValidationError
from .models import MachinePoint, MoveDelta
from .serial_link import DemoMarlinSerial, MarlinSerial, PortInfo, discover_serial_ports
from .service import GantryService, MotionPlan


_POSITION_RE = re.compile(
    r"\bX:\s*(-?\d+(?:\.\d+)?)\s+Y:\s*(-?\d+(?:\.\d+)?)",
    re.IGNORECASE,
)


class GantryController:
    """Stateful, thread-safe façade for web and interactive control."""

    def __init__(
        self,
        config: AppConfig,
        service: GantryService,
        *,
        link_factory: Optional[Callable[[SerialSettings], Any]] = None,
        demo: bool = False,
    ) -> None:
        self.config = config
        self.service = service
        self.demo = demo
        self._link_factory = link_factory or (
            (lambda settings: DemoMarlinSerial(settings))
            if demo
            else (lambda settings: MarlinSerial(settings))
        )
        self._link: Optional[Any] = None
        self._operation_lock = threading.RLock()
        self._homed = False
        self._position: Optional[MachinePoint] = None
        self._last_error: Optional[str] = None

    @property
    def connected(self) -> bool:
        return bool(self._link is not None and getattr(self._link, "connected", False))

    def available_ports(self) -> tuple[PortInfo, ...]:
        if self.demo:
            return (PortInfo("DEMO", "Simulated Marlin controller", "DEMO", True),)
        return discover_serial_ports()

    def status(self) -> dict[str, Any]:
        link = self._link
        try:
            revision = self.service.store.load().revision
        except Exception:
            revision = None
        return {
            "connected": self.connected,
            "port": None if link is None else getattr(link, "active_port", None),
            "baudrate": None if link is None else getattr(link, "active_baudrate", None),
            "firmware": None if link is None else getattr(link, "firmware_identity", None),
            "homed": self._homed,
            "position_mm": (
                {"x": self._position.x, "y": self._position.y}
                if self._position is not None
                else {"x": None, "y": None}
            ),
            "workspace_mm": {
                "min_x": self.config.workspace.min_x_mm,
                "max_x": self.config.workspace.max_x_mm,
                "min_y": self.config.workspace.min_y_mm,
                "max_y": self.config.workspace.max_y_mm,
            },
            "max_manual_feed_mm_min": self.config.motion.travel_feed_mm_min,
            "calibrated": self.config.safety.calibrated,
            "home_before_execute": self.config.safety.home_before_execute,
            "pending_transaction": self.service.journal.exists(),
            "board_revision": revision,
            "last_error": self._last_error,
            "demo": self.demo,
        }

    def connect(
        self,
        *,
        port: Optional[str] = None,
        baudrate: Optional[int] = None,
    ) -> dict[str, Any]:
        with self._operation_lock:
            if self.connected:
                return self.status()
            settings = self.config.serial
            if port:
                settings = replace(settings, port=port)
            if baudrate is not None:
                if baudrate <= 0:
                    raise ValidationError("baudrate must be a positive integer")
                settings = replace(settings, baudrate=baudrate, fallback_baudrates=())
            link = self._link_factory(settings)
            try:
                link.connect()
            except Exception as exc:
                self._last_error = str(exc)
                try:
                    link.close()
                except Exception:
                    pass
                raise
            self._link = link
            self._homed = False
            self._position = None
            self._last_error = None
            return self.status()

    def disconnect(self) -> dict[str, Any]:
        with self._operation_lock:
            link = self._link
            self._link = None
            if link is not None:
                link.close()
            self._homed = False
            self._position = None
            return self.status()

    def _require_link(self) -> Any:
        if not self.connected or self._link is None:
            raise SerialProtocolError("connect to the Marlin controller first")
        return self._link

    def _update_position(self, responses: tuple[str, ...]) -> Optional[MachinePoint]:
        for line in responses:
            match = _POSITION_RE.search(line)
            if match:
                self._position = MachinePoint(float(match.group(1)), float(match.group(2)))
                return self._position
        return None

    def query_position(self) -> dict[str, Any]:
        with self._operation_lock:
            link = self._require_link()
            result = link.send_command("M114", timeout_s=10.0)
            self._update_position(result.responses)
            return self.status()

    def check_endstops(self) -> tuple[str, ...]:
        with self._operation_lock:
            result = self._require_link().send_command("M119", timeout_s=10.0)
            return result.responses

    def home_xy(self) -> dict[str, Any]:
        with self._operation_lock:
            link = self._require_link()
            self.service.home_with_link(link)
            self._homed = True
            try:
                result = link.send_command("M114", timeout_s=10.0)
                self._update_position(result.responses)
            except Exception:
                # Homing itself succeeded; an optional position report should
                # not falsely claim that it did not.
                self._position = MachinePoint(0.0, 0.0)
            self._last_error = None
            return self.status()

    def move_to_mm(
        self,
        *,
        x_mm: float,
        y_mm: float,
        feed_mm_min: float,
    ) -> dict[str, Any]:
        values = (x_mm, y_mm, feed_mm_min)
        if not all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in values):
            raise ValidationError("X, Y, and feed rate must be numbers")
        x_mm, y_mm, feed_mm_min = map(float, values)
        if not all(math.isfinite(value) for value in (x_mm, y_mm, feed_mm_min)):
            raise ValidationError("X, Y, and feed rate must be finite")
        if feed_mm_min <= 0 or feed_mm_min > self.config.motion.travel_feed_mm_min:
            raise ValidationError(
                "manual feed rate must be greater than zero and no more than "
                f"{self.config.motion.travel_feed_mm_min:g} mm/min"
            )
        point = MachinePoint(x_mm, y_mm)
        if not self.config.workspace.contains(point):
            raise ValidationError("manual coordinate is outside the configured workspace")

        with self._operation_lock:
            if not self._homed:
                raise ConfigurationError("home X and Y before commanding an absolute coordinate")
            link = self._require_link()
            link.send_program(
                (
                    "G21",
                    "G90",
                    *self.config.magnet.off_commands,
                    f"G1 X{x_mm:.3f} Y{y_mm:.3f} F{feed_mm_min:.0f}",
                    "M400",
                )
            )
            self._position = point
            try:
                result = link.send_command("M114", timeout_s=10.0)
                self._update_position(result.responses)
            except Exception:
                pass
            self._last_error = None
            return self.status()

    def _move_from_mapping(self, raw_move: Mapping[str, Any]) -> MoveDelta:
        return MoveDelta.from_mapping(
            raw_move,
            self.config.board.width,
            self.config.board.height,
        )

    def plan_move(self, raw_move: Mapping[str, Any]) -> MotionPlan:
        move = self._move_from_mapping(raw_move)
        if self.service.journal.exists():
            raise PendingTransactionError(
                f"pending transaction exists at {self.service.journal.path}; reconcile it first"
            )
        with self.service.store.locked():
            return self.service.plan(move, self.service.store.load())

    def execute_move(
        self,
        raw_move: Mapping[str, Any],
        *,
        confirm_motion: bool,
    ) -> MotionPlan:
        if not confirm_motion:
            raise ConfigurationError("execution requires explicit motion confirmation")
        move = self._move_from_mapping(raw_move)
        with self._operation_lock:
            link = self._require_link()
            if not self.config.safety.home_before_execute and not self._homed:
                raise ConfigurationError(
                    "home X/Y first, or enable safety.home_before_execute"
                )
            plan = self.service.execute_with_link(move, link)
            if self.config.safety.home_before_execute:
                self._homed = True
            if self.config.motion.park_after_move:
                self._position = self.config.motion.park_position
            else:
                self._position = plan.transfers[-1].end
            self._last_error = None
            return plan

    def board_state(self) -> dict[str, Any]:
        return self.service.store.load().to_dict()

    def pending_transaction(self) -> Optional[dict[str, Any]]:
        if not self.service.journal.exists():
            return None
        return dict(self.service.journal.load())

    def emergency_stop(self) -> dict[str, Any]:
        # Do not wait for the normal operation lock: an M400 command could be
        # blocking another request while the stop still needs to be sent.
        link = self._link
        if link is None or not getattr(link, "connected", False):
            raise SerialProtocolError("the Marlin controller is not connected")
        try:
            self.service.emergency_stop_with_link(link)
        finally:
            try:
                link.close()
            finally:
                self._link = None
                self._homed = False
                self._position = None
                self._last_error = (
                    "Emergency stop sent. Reset or power-cycle the controller, "
                    "then reconnect and re-home."
                )
        return self.status()
