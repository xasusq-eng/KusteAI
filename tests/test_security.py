import time

from kusteai.security import CommandGuard


def test_allows_safe_command_without_approval() -> None:
    guard = CommandGuard(owner_pin="1234")
    result = guard.check("ls /sdcard")
    assert result.allowed is True


def test_blocks_dangerous_command_without_approval() -> None:
    guard = CommandGuard(owner_pin="1234")
    result = guard.check("rm -rf /sdcard/DCIM")
    assert result.allowed is False


def test_approval_allows_single_dangerous_command() -> None:
    guard = CommandGuard(owner_pin="1234", approval_ttl_seconds=1)
    assert guard.approve("1234") is True

    first = guard.check("rm -rf /sdcard/tmp")
    second = guard.check("rm -rf /sdcard/tmp")

    assert first.allowed is True
    assert second.allowed is False


def test_approval_expires() -> None:
    guard = CommandGuard(owner_pin="1234", approval_ttl_seconds=1)
    assert guard.approve("1234") is True
    time.sleep(1.1)
    result = guard.check("pm uninstall com.example.app")
    assert result.allowed is False
