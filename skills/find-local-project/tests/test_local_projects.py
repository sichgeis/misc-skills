from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from types import ModuleType


SCRIPT = Path(__file__).parents[1] / "scripts" / "local_projects.py"


def load_script() -> ModuleType:
    spec = importlib.util.spec_from_file_location("local_projects", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


projects = load_script()


class CatalogPathTest(unittest.TestCase):
    def test_state_home_prefers_skill_specific_override(self) -> None:
        environ = {
            "LOCAL_PROJECTS_HOME": "/custom/catalog",
            "XDG_STATE_HOME": "/xdg/state",
        }

        self.assertEqual(
            projects.state_home(environ=environ, home=Path("/home/person")),
            Path("/custom/catalog"),
        )

    def test_state_home_uses_xdg_then_neutral_home_default(self) -> None:
        self.assertEqual(
            projects.state_home(
                environ={"XDG_STATE_HOME": "/xdg/state"},
                home=Path("/home/person"),
            ),
            Path("/xdg/state/local-projects"),
        )
        self.assertEqual(
            projects.state_home(environ={}, home=Path("/home/person")),
            Path("/home/person/.local/state/local-projects"),
        )

    def test_read_falls_back_to_legacy_catalog_only_when_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            primary = projects.default_catalog_path(environ={}, home=home)
            legacy = projects.legacy_catalog_path(environ={}, home=home)
            legacy.parent.mkdir(parents=True)
            legacy.write_text("[]", encoding="utf-8")

            self.assertEqual(
                projects.catalog_for_read(
                    primary,
                    allow_legacy=True,
                    environ={},
                    home=home,
                ),
                legacy,
            )
            self.assertEqual(
                projects.catalog_for_read(
                    primary,
                    allow_legacy=False,
                    environ={},
                    home=home,
                ),
                primary,
            )

            primary.parent.mkdir(parents=True)
            primary.write_text("[]", encoding="utf-8")
            self.assertEqual(
                projects.catalog_for_read(
                    primary,
                    allow_legacy=True,
                    environ={},
                    home=home,
                ),
                primary,
            )


if __name__ == "__main__":
    unittest.main()
