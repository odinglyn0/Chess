from __future__ import annotations

import unittest

from chess_gantry.config import SerialSettings
from chess_gantry.errors import SerialProtocolError
from chess_gantry.serial_link import MarlinSerial


class FakeSerial:
    def __init__(self, responses=None, **kwargs):
        self.responses = list(responses or [])
        self.writes = []
        self.closed = False

    def write(self, payload):
        self.writes.append(payload)
        return len(payload)

    def flush(self):
        pass

    def readline(self):
        if self.responses:
            return self.responses.pop(0)
        return b""

    def reset_input_buffer(self):
        pass

    def close(self):
        self.closed = True


class SerialLinkTests(unittest.TestCase):
    def settings(self, command_timeout_s=0.03):
        return SerialSettings(
            port="loop",
            baudrate=115200,
            read_timeout_s=0.001,
            write_timeout_s=1.0,
            command_timeout_s=command_timeout_s,
            startup_wait_s=0.0,
        )

    def test_acknowledgement(self) -> None:
        fake = FakeSerial([b"echo:busy processing\n", b"ok\n"])
        link = MarlinSerial(self.settings(), serial_factory=lambda **kwargs: fake)
        with link:
            result = link.send_command("G90 ; comment")
        self.assertEqual(fake.writes, [b"G90\n"])
        self.assertEqual(result.responses[-1], "ok")
        self.assertTrue(fake.closed)

    def test_unknown_command_is_error(self) -> None:
        fake = FakeSerial([b'echo:Unknown command: "M9999"\n', b"ok\n"])
        link = MarlinSerial(self.settings(), serial_factory=lambda **kwargs: fake)
        with link, self.assertRaisesRegex(SerialProtocolError, "rejected"):
            link.send_command("M9999")

    def test_resend_request_is_error(self) -> None:
        fake = FakeSerial([b"Resend: 4\n"])
        link = MarlinSerial(self.settings(), serial_factory=lambda **kwargs: fake)
        with link, self.assertRaisesRegex(SerialProtocolError, "numbered-line resend"):
            link.send_command("G90")

    def test_timeout(self) -> None:
        fake = FakeSerial([])
        link = MarlinSerial(self.settings(command_timeout_s=0.005), serial_factory=lambda **kwargs: fake)
        with link, self.assertRaisesRegex(SerialProtocolError, "timeout"):
            link.send_command("M400")


if __name__ == "__main__":
    unittest.main()
