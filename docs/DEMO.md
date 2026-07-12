# Demo Guide

RepoAtlas includes a synthetic demo repository at `demo/sample-repo/` designed to showcase all MVP features.

## What's Inside

```
demo/sample-repo/
├── python-service/     # FastAPI app
│   ├── main.py
│   └── services/
│       ├── user_service.py
│       └── order_service.py
├── node-service/       # Express app
│   └── src/
│       ├── server.ts
│       ├── products.ts
│       └── types.ts
└── shared/             # Shared Python modules
    ├── models.py
    ├── utils.py
    └── orders.py       # Circular dependency with utils.py
```

## Intentional Demo Features

| Feature | Location |
|---------|----------|
| FastAPI routes | `python-service/main.py` — `/health`, `/users`, `/orders` |
| Express routes | `node-service/src/server.ts` — `/api/products`, etc. |
| Circular dependency | `shared/utils.py` ↔ `shared/orders.py` |
| Cross-module imports | python-service → shared |
| Entry points | `main.py`, `server.ts` |
| Risk hotspots | Services with multiple imports and logic |

## Running the Demo

### Option 1: UI

1. Start the app: `make dev`
2. Open http://localhost:3000
3. Click **Run Demo**

### Option 2: API

```bash
# From repo-atlas root (with backend running)
make demo
```

Or manually:

```bash
curl -X POST http://localhost:8000/api/projects/scan \
  -H "Content-Type: application/json" \
  -d '{"path": "demo/sample-repo", "name": "Demo Sample Repo"}'
```

> **Note:** The scan path is relative to the backend's working directory. Run the backend from the `repo-atlas/` root for demo paths to resolve correctly.

## Expected Results

After scanning, you should see:

- **~10+ files** across Python and TypeScript
- **2 languages** detected
- **8+ API endpoints** (FastAPI + Express)
- **Multiple dependency edges** between modules
- **At least 1 circular dependency** in the shared package
- **Risk hotspots** in service files with higher complexity

## Exploring Results

1. **Overview cards** — Quick stats at the top
2. **Dependency graph** — Click nodes to inspect files
3. **File explorer** — Browse all scanned files
4. **API endpoints table** — All discovered routes
5. **Hotspots table** — Files ranked by risk
6. **Circular dependencies** — Highlighted cycles
