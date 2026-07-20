from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import ModuleType


SCRIPT = Path(__file__).parents[1] / "scripts" / "install_daily_refresh.py"


def load_script() -> ModuleType:
    spec = importlib.util.spec_from_file_location("install_daily_refresh", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


installer = load_script()


class RetireLegacyJobsTest(unittest.TestCase):
    def test_unloads_loaded_job_and_removes_legacy_plist(self) -> None:
        calls: list[tuple[tuple[str, ...], bool]] = []

        def runner(
            *args: str,
            check: bool = True,
        ) -> subprocess.CompletedProcess[str]:
            calls.append((args, check))
            return subprocess.CompletedProcess(args, 0, "", "")

        with tempfile.TemporaryDirectory() as directory:
            agents_dir = Path(directory)
            legacy_path = installer.plist_path(
                installer.LEGACY_LABELS[0],
                agents_dir=agents_dir,
            )
            legacy_path.write_text("legacy", encoding="utf-8")

            installer.retire_legacy_jobs(
                agents_dir=agents_dir,
                runner=runner,
                uid=501,
            )

            self.assertFalse(legacy_path.exists())

        target = "gui/501/com.christian.codex.local-project-catalog"
        self.assertEqual(
            calls,
            [
                (("print", target), False),
                (("bootout", target), True),
            ],
        )

    def test_removes_stale_plist_when_job_is_not_loaded(self) -> None:
        calls: list[tuple[tuple[str, ...], bool]] = []

        def runner(
            *args: str,
            check: bool = True,
        ) -> subprocess.CompletedProcess[str]:
            calls.append((args, check))
            return subprocess.CompletedProcess(args, 1, "", "")

        with tempfile.TemporaryDirectory() as directory:
            agents_dir = Path(directory)
            legacy_path = installer.plist_path(
                installer.LEGACY_LABELS[0],
                agents_dir=agents_dir,
            )
            legacy_path.write_text("legacy", encoding="utf-8")

            installer.retire_legacy_jobs(
                agents_dir=agents_dir,
                runner=runner,
                uid=501,
            )

            self.assertFalse(legacy_path.exists())

        target = "gui/501/com.christian.codex.local-project-catalog"
        self.assertEqual(calls, [(("print", target), False)])


if __name__ == "__main__":
    unittest.main()
