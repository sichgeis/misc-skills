#!/usr/bin/env python3
"""Print a compact, text-only summary of an Excalidraw scene."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def load_scene(path: str) -> dict[str, Any]:
    try:
        text = Path(path).read_text(encoding="utf-8")
        scene = json.loads(text)
    except FileNotFoundError as exc:
        raise SystemExit(f"File not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid Excalidraw JSON: {exc}") from exc

    if not isinstance(scene, dict):
        raise SystemExit("Scene must be a JSON object.")
    return scene


def active_elements(scene: dict[str, Any]) -> list[dict[str, Any]]:
    elements = scene.get("elements")
    if not isinstance(elements, list):
        raise SystemExit("Scene does not contain an elements list.")
    return [element for element in elements if isinstance(element, dict) and not element.get("isDeleted")]


def clean_text(value: object) -> str:
    if not isinstance(value, str):
        return ""
    return " / ".join(part.strip() for part in value.splitlines() if part.strip())


def label_maps(elements: list[dict[str, Any]]) -> tuple[dict[str, str], dict[str, list[str]]]:
    labels_by_container: dict[str, list[str]] = defaultdict(list)
    all_text: list[str] = []

    for element in elements:
        if element.get("type") != "text":
            continue
        text = clean_text(element.get("text") or element.get("originalText"))
        if not text:
            continue
        all_text.append(text)
        container_id = element.get("containerId")
        if isinstance(container_id, str):
            labels_by_container[container_id].append(text)

    primary_labels = {
        container_id: " | ".join(labels)
        for container_id, labels in labels_by_container.items()
    }
    primary_labels["__all_text__"] = "\n".join(all_text)
    return primary_labels, labels_by_container


def element_label(element_id: object, labels: dict[str, str]) -> str:
    if isinstance(element_id, str) and labels.get(element_id):
        return labels[element_id]
    if isinstance(element_id, str):
        return f"element:{element_id}"
    return "unbound"


def arrow_relationships(elements: list[dict[str, Any]], labels: dict[str, str]) -> list[str]:
    relationships: list[str] = []
    for element in elements:
        if element.get("type") != "arrow":
            continue

        start_binding = element.get("startBinding")
        end_binding = element.get("endBinding")
        start_id = start_binding.get("elementId") if isinstance(start_binding, dict) else None
        end_id = end_binding.get("elementId") if isinstance(end_binding, dict) else None

        source = element_label(start_id, labels)
        target = element_label(end_id, labels)
        edge_label = labels.get(str(element.get("id")), "")
        if edge_label:
            relationships.append(f"{source} -> {target} ({edge_label})")
        else:
            relationships.append(f"{source} -> {target}")
    return relationships


def summarize(path: str) -> str:
    scene = load_scene(path)
    elements = active_elements(scene)
    counts = Counter(str(element.get("type", "unknown")) for element in elements)
    labels, _labels_by_container = label_maps(elements)
    all_text = labels.pop("__all_text__", "")
    relationships = arrow_relationships(elements, labels)

    lines = [f"File: {path}", f"Scene type: {scene.get('type', 'unknown')}", f"Elements: {len(elements)}"]
    if counts:
        count_text = ", ".join(f"{name}={count}" for name, count in sorted(counts.items()))
        lines.append(f"Element counts: {count_text}")

    if all_text:
        lines.append("")
        lines.append("Text labels:")
        for text in all_text.splitlines():
            lines.append(f"- {text}")

    if relationships:
        lines.append("")
        lines.append("Relationships:")
        for relationship in relationships:
            lines.append(f"- {relationship}")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("diagram", help="Path to .excalidraw or .excalidraw.json file.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    sys.stdout.write(summarize(args.diagram))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
