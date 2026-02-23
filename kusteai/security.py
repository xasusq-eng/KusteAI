from __future__ import annotations

import re
import time
from dataclasses import dataclass


DANGEROUS_PATTERNS = [
    r"\brm\b",
    r"\bmkfs\b",
    r"\bdd\b",
    r"\bpm\s+uninstall\b",
    r"\bam\s+force-stop\b",
    r"\breboot\b",
]


@dataclass
class GuardResult:
    allowed: bool
    reason: str = ""


class CommandGuard:
    """Blocks destructive commands unless owner PIN approval is active."""

    def __init__(self, owner_pin: str, approval_ttl_seconds: int = 60) -> None:
        self.owner_pin = owner_pin.strip()
        self.approval_ttl_seconds = approval_ttl_seconds
        self._approved_until = 0.0

    def approve(self, pin: str) -> bool:
        if not self.owner_pin:
            return False
        if pin.strip() != self.owner_pin:
            return False
        self._approved_until = time.time() + self.approval_ttl_seconds
        return True

    def _is_dangerous(self, command: str) -> bool:
        return any(re.search(pattern, command) for pattern in DANGEROUS_PATTERNS)

    def check(self, command: str) -> GuardResult:
        if not self._is_dangerous(command):
            return GuardResult(True)

        if time.time() <= self._approved_until:
            # One dangerous window consumed by this execution.
            self._approved_until = 0.0
            return GuardResult(True)

        return GuardResult(
            False,
            "Команда выглядит опасной. Подтвердите владельцем: /approve <PIN>, затем повторите команду.",
        )
