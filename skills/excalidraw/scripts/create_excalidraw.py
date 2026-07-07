#!/usr/bin/env python3
"""Create an Excalidraw scene from a compact JSON diagram spec."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import defaultdict, deque
from pathlib import Path
from textwrap import wrap
from typing import Any


SHAPE_TYPES = {"rectangle", "diamond", "ellipse"}
DIRECTION_ALIASES = {
    "LR": "LR",
    "LEFT-RIGHT": "LR",
    "LEFT_TO_RIGHT": "LR",
    "LEFT-TO-RIGHT": "LR",
    "RIGHT": "LR",
    "TB": "TB",
    "TOP-BOTTOM": "TB",
    "TOP_TO_BOTTOM": "TB",
    "TOP-TO-BOTTOM": "TB",
    "DOWN": "TB",
}


def stable_digest(*parts: object) -> str:
    text = "::".join(str(part) for part in parts)
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def stable_id(prefix: str, *parts: object) -> str:
    return f"{prefix}_{stable_digest(*parts)[:16]}"


def stable_int(*parts: object) -> int:
    value = int(stable_digest(*parts)[:8], 16)
    return value or 1


def load_spec(path: str) -> dict[str, Any]:
    if path == "-":
        data = sys.stdin.read()
    else:
        data = Path(path).read_text(encoding="utf-8")

    try:
        spec = json.loads(data)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON spec: {exc}") from exc

    if not isinstance(spec, dict):
        raise SystemExit("Spec must be a JSON object.")
    return spec


def normalize_direction(value: object) -> str:
    direction = str(value or "LR").strip().upper()
    if direction not in DIRECTION_ALIASES:
        raise SystemExit("direction must be LR or TB.")
    return DIRECTION_ALIASES[direction]


def require_text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SystemExit(f"{field} must be a non-empty string.")
    return value.strip()


def normalize_nodes(raw_nodes: object) -> list[dict[str, str]]:
    if not isinstance(raw_nodes, list) or not raw_nodes:
        raise SystemExit("nodes must be a non-empty list.")

    seen: set[str] = set()
    nodes: list[dict[str, str]] = []
    for index, raw_node in enumerate(raw_nodes):
        if not isinstance(raw_node, dict):
            raise SystemExit(f"nodes[{index}] must be an object.")
        node_id = require_text(raw_node.get("id"), f"nodes[{index}].id")
        if node_id in seen:
            raise SystemExit(f"Duplicate node id: {node_id}")
        seen.add(node_id)

        shape_type = str(raw_node.get("type", "rectangle")).strip().lower()
        if shape_type not in SHAPE_TYPES:
            raise SystemExit(
                f"nodes[{index}].type must be one of: {', '.join(sorted(SHAPE_TYPES))}."
            )

        nodes.append(
            {
                "id": node_id,
                "label": require_text(raw_node.get("label"), f"nodes[{index}].label"),
                "type": shape_type,
            }
        )
    return nodes


def normalize_edges(raw_edges: object, node_ids: set[str]) -> list[dict[str, str]]:
    if raw_edges is None:
        return []
    if not isinstance(raw_edges, list):
        raise SystemExit("edges must be a list.")

    edges: list[dict[str, str]] = []
    for index, raw_edge in enumerate(raw_edges):
        if not isinstance(raw_edge, dict):
            raise SystemExit(f"edges[{index}] must be an object.")
        source = require_text(raw_edge.get("from"), f"edges[{index}].from")
        target = require_text(raw_edge.get("to"), f"edges[{index}].to")
        if source not in node_ids:
            raise SystemExit(f"edges[{index}].from references unknown node: {source}")
        if target not in node_ids:
            raise SystemExit(f"edges[{index}].to references unknown node: {target}")
        edge: dict[str, str] = {"from": source, "to": target}
        label = raw_edge.get("label")
        if isinstance(label, str) and label.strip():
            edge["label"] = label.strip()
        edges.append(edge)
    return edges


def wrapped_label(label: str) -> str:
    lines: list[str] = []
    for line in label.splitlines() or [label]:
        wrapped = wrap(line, width=24, break_long_words=False) or [line]
        lines.extend(wrapped)
    return "\n".join(lines)


def text_size(text: str, font_size: int = 20) -> tuple[float, float]:
    lines = text.splitlines() or [text]
    width = max(len(line) for line in lines) * font_size * 0.56
    height = len(lines) * font_size * 1.25
    return width, height


def node_size(label: str, shape_type: str) -> tuple[float, float]:
    text_width, text_height = text_size(label)
    width = min(max(text_width + 56, 160), 360)
    height = max(text_height + 44, 84)
    if shape_type == "diamond":
        width = max(width, 184)
        height = max(height, 128)
    if shape_type == "ellipse":
        width = max(width, 172)
        height = max(height, 96)
    return round(width, 2), round(height, 2)


def compute_levels(nodes: list[dict[str, str]], edges: list[dict[str, str]]) -> dict[str, int]:
    order = {node["id"]: index for index, node in enumerate(nodes)}
    incoming_count: dict[str, int] = {node["id"]: 0 for node in nodes}
    outgoing: dict[str, list[str]] = defaultdict(list)
    for edge in edges:
        outgoing[edge["from"]].append(edge["to"])
        incoming_count[edge["to"]] += 1

    queue = deque(sorted((node_id for node_id, count in incoming_count.items() if count == 0), key=order.get))
    levels = {node["id"]: 0 for node in nodes}
    visited: set[str] = set()

    while queue:
        node_id = queue.popleft()
        visited.add(node_id)
        for target in sorted(outgoing[node_id], key=order.get):
            levels[target] = max(levels[target], levels[node_id] + 1)
            incoming_count[target] -= 1
            if incoming_count[target] == 0:
                queue.append(target)

    if len(visited) != len(nodes):
        last_level = max(levels.values(), default=0)
        for node in nodes:
            if node["id"] not in visited:
                last_level += 1
                levels[node["id"]] = last_level

    return levels


def layout_nodes(
    nodes: list[dict[str, str]],
    edges: list[dict[str, str]],
    direction: str,
) -> dict[str, dict[str, float]]:
    levels = compute_levels(nodes, edges)
    by_level: dict[int, list[dict[str, str]]] = defaultdict(list)
    for node in nodes:
        by_level[levels[node["id"]]].append(node)

    sizes = {node["id"]: node_size(node["label"], node["type"]) for node in nodes}
    layout: dict[str, dict[str, float]] = {}
    primary_gap = 160
    cross_gap = 80
    level_offsets: dict[int, float] = {}

    cursor = 0.0
    for level in sorted(by_level):
        group = by_level[level]
        level_offsets[level] = cursor
        if direction == "LR":
            cursor += max(sizes[node["id"]][0] for node in group) + primary_gap
        else:
            cursor += max(sizes[node["id"]][1] for node in group) + primary_gap

    for level in sorted(by_level):
        group = by_level[level]

        if direction == "LR":
            total_height = sum(sizes[node["id"]][1] for node in group) + cross_gap * (len(group) - 1)
            row_cursor = -total_height / 2
            x = level_offsets[level]
            for node in group:
                width, height = sizes[node["id"]]
                layout[node["id"]] = {"x": x, "y": row_cursor, "width": width, "height": height}
                row_cursor += height + cross_gap
        else:
            total_width = sum(sizes[node["id"]][0] for node in group) + primary_gap * (len(group) - 1)
            column_cursor = -total_width / 2
            y = level_offsets[level]
            for node in group:
                width, height = sizes[node["id"]]
                layout[node["id"]] = {"x": column_cursor, "y": y, "width": width, "height": height}
                column_cursor += width + primary_gap

    min_x = min(item["x"] for item in layout.values())
    min_y = min(item["y"] for item in layout.values())
    for item in layout.values():
        item["x"] = round(item["x"] - min_x + 80, 2)
        item["y"] = round(item["y"] - min_y + 120, 2)
    return layout


def base_element(element_id: str, element_type: str, x: float, y: float, width: float, height: float) -> dict[str, Any]:
    return {
        "id": element_id,
        "type": element_type,
        "x": round(x, 2),
        "y": round(y, 2),
        "width": round(width, 2),
        "height": round(height, 2),
        "angle": 0,
        "strokeColor": "#1e1e1e",
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "seed": stable_int("seed", element_id),
        "version": 1,
        "versionNonce": stable_int("version", element_id),
        "isDeleted": False,
        "boundElements": None,
        "updated": 1,
        "link": None,
        "locked": False,
    }


def make_text(
    element_id: str,
    text: str,
    x: float,
    y: float,
    width: float,
    height: float,
    *,
    font_size: int = 20,
    text_align: str = "center",
    vertical_align: str = "middle",
    container_id: str | None = None,
) -> dict[str, Any]:
    element = base_element(element_id, "text", x, y, width, height)
    element.update(
        {
            "strokeColor": "#1e1e1e",
            "backgroundColor": "transparent",
            "text": text,
            "fontSize": font_size,
            "fontFamily": 1,
            "textAlign": text_align,
            "verticalAlign": vertical_align,
            "containerId": container_id,
            "originalText": text,
            "autoResize": False,
            "lineHeight": 1.25,
        }
    )
    return element


def shape_fill(shape_type: str) -> str:
    return {
        "rectangle": "#e7f5ff",
        "diamond": "#fff4e6",
        "ellipse": "#ebfbee",
    }[shape_type]


def make_shape(node: dict[str, str], placement: dict[str, float], text_id: str) -> dict[str, Any]:
    shape_id = stable_id("node", node["id"])
    element = base_element(
        shape_id,
        node["type"],
        placement["x"],
        placement["y"],
        placement["width"],
        placement["height"],
    )
    element["backgroundColor"] = shape_fill(node["type"])
    element["boundElements"] = [{"type": "text", "id": text_id}]
    if node["type"] == "rectangle":
        element["roundness"] = {"type": 3}
    return element


def center(placement: dict[str, float]) -> tuple[float, float]:
    return placement["x"] + placement["width"] / 2, placement["y"] + placement["height"] / 2


def boundary_points(
    source: dict[str, float],
    target: dict[str, float],
) -> tuple[tuple[float, float], tuple[float, float]]:
    source_center = center(source)
    target_center = center(target)
    dx = target_center[0] - source_center[0]
    dy = target_center[1] - source_center[1]

    if abs(dx) >= abs(dy):
        source_x = source["x"] + (source["width"] if dx >= 0 else 0)
        source_y = source_center[1]
        target_x = target["x"] if dx >= 0 else target["x"] + target["width"]
        target_y = target_center[1]
    else:
        source_x = source_center[0]
        source_y = source["y"] + (source["height"] if dy >= 0 else 0)
        target_x = target_center[0]
        target_y = target["y"] if dy >= 0 else target["y"] + target["height"]

    return (round(source_x, 2), round(source_y, 2)), (round(target_x, 2), round(target_y, 2))


def make_arrow(
    edge: dict[str, str],
    index: int,
    layout: dict[str, dict[str, float]],
    shape_ids: dict[str, str],
    label_id: str | None,
) -> dict[str, Any]:
    source_point, target_point = boundary_points(layout[edge["from"]], layout[edge["to"]])
    width = target_point[0] - source_point[0]
    height = target_point[1] - source_point[1]
    arrow_id = stable_id("edge", edge["from"], edge["to"], index, edge.get("label", ""))
    element = base_element(arrow_id, "arrow", source_point[0], source_point[1], width, height)
    element.update(
        {
            "backgroundColor": "transparent",
            "points": [[0, 0], [round(width, 2), round(height, 2)]],
            "lastCommittedPoint": None,
            "startBinding": {
                "elementId": shape_ids[edge["from"]],
                "focus": 0,
                "gap": 8,
            },
            "endBinding": {
                "elementId": shape_ids[edge["to"]],
                "focus": 0,
                "gap": 8,
            },
            "startArrowhead": None,
            "endArrowhead": "arrow",
        }
    )
    if label_id:
        element["boundElements"] = [{"type": "text", "id": label_id}]
    return element


def make_scene(spec: dict[str, Any]) -> dict[str, Any]:
    direction = normalize_direction(spec.get("direction", "LR"))
    nodes = normalize_nodes(spec.get("nodes"))
    node_ids = {node["id"] for node in nodes}
    edges = normalize_edges(spec.get("edges", []), node_ids)
    title = spec.get("title")
    if title is not None and not isinstance(title, str):
        raise SystemExit("title must be a string when provided.")

    for node in nodes:
        node["label"] = wrapped_label(node["label"])

    layout = layout_nodes(nodes, edges, direction)
    elements: list[dict[str, Any]] = []
    shape_ids = {node["id"]: stable_id("node", node["id"]) for node in nodes}
    text_ids = {node["id"]: stable_id("text", node["id"], node["label"]) for node in nodes}
    shape_elements: dict[str, dict[str, Any]] = {}

    if isinstance(title, str) and title.strip():
        title_text = title.strip()
        title_width, title_height = text_size(title_text, font_size=28)
        min_x = min(item["x"] for item in layout.values())
        max_x = max(item["x"] + item["width"] for item in layout.values())
        elements.append(
            make_text(
                stable_id("title", title_text),
                title_text,
                min_x,
                32,
                max(title_width + 16, max_x - min_x),
                title_height + 8,
                font_size=28,
            )
        )

    for node in nodes:
        placement = layout[node["id"]]
        shape = make_shape(node, placement, text_ids[node["id"]])
        shape_elements[node["id"]] = shape
        elements.append(shape)
        text_width, text_height = text_size(node["label"])
        elements.append(
            make_text(
                text_ids[node["id"]],
                node["label"],
                placement["x"] + 16,
                placement["y"] + (placement["height"] - text_height) / 2,
                placement["width"] - 32,
                text_height,
                container_id=shape_ids[node["id"]],
            )
        )

    for index, edge in enumerate(edges):
        label_id = stable_id("edge_text", edge["from"], edge["to"], index, edge.get("label", "")) if edge.get("label") else None
        arrow = make_arrow(edge, index, layout, shape_ids, label_id)
        elements.append(arrow)
        for endpoint in ("from", "to"):
            shape = shape_elements[edge[endpoint]]
            if shape["boundElements"] is None:
                shape["boundElements"] = []
            shape["boundElements"].append({"type": "arrow", "id": arrow["id"]})

        if edge.get("label") and label_id:
            source_point, target_point = boundary_points(layout[edge["from"]], layout[edge["to"]])
            mid_x = (source_point[0] + target_point[0]) / 2
            mid_y = (source_point[1] + target_point[1]) / 2
            label_width, label_height = text_size(edge["label"], font_size=16)
            elements.append(
                make_text(
                    label_id,
                    edge["label"],
                    mid_x - label_width / 2,
                    mid_y - label_height - 8,
                    max(label_width, 40),
                    label_height,
                    font_size=16,
                    container_id=arrow["id"],
                )
            )

    return {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {
            "gridSize": None,
            "viewBackgroundColor": "#ffffff",
        },
        "files": {},
    }


def write_scene(scene: dict[str, Any], path: str, compact: bool) -> None:
    output = json.dumps(scene, ensure_ascii=False, separators=(",", ":") if compact else None, indent=None if compact else 2)
    if path == "-":
        sys.stdout.write(output)
        sys.stdout.write("\n")
    else:
        Path(path).write_text(output + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", help="Input compact spec JSON path, or '-' for stdin.")
    parser.add_argument("output", help="Output .excalidraw/.excalidraw.json path, or '-' for stdout.")
    parser.add_argument("--compact", action="store_true", help="Write compact JSON instead of pretty JSON.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    spec = load_spec(args.spec)
    scene = make_scene(spec)
    write_scene(scene, args.output, args.compact)


if __name__ == "__main__":
    main()
