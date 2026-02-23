from unittest.mock import patch

from kusteai.adb_bridge import ADBBridge
from kusteai.security import CommandGuard


class DummyCompleted:
    def __init__(self, returncode: int, stdout: str = "", stderr: str = "") -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def test_adb_bridge_blocks_without_approval() -> None:
    bridge = ADBBridge(guard=CommandGuard(owner_pin="1234"))
    out = bridge.run_shell("rm -rf /sdcard/tmp")
    assert "Подтвердите" in out


def test_adb_bridge_runs_command() -> None:
    guard = CommandGuard(owner_pin="1234")
    bridge = ADBBridge(guard=guard)

    with patch("subprocess.run", return_value=DummyCompleted(0, stdout="ok")) as run_mock:
        out = bridge.run_shell("echo hello")

    assert out == "ok"
    run_mock.assert_called_once()
