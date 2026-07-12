# RepoAtlas API Reference

Base URL: `http://localhost:8000`

## Health

### `GET /health`

Returns service status.

```json
{ "status": "ok", "service": "repo-atlas" }
```

---

## Projects

### `POST /api/projects/scan`

Scan a local repository and persist results.

**Request body:**

```json
{
  "path": "demo/sample-repo",
  "name": "Optional Display Name"
}
```

**Response:** `ProjectDetail` object with overview stats and top risky files.

**Errors:**
- `404` — Path does not exist
- `400` — Path is not a directory
- `500` — Scan failure

---

### `GET /api/projects`

List all scanned projects (most recently updated first).

**Response:** Array of `ProjectSummary`.

---

### `GET /api/projects/{project_id}`

Get project details including languages and top risky files.

---

### `GET /api/projects/{project_id}/graph`

Get dependency graph for visualization.

**Response:**

```json
{
  "nodes": [
    {
      "id": "shared/utils.py",
      "label": "utils.py",
      "language": "python",
      "risk_score": 42.5,
      "blast_radius": 3.0,
      "is_entry_point": false
    }
  ],
  "edges": [
    {
      "id": "e0",
      "source": "shared/utils.py",
      "target": "shared/models.py",
      "label": "from shared.models import User"
    }
  ],
  "circular_dependencies": [
    { "cycle": ["shared/utils.py", "shared/orders.py", "shared/utils.py"] }
  ]
}
```

---

### `GET /api/projects/{project_id}/files`

List all scanned files with metadata.

---

### `GET /api/projects/{project_id}/endpoints`

List discovered API endpoints (FastAPI, Flask, Express).

---

### `GET /api/projects/{project_id}/hotspots`

List files ranked by risk score (descending).

---

## Schema Reference

### ProjectSummary

| Field | Type | Description |
|-------|------|-------------|
| id | int | Project ID |
| name | string | Display name |
| path | string | Absolute scan path |
| file_count | int | Files scanned |
| endpoint_count | int | APIs discovered |
| dependency_count | int | Internal import edges |
| circular_dependency_count | int | Detected cycles |

### HotspotItem

| Field | Type | Description |
|-------|------|-------------|
| file_path | string | Relative file path |
| risk_score | float | 0–100 composite score |
| risk_explanation | string | Plain-English summary |
| blast_radius | float | Transitive dependent count |

Interactive API docs available at `/docs` when the backend is running.
