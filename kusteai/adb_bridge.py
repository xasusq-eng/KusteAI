from __future__ import annotations

import subprocess

from kusteai.security import CommandGuard


class ADBBridge:
    def __init__(self, guard: CommandGuard, adb_path: str = "adb") -> None:
        self.guard = guard
        self.adb_path = adb_path

    def run_shell(self, command: str, timeout: int = 25) -> str:
        check = self.guard.check(command)
        if not check.allowed:
            return check.reason

        proc = subprocess.run(
            [self.adb_path, "shell", command],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )

        output = (proc.stdout or "").strip()
        error = (proc.stderr or "").strip()

        if proc.returncode != 0:
            return f"ADB ошибка ({proc.returncode}): {error or output or 'нет деталей'}"

        return output or "Готово."
