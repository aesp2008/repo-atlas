from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.session import get_db
from app.main import app
from app.models.entities import Base


@pytest.fixture()
def client(tmp_path: Path):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # Create mini demo repo
    demo = tmp_path / "demo-repo"
    demo.mkdir()
    (demo / "main.py").write_text(
        '''
from fastapi import FastAPI
app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}
'''
    )
    (demo / "utils.py").write_text("def helper():\n    return 1\n")

    with TestClient(app) as test_client:
        yield test_client, str(demo)

    app.dependency_overrides.clear()


def test_health(client):
    test_client, _ = client
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_scan_and_get_project(client):
    test_client, demo_path = client
    response = test_client.post("/api/projects/scan", json={"path": demo_path, "name": "Test"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test"
    assert data["file_count"] >= 1

    project_id = data["id"]
    detail = test_client.get(f"/api/projects/{project_id}")
    assert detail.status_code == 200

    endpoints = test_client.get(f"/api/projects/{project_id}/endpoints")
    assert endpoints.status_code == 200
    assert any(e["path"] == "/health" for e in endpoints.json())

    graph = test_client.get(f"/api/projects/{project_id}/graph")
    assert graph.status_code == 200
    assert "nodes" in graph.json()

    hotspots = test_client.get(f"/api/projects/{project_id}/hotspots")
    assert hotspots.status_code == 200
