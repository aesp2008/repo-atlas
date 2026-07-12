# RepoAtlas Backend

FastAPI backend for the RepoAtlas developer intelligence platform.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

Run from the `repo-atlas/` root so demo paths resolve correctly:

```bash
cd .. && uvicorn app.main:app --reload --app-dir backend --port 8000
```

## Tests

```bash
pytest -v
```
