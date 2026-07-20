#!/usr/bin/env python3
"""Discover and search the local Git project catalog."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    import tomllib
except ImportError:  # pragma: no cover - supported hosts normally ship modern Python.
    tomllib = None


DEFAULT_ROOTS = {
    "work": Path("/Users/christian/hypatos"),
    "other": Path("/Users/christian/projects"),
}

SKIP_DIRS = {
    ".cache",
    ".direnv",
    ".idea",
    ".mypy_cache",
    ".next",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    ".vscode",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "target",
    "venv",
    "worktrees",
    ".worktrees",
    "symphony-workspaces",
}

README_NAMES = (
    "README.md",
    "README.rst",
    "README.txt",
    "README",
)

STATE_HOME_ENV = "LOCAL_PROJECTS_HOME"
STATE_DIR_NAME = "local-projects"
CATALOG_NAME = "local-projects.json"


def state_home(
    environ: dict[str, str] | None = None,
    home: Path | None = None,
) -> Path:
    env = os.environ if environ is None else environ
    if env.get(STATE_HOME_ENV):
        return Path(env[STATE_HOME_ENV]).expanduser()
    if env.get("XDG_STATE_HOME"):
        return Path(env["XDG_STATE_HOME"]).expanduser() / STATE_DIR_NAME
    base_home = Path.home() if home is None else home
    return base_home / ".local" / "state" / STATE_DIR_NAME


def legacy_codex_home(
    environ: dict[str, str] | None = None,
    home: Path | None = None,
) -> Path:
    env = os.environ if environ is None else environ
    base_home = Path.home() if home is None else home
    return Path(env.get("CODEX_HOME", base_home / ".codex")).expanduser()


def default_catalog_path(
    environ: dict[str, str] | None = None,
    home: Path | None = None,
) -> Path:
    return state_home(environ=environ, home=home) / CATALOG_NAME


def legacy_catalog_path(
    environ: dict[str, str] | None = None,
    home: Path | None = None,
) -> Path:
    return legacy_codex_home(environ=environ, home=home) / CATALOG_NAME


def catalog_for_read(
    primary: Path,
    *,
    allow_legacy: bool,
    environ: dict[str, str] | None = None,
    home: Path | None = None,
) -> Path:
    if primary.exists() or not allow_legacy:
        return primary
    legacy = legacy_catalog_path(environ=environ, home=home)
    return legacy if legacy.exists() else primary


def run_git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
        timeout=8,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def clean_text(value: str, limit: int = 240) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"[`*_>#\[\]]", " ", value)
    value = re.sub(r"\s+", " ", value).strip(" -:")
    return value[:limit].rstrip()


def package_description(repo: Path) -> str:
    pyproject = repo / "pyproject.toml"
    if tomllib and pyproject.is_file():
        try:
            data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
            project = data.get("project", {})
            poetry = data.get("tool", {}).get("poetry", {})
            description = project.get("description") or poetry.get("description")
            if isinstance(description, str) and description.strip():
                return clean_text(description)
        except (OSError, ValueError):
            pass

    package_json = repo / "package.json"
    if package_json.is_file():
        try:
            data = json.loads(package_json.read_text(encoding="utf-8"))
            description = data.get("description")
            if isinstance(description, str) and description.strip():
                return clean_text(description)
        except (OSError, json.JSONDecodeError):
            pass

    cargo = repo / "Cargo.toml"
    if tomllib and cargo.is_file():
        try:
            data = tomllib.loads(cargo.read_text(encoding="utf-8"))
            description = data.get("package", {}).get("description")
            if isinstance(description, str) and description.strip():
                return clean_text(description)
        except (OSError, ValueError):
            pass

    return ""


def readme_description(repo: Path) -> str:
    for name in README_NAMES:
        path = repo / name
        if not path.is_file():
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue

        paragraph: list[str] = []
        in_fence = False
        for raw in lines[:160]:
            line = raw.strip()
            if line.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence or not line:
                if paragraph:
                    text = clean_text(" ".join(paragraph))
                    if len(text) >= 20:
                        return text
                    paragraph = []
                continue
            if line.startswith(("#", "![", "[![", "<img", "<div", "---", "===")):
                continue
            paragraph.append(line)
        if paragraph:
            return clean_text(" ".join(paragraph))
    return ""


def detect_languages(repo: Path) -> list[str]:
    markers = (
        ("Python", ("pyproject.toml", "setup.py", "requirements.txt")),
        ("TypeScript/JavaScript", ("package.json",)),
        ("Java/Kotlin", ("build.gradle", "build.gradle.kts", "pom.xml")),
        ("Go", ("go.mod",)),
        ("Rust", ("Cargo.toml",)),
        ("Ruby", ("Gemfile",)),
        ("Swift", ("Package.swift",)),
        ("Infrastructure", ("Chart.yaml", "terraform.tf", "terragrunt.hcl")),
    )
    found = [
        language
        for language, filenames in markers
        if any((repo / filename).exists() for filename in filenames)
    ]
    return found


def remote_name(remote: str) -> str:
    if not remote:
        return ""
    tail = remote.rstrip("/").rsplit("/", 1)[-1].rsplit(":", 1)[-1]
    return re.sub(r"\.git$", "", tail)


def aliases_for(name: str, remote: str) -> list[str]:
    values = {
        name,
        name.lower(),
        name.replace("-", " "),
        name.replace("_", " "),
        remote_name(remote),
    }
    return sorted(value for value in values if value)


def discover(roots: dict[str, Path]) -> list[dict[str, Any]]:
    projects: list[dict[str, Any]] = []
    seen: set[Path] = set()

    for category, root in roots.items():
        root = root.expanduser().resolve()
        if not root.is_dir():
            continue

        for current, dirs, files in os.walk(root):
            current_path = Path(current)
            has_git_marker = ".git" in dirs or ".git" in files
            dirs[:] = sorted(
                directory
                for directory in dirs
                if directory not in SKIP_DIRS and not directory.startswith(".")
            )

            if not has_git_marker:
                continue

            repo = current_path.resolve()
            if repo in seen:
                dirs[:] = []
                continue
            seen.add(repo)
            dirs[:] = []

            remote = run_git(repo, "remote", "get-url", "origin")
            timestamp = run_git(repo, "log", "-1", "--format=%cI")
            subject = run_git(repo, "log", "-1", "--format=%s")
            branch = run_git(repo, "branch", "--show-current")
            description = package_description(repo) or readme_description(repo)

            projects.append(
                {
                    "name": repo.name,
                    "path": str(repo),
                    "category": category,
                    "summary": description,
                    "aliases": aliases_for(repo.name, remote),
                    "languages": detect_languages(repo),
                    "remote": remote,
                    "branch": branch,
                    "lastCommitAt": timestamp,
                    "lastCommitSubject": subject,
                }
            )

    return sorted(projects, key=lambda item: (item["category"], item["name"].lower()))


def parse_roots(values: list[str]) -> dict[str, Path]:
    if not values:
        return DEFAULT_ROOTS.copy()
    roots: dict[str, Path] = {}
    for value in values:
        if "=" not in value:
            raise SystemExit(f"Invalid --root {value!r}; expected CATEGORY=PATH")
        category, path = value.split("=", 1)
        roots[category.strip()] = Path(path).expanduser()
    return roots


def write_catalog(
    projects: list[dict[str, Any]],
    roots: dict[str, Path],
    json_path: Path,
    markdown_path: Path,
) -> None:
    generated_at = dt.datetime.now(dt.timezone.utc).isoformat()
    payload = {
        "generatedAt": generated_at,
        "roots": {name: str(path.expanduser()) for name, path in roots.items()},
        "projects": projects,
    }

    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Local Projects",
        "",
        f"Generated: {generated_at}",
        "",
    ]
    for category in roots:
        items = [project for project in projects if project["category"] == category]
        lines.extend((f"## {category.title()}", ""))
        for project in items:
            summary = project["summary"] or "No summary available."
            languages = ", ".join(project["languages"])
            details = f" — {languages}" if languages else ""
            lines.append(
                f"- **{project['name']}** — `{project['path']}`{details}  \n"
                f"  {summary}"
            )
        lines.append("")
    markdown_path.write_text("\n".join(lines), encoding="utf-8")


def load_projects(json_path: Path) -> list[dict[str, Any]]:
    try:
        return json.loads(json_path.read_text(encoding="utf-8"))["projects"]
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Cannot read catalog {json_path}: {exc}") from exc


def searchable_text(project: dict[str, Any]) -> str:
    fields = [
        project["name"],
        project["path"],
        project.get("summary", ""),
        project.get("remote", ""),
        " ".join(project.get("aliases", [])),
        " ".join(project.get("languages", [])),
    ]
    return " ".join(fields).lower()


def match_score(project: dict[str, Any], query: str) -> int:
    normalized = query.lower().strip()
    name = project["name"].lower()
    aliases = [alias.lower() for alias in project.get("aliases", [])]
    text = searchable_text(project)
    tokens = re.findall(r"[a-z0-9]+", normalized)

    score = 0
    if normalized == name or normalized in aliases:
        score += 100
    if normalized in name:
        score += 50
    if normalized in text:
        score += 25
    score += sum(8 for token in tokens if token in name)
    score += sum(3 for token in tokens if token in text)
    if tokens and all(token in text for token in tokens):
        score += 20
    return score


def display(project: dict[str, Any]) -> None:
    print(f"{project['name']} [{project['category']}]")
    print(f"  path: {project['path']}")
    if project.get("summary"):
        print(f"  summary: {project['summary']}")
    if project.get("remote"):
        print(f"  remote: {project['remote']}")
    if project.get("languages"):
        print(f"  languages: {', '.join(project['languages'])}")
    if project.get("lastCommitAt"):
        print(
            f"  last commit: {project['lastCommitAt']} "
            f"{project.get('lastCommitSubject', '')}".rstrip()
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        action="append",
        default=[],
        metavar="CATEGORY=PATH",
        help="Project root; repeat for multiple categories",
    )
    parser.add_argument(
        "--json",
        type=Path,
        default=None,
        help=(
            f"JSON catalog path; defaults to ${STATE_HOME_ENV}/local-projects.json "
            "or the platform-neutral user state directory"
        ),
    )
    parser.add_argument(
        "--markdown",
        type=Path,
        default=None,
        help="Markdown catalog path; defaults beside the JSON catalog",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("refresh", help="Scan roots and regenerate the catalog")
    subparsers.add_parser("list", help="List cataloged projects")
    find_parser = subparsers.add_parser("find", help="Find projects matching a query")
    find_parser.add_argument("query")
    find_parser.add_argument(
        "--refresh",
        action="store_true",
        help="Refresh before searching",
    )
    args = parser.parse_args()

    explicit_json = args.json is not None
    json_path = args.json or default_catalog_path()
    markdown_path = args.markdown or json_path.with_suffix(".md")
    allow_legacy = not explicit_json and not os.environ.get(STATE_HOME_ENV)
    read_path = catalog_for_read(json_path, allow_legacy=allow_legacy)

    roots = parse_roots(args.root)
    if args.command == "refresh":
        projects = discover(roots)
        write_catalog(projects, roots, json_path, markdown_path)
        print(f"Cataloged {len(projects)} projects in {json_path}")
        return 0

    if args.command == "find" and (args.refresh or not read_path.exists()):
        projects = discover(roots)
        write_catalog(projects, roots, json_path, markdown_path)
    else:
        projects = load_projects(read_path)

    if args.command == "list":
        for project in projects:
            print(f"{project['category']:>5}  {project['name']:<40} {project['path']}")
        return 0

    ranked = sorted(
        (
            (match_score(project, args.query), project)
            for project in projects
        ),
        key=lambda item: (-item[0], item[1]["name"].lower()),
    )
    matches = [(score, project) for score, project in ranked if score > 0][:5]
    if not matches:
        print(f"No project matched {args.query!r}. Try refreshing the catalog.")
        return 1

    for index, (score, project) in enumerate(matches):
        if index:
            print()
        print(f"match score: {score}")
        display(project)
    return 0


if __name__ == "__main__":
    sys.exit(main())
