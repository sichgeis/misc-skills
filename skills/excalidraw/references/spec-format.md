# Compact Excalidraw Spec

Use this compact JSON format as the input to `scripts/create_excalidraw.py`.

## Schema

```json
{
  "title": "Optional diagram title",
  "direction": "LR",
  "nodes": [
    {
      "id": "stable-node-id",
      "label": "Visible label",
      "type": "rectangle"
    }
  ],
  "edges": [
    {
      "from": "source-node-id",
      "to": "target-node-id",
      "label": "Optional edge label"
    }
  ]
}
```

## Fields

- `title`: optional string rendered above the diagram.
- `direction`: `LR` for left-to-right, `TB` for top-to-bottom. Defaults to `LR`.
- `nodes`: required list of diagram nodes.
- `nodes[].id`: required stable ASCII identifier. Edge endpoints refer to this value.
- `nodes[].label`: required visible label. Use `\n` for intentional line breaks.
- `nodes[].type`: optional shape type: `rectangle`, `diamond`, or `ellipse`. Defaults to `rectangle`.
- `edges`: optional list of arrows.
- `edges[].from` / `edges[].to`: required node ids.
- `edges[].label`: optional visible arrow label.

## Example: Auth Flow

```json
{
  "title": "Authentication Flow",
  "direction": "TB",
  "nodes": [
    {"id": "login", "label": "User submits\ncredentials"},
    {"id": "validate", "label": "Credentials valid?", "type": "diamond"},
    {"id": "token", "label": "Issue session token"},
    {"id": "reject", "label": "Show login error", "type": "ellipse"}
  ],
  "edges": [
    {"from": "login", "to": "validate"},
    {"from": "validate", "to": "token", "label": "yes"},
    {"from": "validate", "to": "reject", "label": "no"}
  ]
}
```

## Example: Architecture

```json
{
  "title": "Checkout Architecture",
  "direction": "LR",
  "nodes": [
    {"id": "web", "label": "Web app"},
    {"id": "api", "label": "Checkout API"},
    {"id": "payments", "label": "Payment provider"},
    {"id": "db", "label": "Orders DB", "type": "ellipse"}
  ],
  "edges": [
    {"from": "web", "to": "api", "label": "submit cart"},
    {"from": "api", "to": "payments", "label": "authorize"},
    {"from": "api", "to": "db", "label": "persist order"}
  ]
}
```
