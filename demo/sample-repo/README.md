# Demo Sample Repository

A synthetic multi-language repository for RepoAtlas demos.

## Structure

- `python-service/` — FastAPI app with user and order services
- `node-service/` — Express API for products
- `shared/` — Shared Python modules with an intentional circular dependency

## Intentional Features

- FastAPI routes: `/health`, `/users`, `/users/{id}`, `/orders`
- Express routes: `/health`, `/api/products`, `/api/products/:id`, `/api/products/search`
- Circular dependency: `shared/utils.py` ↔ `shared/orders.py`
- Cross-module imports between python-service and shared

## Scan Command

From the repo-atlas root:

```bash
make demo
```

Or manually:

```bash
curl -X POST http://localhost:8000/api/projects/scan \
  -H "Content-Type: application/json" \
  -d '{"path": "demo/sample-repo", "name": "Demo Sample Repo"}'
```
