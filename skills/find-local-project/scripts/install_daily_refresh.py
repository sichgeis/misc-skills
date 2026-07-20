#!/usr/bin/env python3
"""Install or manage the macOS launch agent for local project catalog refresh."""

from __future__ import annotations

import argparse
import os
import plistlib
import subprocess
import sys
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any


LABEL = "com.christian.local-project-catalog"
LEGACY_LABELS = ("com.christian.codex.local-project-catalog",)
STATE_HOME_ENV = "LOCAL_PROJECTS_HOME"
STATE_DIR_NAME = "local-projects"
CATALOG_NAME = "local-projects.json"

LaunchctlRunner = Callable[..., subprocess.CompletedProcess[str]]


def state_home(
    environ: Mapping[str, str] | None = None,
    home: Path | None = None,
) -> Path:
    env = os.environ if environ is None else environ
    if env.get(STATE_HOME_ENV):
        return Path(env[STATE_HOME_ENV]).expanduser()
    if env.get("XDG_STATE_HOME"):
        return Path(env["XDG_STATE_HOME"]).expanduser() / STATE_DIR_NAME
    base_home = Path.home() if home is None else home
    return base_home / ".local" / "state" / STATE_DIR_NAME


def launch_agents_dir(home: Path | None = None) -> Path:
    base_home = Path.home() if home is None else home
    return base_home / "Library" / "LaunchAgents"


def plist_path(
    label: str = LABEL,
    *,
    agents_dir: Path | None = None,
) -> Path:
    directory = launch_agents_dir() if agents_dir is None else agents_dir
    return directory / f"{label}.plist"


def service_target(label: str = LABEL, *, uid: int | None = None) -> str:
    user_id = os.getuid() if uid is None else uid
    return f"gui/{user_id}/{label}"


def launch_domain(*, uid: int | None = None) -> str:
    user_id = os.getuid() if uid is None else uid
    return f"gui/{user_id}"


def scanner_path(script_file: Path | None = None) -> Path:
    source = Path(__file__) if script_file is None else script_file
    return source.resolve().with_name("local_projects.py")


def run_launchctl(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["launchctl", *args],
        check=check,
        capture_output=True,
        text=True,
    )


def payload(
    *,
    scanner: Path | None = None,
    python_executable: str | None = None,
    catalog_home: Path | None = None,
) -> dict[str, Any]:
    home = state_home() if catalog_home is None else catalog_home
    logs = home / "logs"
    catalog = home / CATALOG_NAME
    return {
        "Label": LABEL,
        "ProgramArguments": [
            sys.executable if python_executable is None else python_executable,
            str(scanner_path() if scanner is None else scanner),
            "--json",
            str(catalog),
            "--markdown",
            str(catalog.with_suffix(".md")),
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


def recognized_labels() -> tuple[str, ...]:
    return (LABEL, *LEGACY_LABELS)


def installed(
    label: str = LABEL,
    *,
    runner: LaunchctlRunner = run_launchctl,
    uid: int | None = None,
) -> bool:
    result = runner("print", service_target(label, uid=uid), check=False)
    return result.returncode == 0


def retire_legacy_jobs(
    *,
    agents_dir: Path | None = None,
    runner: LaunchctlRunner = run_launchctl,
    uid: int | None = None,
) -> None:
    directory = launch_agents_dir() if agents_dir is None else agents_dir
    for label in LEGACY_LABELS:
        if installed(label, runner=runner, uid=uid):
            runner("bootout", service_target(label, uid=uid))
        path = plist_path(label, agents_dir=directory)
        if path.exists():
            path.unlink()


def install() -> None:
    if sys.platform != "darwin":
        raise SystemExit("This installer supports macOS only.")

    scanner = scanner_path()
    if not scanner.is_file():
        raise SystemExit(f"Scanner not found: {scanner}")

    agents_dir = launch_agents_dir()
    catalog_home = state_home()
    agents_dir.mkdir(parents=True, exist_ok=True)
    (catalog_home / "logs").mkdir(parents=True, exist_ok=True)

    path = plist_path(agents_dir=agents_dir)
    with path.open("wb") as output:
        plistlib.dump(
            payload(scanner=scanner, catalog_home=catalog_home),
            output,
            sort_keys=False,
        )

    if installed(LABEL):
        run_launchctl("bootout", service_target())
    retire_legacy_jobs(agents_dir=agents_dir)
    run_launchctl("bootstrap", launch_domain(), str(path))
    run_launchctl("enable", service_target())
    run_launchctl("kickstart", "-k", service_target())
    print(f"Installed and started {LABEL}")
    print("Schedule: daily at 09:00 local time, plus RunAtLoad")
    print(f"Catalog state: {catalog_home}")
    print(f"Plist: {path}")


def uninstall() -> None:
    agents_dir = launch_agents_dir()
    for label in recognized_labels():
        if installed(label):
            run_launchctl("bootout", service_target(label))
        path = plist_path(label, agents_dir=agents_dir)
        if path.exists():
            path.unlink()
    print(f"Uninstalled recognized local project refresh jobs: {', '.join(recognized_labels())}")


def status() -> int:
    found = False
    for label in recognized_labels():
        result = run_launchctl("print", service_target(label), check=False)
        if result.returncode != 0:
            continue
        found = True
        print(f"[{label}]")
        print(result.stdout.rstrip())
    if found:
        return 0
    print(f"No recognized local project refresh job is loaded ({', '.join(recognized_labels())})")
    return 1


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
