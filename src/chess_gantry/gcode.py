"""Generate conservative Marlin G-code from physical piece transfers."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Iterable, Sequence, Tuple

from .config import AppConfig
from .models import PieceTransfer


def _format_number(value: float) -> str:
    text = f"{value:.3f}"
    text = text.rstrip("0").rstrip(".")
    return text if text not in {"-0", ""} else "0"


def _command_part(line: str) -> str:
    return line.split(";", 1)[0].strip()


@dataclass(frozen=True)
class GCodeProgram:
    lines: Tuple[str, ...]

    @property
    def commands(self) -> Tuple[str, ...]:
        return tuple(command for line in self.lines if (command := _command_part(line)))

    @property
    def digest(self) -> str:
        payload = ("\n".join(self.commands) + "\n").encode("ascii")
        return sha256(payload).hexdigest()

    def text(self) -> str:
        return "\n".join(self.lines) + "\n"


class GCodeGenerator:
    def __init__(self, config: AppConfig) -> None:
        self.config = config

    def _dwell(self, milliseconds: int) -> Iterable[str]:
        if milliseconds > 0:
            yield f"G4 P{milliseconds}"

    def generate(self, transfers: Sequence[PieceTransfer]) -> GCodeProgram:
        if not transfers:
            raise ValueError("at least one piece transfer is required")

        lines = [
            "; chess-gantry generated program",
            "G21 ; millimetres",
            "G90 ; absolute positioning",
            "; force magnet off before travel",
            *self.config.magnet.off_commands,
            "M400",
        ]

        for index, transfer in enumerate(transfers, start=1):
            lines.extend(
                [
                    "",
                    f"; transfer {index}: {transfer.purpose} piece {transfer.piece_id}",
                    (
                        f"G0 X{_format_number(transfer.start.x)} "
                        f"Y{_format_number(transfer.start.y)} "
                        f"F{_format_number(self.config.motion.travel_feed_mm_min)}"
                    ),
                    "M400 ; arrive before energising magnet",
                    *self.config.magnet.on_commands,
                    *self._dwell(self.config.motion.magnet_on_dwell_ms),
                ]
            )
            for waypoint in transfer.path[1:]:
                lines.append(
                    f"G1 X{_format_number(waypoint.x)} Y{_format_number(waypoint.y)} "
                    f"F{_format_number(self.config.motion.drag_feed_mm_min)}"
                )
            lines.extend(
                [
                    "M400 ; finish drag before releasing piece",
                    *self.config.magnet.off_commands,
                    *self._dwell(self.config.motion.magnet_off_dwell_ms),
                ]
            )

        if self.config.motion.park_after_move:
            park = self.config.motion.park_position
            assert park is not None
            lines.extend(
                [
                    "",
                    "; park with magnet off",
                    *self.config.magnet.off_commands,
                    (
                        f"G0 X{_format_number(park.x)} Y{_format_number(park.y)} "
                        f"F{_format_number(self.config.motion.travel_feed_mm_min)}"
                    ),
                    "M400",
                ]
            )

        lines.extend(["", "; final fail-safe magnet off", *self.config.magnet.off_commands, "M400"])
        return GCodeProgram(lines=tuple(lines))
