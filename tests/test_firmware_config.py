from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
MARLIN = ROOT / "chicken" / "Marlin"


class FirmwareConfigurationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.configuration = (MARLIN / "Configuration.h").read_text(encoding="utf-8")
        cls.advanced = (MARLIN / "Configuration_adv.h").read_text(encoding="utf-8")
        cls.pins = (
            MARLIN / "src" / "pins" / "stm32f1" / "pins_CREALITY_V422.h"
        ).read_text(encoding="utf-8")
        cls.platformio = (ROOT / "chicken" / "platformio.ini").read_text(
            encoding="utf-8"
        )

    def assert_define(self, text: str, name: str, value: str) -> None:
        self.assertRegex(
            text, rf"(?m)^\s*#define\s+{name}\s+{re.escape(value)}\s*(?://.*)?$"
        )

    def test_exact_board_and_build_target(self) -> None:
        self.assert_define(self.configuration, "MOTHERBOARD", "BOARD_CREALITY_V422")
        self.assertRegex(
            self.platformio,
            r"(?m)^default_envs\s*=\s*STM32F103RE_creality\s*$",
        )

    def test_outer_axes_home_together_to_independent_switches(self) -> None:
        self.assert_define(self.configuration, "X_HOME_DIR", "-1")
        self.assert_define(self.configuration, "Y_HOME_DIR", "1")
        self.assertRegex(self.advanced, r"(?m)^\s*#define\s+QUICK_HOME\b")
        self.assertRegex(
            self.configuration, r"(?m)^\s*#define\s+VALIDATE_HOMING_ENDSTOPS\b"
        )

    def test_inner_z_axis_uses_physical_e_driver_and_z_switch(self) -> None:
        self.assert_define(self.pins, "Z_STEP_PIN", "PB4")
        self.assert_define(self.pins, "Z_DIR_PIN", "PB3")
        self.assert_define(self.configuration, "Z_HOME_DIR", "1")
        self.assert_define(self.configuration, "Z_MAX_POS", "350")
        self.assertNotRegex(self.configuration, r"(?m)^\s*#define\s+BLTOUCH\b")
        self.assertNotRegex(
            self.configuration,
            r"(?m)^\s*#define\s+Z_MIN_PROBE_USES_Z_MIN_ENDSTOP_PIN\b",
        )

    def test_motion_and_non_printer_safety_profile(self) -> None:
        self.assert_define(
            self.configuration, "DEFAULT_AXIS_STEPS_PER_UNIT", "{ 80, 80, 80 }"
        )
        self.assert_define(self.configuration, "EXTRUDERS", "0")
        self.assert_define(self.configuration, "TEMP_SENSOR_0", "0")
        self.assert_define(self.configuration, "TEMP_SENSOR_BED", "0")
        self.assertRegex(
            self.advanced, r"(?m)^\s*#define\s+ENDSTOPS_ALWAYS_ON_DEFAULT\b"
        )


if __name__ == "__main__":
    unittest.main()
