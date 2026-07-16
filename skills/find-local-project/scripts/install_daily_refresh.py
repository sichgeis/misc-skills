#!/usr/bin/env python3
"""Install or manage the macOS launch agent for local project catalog refresh."""

from __future__ import annotations

import argparse
import os
import plistlib
import subprocess
import sys
from pathlib import Path
from typing import Any


LABEL = "com.christian.codex.local-project-catalog"
PLIST_NAME = f"{LABEL}.plist"


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()


def launch_agents_dir() -> Path:
    return Path.home() / "Library" / "LaunchAgents"


def plist_path() -> Path:
    return launch_agents_dir() / PLIST_NAME


def service_target() -> str:
    return f"gui/{os.getuid()}/{LABEL}"


def launch_domain() -> str:
    return f"gui/{os.getuid()}"


def scanner_path() -> Path:
    return Path(__file__).resolve().with_name("local_projects.py")


def run_launchctl(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["launchctl", *args],
        check=check,
        capture_output=True,
        text=True,
    )


def payload() -> dict[str, Any]:
    logs = codex_home() / "logs"
    return {
        "Label": LABEL,
        "ProgramArguments": [
            sys.executable,
            str(scanner_path()),
            "refresh",
        ],
        "RunAtLoad": True,
        "StartCalendarInterval": {
            "Hour": 9,
            "Minute": 0,
        },
        "ProcessType": "Background",
        "Nice": 10,
        "StandardOutPath": str(logs / "local-project-catalog.log"),
        "StandardErrorPath": str(logs / "local-project-catalog.error.log"),
    }


def installed() -> bool:
    return run_launchctl("print", service_target(), check=False).returncode == 0


def install() -> None:
    if sys.platform != "darwin":
        raise SystemExit("This installer supports macOS only.")
    if not scanner_path().is_file():
        raise SystemExit(f"Scanner not found: {scanner_path()}")

    launch_agents_dir().mkdir(parents=True, exist_ok=True)
    (codex_home() / "logs").mkdir(parents=True, exist_ok=True)

    path = plist_path()
    with path.open("wb") as output:
        plistlib.dump(payload(), output, sort_keys=False)

    if installed():
        run_launchctl("bootout", service_target())
    run_launchctl("bootstrap", launch_domain(), str(path))
    run_launchctl("enable", service_target())
    run_launchctl("kickstart", "-k", service_target())
    print(f"Installed and started {LABEL}")
    print(f"Schedule: daily at 09:00 local time, plus RunAtLoad")
    print(f"Plist: {path}")


def uninstall() -> None:
    if installed():
        run_launchctl("bootout", service_target())
    path = plist_path()
    if path.exists():
        path.unlink()
    print(f"Uninstalled {LABEL}")


def status() -> int:
    result = run_launchctl("print", service_target(), check=False)
    if result.returncode != 0:
        print(f"{LABEL} is not loaded")
        return 1
    print(result.stdout.rstrip())
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("install", "status", "uninstall"))
    args = parser.parse_args()

    if args.command == "install":
        install()
        return 0
    if args.command == "uninstall":
        uninstall()
        return 0
    return status()


if __name__ == "__main__":
    sys.exit(main())
