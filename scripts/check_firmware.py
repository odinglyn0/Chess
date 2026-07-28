from __future__ import annotations

import argparse
import re

from chess_gantry.config import AppConfig
from chess_gantry.errors import GantryError
from chess_gantry.serial_link import MarlinSerial, parse_endstop_states


POSITION_RE = re.compile(
    r"\bX:\s*(-?\d+(?:\.\d+)?)\s+Y:\s*(-?\d+(?:\.\d+)?)\s+Z:\s*(-?\d+(?:\.\d+)?)",
    re.IGNORECASE,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Relay Chess Marlin firmware")
    parser.add_argument("--config", default="config.json")
    parser.add_argument("--home", action="store_true", help="run physical G28 X Y Z")
    parser.add_argument(
        "--confirm-clear-path",
        action="store_true",
        help="required with --home",
    )
    args = parser.parse_args()
    if args.home and not args.confirm_clear_path:
        parser.error("--home requires --confirm-clear-path")

    config = AppConfig.load(args.config)
    with MarlinSerial(config.serial) as link:
        try:
            identity = link.send_command("M115", timeout_s=10.0)
            identity_text = "\n".join(identity.responses)
            if "Relay Chess Gantry" not in identity_text:
                raise GantryError(
                    "M115 does not identify Relay Chess Gantry firmware; do not run homing"
                )
            before = link.send_command("M119", timeout_s=10.0)
            print(identity_text)
            print("\n".join(before.responses))
            if not args.home:
                print(
                    "Firmware identity and endstop reporting passed. Homing was not run."
                )
                return 0

            link.send_program(
                (*config.magnet.off_commands, *config.safety.home_commands)
            )
            endstops = link.send_command("M119", timeout_s=10.0)
            positions = link.send_command("M114", timeout_s=10.0)
        except KeyboardInterrupt:
            link.emergency_stop(config.safety.emergency_stop_command)
            print("Homing interrupted; emergency stop sent. Reset Marlin before reuse.")
            return 130
        states = parse_endstop_states(endstops.responses)
        expected = ("x_min", "y_max", "z_max")
        missing = [name for name in expected if name not in states]
        if missing:
            raise GantryError("M119 did not report " + ", ".join(missing))
        position = None
        for line in positions.responses:
            match = POSITION_RE.search(line)
            if match:
                position = tuple(float(match.group(index)) for index in range(1, 4))
                break
        if position is None:
            raise GantryError("M114 did not return parseable X/Y/Z coordinates")
        expected_position = (2.0, 298.0, 328.0)
        if any(
            abs(actual - wanted) > 0.1
            for actual, wanted in zip(position, expected_position)
        ):
            raise GantryError(
                f"unexpected home position {position}; expected {expected_position}"
            )
        print("\n".join(endstops.responses))
        print("\n".join(positions.responses))
        print("Firmware homing passed: X2 Y298 Z328 after 2 mm backoff.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GantryError as exc:
        print(f"Firmware check failed: {exc}")
        print(
            "If /dev/ttyUSB0 exists but no baud responds, verify the Ender 24 V "
            "supply, USB cable, and serial-port ownership. Reflashing is not required "
            "for the 330 x 300 host-side dimension remap."
        )
        raise SystemExit(1)
