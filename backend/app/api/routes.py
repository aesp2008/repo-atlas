from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import Dependency, Endpoint, FileMetric, FileRecord, Project, ScanRun
from app.schemas.project import (
    EndpointItem,
    FileItem,
    GraphEdge,
    GraphNode,
    GraphResponse,
    HotspotItem,
    ProjectDetail,
    ProjectSummary,
    ScanRequest,
)
from app.services.graph.builder import compute_blast_radius, find_circular_dependencies
from app.services.scan_service import ScanService

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.post("/scan", response_model=ProjectDetail)
def scan_project(payload: ScanRequest, db: Session = Depends(get_db)) -> ProjectDetail:
    service = ScanService(db)
    try:
        project = service.scan_repository(payload.path, payload.name)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except NotADirectoryError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Scan failed: {exc}") from exc

    return _build_project_detail(db, project)


@router.get("", response_model=list[ProjectSummary])
def list_projects(db: Session = Depends(get_db)) -> list[ProjectSummary]:
    projects = db.query(Project).order_by(Project.updated_at.desc()).all()
    return [_build_project_summary(db, p) for p in projects]


@router.get("/{project_id}", response_model=ProjectDetail)
def get_project(project_id: int, db: Session = Depends(get_db)) -> ProjectDetail:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return _build_project_detail(db, project)


@router.get("/{project_id}/graph", response_model=GraphResponse)
def get_graph(project_id: int, db: Session = Depends(get_db)) -> GraphResponse:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    files = db.query(FileRecord).filter(FileRecord.project_id == project_id).all()
    deps = db.query(Dependency).filter(Dependency.project_id == project_id).all()
    metrics = {m.file_path: m for m in db.query(FileMetric).filter(FileMetric.project_id == project_id).all()}

    nodes: dict[str, GraphNode] = {}
    for f in files:
        m = metrics.get(f.relative_path)
        nodes[f.relative_path] = GraphNode(
            id=f.relative_path,
            label=f.relative_path.split("/")[-1],
            language=f.language,
            risk_score=m.risk_score if m else 0.0,
            blast_radius=m.blast_radius if m else 0.0,
            is_entry_point=f.is_entry_point,
        )

    edges: list[GraphEdge] = []
    for i, dep in enumerate(deps):
        nodes.setdefault(
            dep.source_path,
            GraphNode(id=dep.source_path, label=dep.source_path.split("/")[-1], language="unknown"),
        )
        nodes.setdefault(
            dep.target_path,
            GraphNode(id=dep.target_path, label=dep.target_path.split("/")[-1], language="unknown"),
        )
        edges.append(
            GraphEdge(
                id=f"e{i}",
                source=dep.source_path,
                target=dep.target_path,
                label=dep.import_statement[:40],
            )
        )

    edge_tuples = [(d.source_path, d.target_path, d.import_statement) for d in deps]
    cycles = find_circular_dependencies(edge_tuples)

    return GraphResponse(
        nodes=list(nodes.values()),
        edges=edges,
        circular_dependencies=[{"cycle": c} for c in cycles],
    )


@router.get("/{project_id}/files", response_model=list[FileItem])
def get_files(project_id: int, db: Session = Depends(get_db)) -> list[FileItem]:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    files = db.query(FileRecord).filter(FileRecord.project_id == project_id).order_by(FileRecord.relative_path).all()
    return [FileItem.model_validate(f) for f in files]


@router.get("/{project_id}/endpoints", response_model=list[EndpointItem])
def get_endpoints(project_id: int, db: Session = Depends(get_db)) -> list[EndpointItem]:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    endpoints = db.query(Endpoint).filter(Endpoint.project_id == project_id).order_by(Endpoint.path).all()
    return [EndpointItem.model_validate(e) for e in endpoints]


@router.get("/{project_id}/hotspots", response_model=list[HotspotItem])
def get_hotspots(project_id: int, db: Session = Depends(get_db)) -> list[HotspotItem]:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    metrics = (
        db.query(FileMetric)
        .filter(FileMetric.project_id == project_id)
        .order_by(FileMetric.risk_score.desc())
        .all()
    )
    return [HotspotItem.model_validate(m) for m in metrics]


def _build_project_summary(db: Session, project: Project) -> ProjectSummary:
    latest_scan = (
        db.query(ScanRun)
        .filter(ScanRun.project_id == project.id)
        .order_by(ScanRun.started_at.desc())
        .first()
    )
    file_count = db.query(FileRecord).filter(FileRecord.project_id == project.id).count()
    endpoint_count = db.query(Endpoint).filter(Endpoint.project_id == project.id).count()
    dependency_count = db.query(Dependency).filter(Dependency.project_id == project.id).count()

    deps = db.query(Dependency).filter(Dependency.project_id == project.id).all()
    edge_tuples = [(d.source_path, d.target_path, d.import_statement) for d in deps]
    circular_count = len(find_circular_dependencies(edge_tuples))

    from app.schemas.project import ScanRunSummary

    return ProjectSummary(
        id=project.id,
        name=project.name,
        path=project.path,
        created_at=project.created_at,
        updated_at=project.updated_at,
        latest_scan=ScanRunSummary.model_validate(latest_scan) if latest_scan else None,
        file_count=file_count,
        endpoint_count=endpoint_count,
        dependency_count=dependency_count,
        circular_dependency_count=circular_count,
    )


def _build_project_detail(db: Session, project: Project) -> ProjectDetail:
    summary = _build_project_summary(db, project)

    files = db.query(FileRecord).filter(FileRecord.project_id == project.id).all()
    languages = sorted({f.language for f in files})

    metrics = (
        db.query(FileMetric)
        .filter(FileMetric.project_id == project.id)
        .order_by(FileMetric.risk_score.desc())
        .limit(5)
        .all()
    )

    return ProjectDetail(
        **summary.model_dump(),
        languages=languages,
        top_risky_files=[HotspotItem.model_validate(m) for m in metrics],
    )
