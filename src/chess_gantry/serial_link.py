"""Small, blocking Marlin serial client with explicit acknowledgement handling."""

from __future__ import annotations

from dataclasses import dataclass
from time import monotonic, sleep
from typing import Any, Callable, Iterable, List, Optional, Sequence, Tuple

from .config import SerialSettings
from .errors import SerialProtocolError


@dataclass(frozen=True)
class CommandResult:
    command: str
    responses: Tuple[str, ...]


class MarlinSerial:
    """Send one command at a time and wait for Marlin's ``ok`` response."""

    def __init__(
        self,
        settings: SerialSettings,
        serial_factory: Optional[Callable[..., Any]] = None,
    ) -> None:
        self.settings = settings
        self._serial_factory = serial_factory
        self._serial: Optional[Any] = None

    @property
    def connected(self) -> bool:
        return self._serial is not None

    def connect(self) -> None:
        if self._serial is not None:
            return
        factory = self._serial_factory
        if factory is None:
            try:
                import serial  # type: ignore
            except ImportError as exc:
                raise SerialProtocolError(
                    "pyserial is not installed; run 'python -m pip install -e .'"
                ) from exc
            factory = serial.Serial
        try:
            self._serial = factory(
                port=self.settings.port,
                baudrate=self.settings.baudrate,
                timeout=self.settings.read_timeout_s,
                write_timeout=self.settings.write_timeout_s,
                rtscts=False,
                dsrdtr=False,
            )
            if self.settings.startup_wait_s:
                sleep(self.settings.startup_wait_s)
            reset = getattr(self._serial, "reset_input_buffer", None)
            if callable(reset):
                reset()
        except Exception as exc:
            self._serial = None
            raise SerialProtocolError(
                f"could not open {self.settings.port} at {self.settings.baudrate} baud: {exc}"
            ) from exc

    def close(self) -> None:
        serial_object = self._serial
        self._serial = None
        if serial_object is not None:
            close = getattr(serial_object, "close", None)
            if callable(close):
                close()

    def __enter__(self) -> "MarlinSerial":
        self.connect()
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        self.close()

    def _require_connected(self) -> Any:
        if self._serial is None:
            raise SerialProtocolError("serial link is not connected")
        return self._serial

    def send_command(self, command: str, timeout_s: Optional[float] = None) -> CommandResult:
        serial_object = self._require_connected()
        stripped = command.split(";", 1)[0].strip()
        if not stripped:
            return CommandResult(command="", responses=())
        if "\n" in stripped or "\r" in stripped:
            raise SerialProtocolError("a serial command cannot contain a newline")
        try:
            payload = (stripped + "\n").encode("ascii")
        except UnicodeEncodeError as exc:
            raise SerialProtocolError(f"G-code must be ASCII: {stripped!r}") from exc

        try:
            serial_object.write(payload)
            flush = getattr(serial_object, "flush", None)
            if callable(flush):
                flush()
        except Exception as exc:
            raise SerialProtocolError(f"failed to write command {stripped!r}: {exc}") from exc

        deadline = monotonic() + (timeout_s if timeout_s is not None else self.settings.command_timeout_s)
        responses: List[str] = []
        while monotonic() < deadline:
            try:
                raw = serial_object.readline()
            except Exception as exc:
                raise SerialProtocolError(f"failed while reading response to {stripped!r}: {exc}") from exc
            if not raw:
                continue
            if isinstance(raw, bytes):
                line = raw.decode("utf-8", errors="replace").strip()
            else:
                line = str(raw).strip()
            if not line:
                continue
            responses.append(line)
            lower = line.lower()
            if lower.startswith("ok"):
                return CommandResult(command=stripped, responses=tuple(responses))
            if (
                lower.startswith("error")
                or lower.startswith("!!")
                or "unknown command" in lower
                or "printer halted" in lower
                or "kill() called" in lower
            ):
                raise SerialProtocolError(
                    f"Marlin rejected {stripped!r}: {' | '.join(responses[-8:])}"
                )
            if lower.startswith("resend:") or lower.startswith("rs "):
                raise SerialProtocolError(
                    "Marlin requested a numbered-line resend, which this simple USB protocol does not use: "
                    + line
                )
            # echo:, busy:, wait, temperatures, and startup text are informational.

        detail = " | ".join(responses[-8:]) if responses else "no response"
        raise SerialProtocolError(f"timeout waiting for Marlin acknowledgement of {stripped!r}: {detail}")

    def send_program(self, commands: Iterable[str]) -> Tuple[CommandResult, ...]:
        results = []
        for command in commands:
            result = self.send_command(command)
            if result.command:
                results.append(result)
        return tuple(results)

    def best_effort(self, commands: Sequence[str]) -> None:
        for command in commands:
            try:
                self.send_command(command, timeout_s=min(5.0, self.settings.command_timeout_s))
            except Exception:
                return

    def emergency_stop(self, command: str = "M112") -> None:
        serial_object = self._require_connected()
        try:
            serial_object.write((command.strip() + "\n").encode("ascii"))
            flush = getattr(serial_object, "flush", None)
            if callable(flush):
                flush()
        except Exception as exc:
            raise SerialProtocolError(f"failed to send emergency stop: {exc}") from exc


def list_serial_ports() -> Tuple[Tuple[str, str], ...]:
    try:
        from serial.tools import list_ports  # type: ignore
    except ImportError as exc:
        raise SerialProtocolError("pyserial is not installed") from exc
    return tuple((port.device, port.description or "") for port in list_ports.comports())
