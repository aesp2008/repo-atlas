from datetime import datetime

from pydantic import BaseModel, Field


class ScanRequest(BaseModel):
    path: str = Field(..., min_length=1, description="Absolute or relative path to local repository")
    name: str | None = Field(None, description="Optional project display name")


class ScanRunSummary(BaseModel):
    id: int
    status: str
    files_scanned: int
    started_at: datetime
    completed_at: datetime | None

    model_config = {"from_attributes": True}


class ProjectSummary(BaseModel):
    id: int
    name: str
    path: str
    created_at: datetime
    updated_at: datetime
    latest_scan: ScanRunSummary | None = None
    file_count: int = 0
    endpoint_count: int = 0
    dependency_count: int = 0
    circular_dependency_count: int = 0

    model_config = {"from_attributes": True}


class ProjectDetail(ProjectSummary):
    languages: list[str] = []
    top_risky_files: list["HotspotItem"] = []


class FileItem(BaseModel):
    id: int
    relative_path: str
    language: str
    size_bytes: int
    lines_of_code: int
    function_count: int
    class_count: int
    import_count: int
    is_entry_point: bool

    model_config = {"from_attributes": True}


class DependencyItem(BaseModel):
    source_path: str
    target_path: str
    import_statement: str


class EndpointItem(BaseModel):
    id: int
    method: str
    path: str
    file_path: str
    line_number: int
    framework: str

    model_config = {"from_attributes": True}


class HotspotItem(BaseModel):
    file_path: str
    risk_score: float
    lines_of_code: int
    import_count: int
    dependent_count: int
    function_count: int
    class_count: int
    cyclomatic_complexity: float
    blast_radius: float
    risk_explanation: str

    model_config = {"from_attributes": True}


class GraphNode(BaseModel):
    id: str
    label: str
    language: str
    risk_score: float = 0.0
    blast_radius: float = 0.0
    is_entry_point: bool = False


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    label: str = ""


class CircularDependency(BaseModel):
    cycle: list[str]


class GraphResponse(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]
    circular_dependencies: list[CircularDependency]


class OverviewStats(BaseModel):
    files_scanned: int
    languages: list[str]
    api_count: int
    dependency_count: int
    circular_dependency_count: int
    top_risky_files: list[HotspotItem]
