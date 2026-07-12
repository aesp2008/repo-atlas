.PHONY: install dev test demo clean backend frontend docker-up docker-down

install:
	cd backend && (command -v python3.10 >/dev/null && python3.10 -m venv .venv || python3 -m venv .venv) && . .venv/bin/activate && pip install -e ".[dev]"
	cd frontend && npm install

dev:
	@echo "Starting backend and frontend..."
	@make -j2 backend frontend

backend:
	cd backend && . .venv/bin/activate && cd .. && PYTHONPATH=backend backend/.venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend:
	cd frontend && npm run dev

test:
	cd backend && . .venv/bin/activate && pytest -v
	cd frontend && npm test

demo:
	@echo "Scanning demo repository..."
	@curl -s -X POST http://localhost:8000/api/projects/scan \
		-H "Content-Type: application/json" \
		-d '{"path": "demo/sample-repo", "name": "Demo Sample Repo"}' | python3 -m json.tool

clean:
	rm -rf backend/.venv backend/data backend/.pytest_cache backend/**/__pycache__
	rm -rf frontend/node_modules frontend/.next
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

docker-up:
	docker compose up --build

docker-down:
	docker compose down
