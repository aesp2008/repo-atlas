from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.entities import Dependency, Endpoint, FileMetric, FileRecord, Project, ScanRun
from app.services.analyzers.risk import compute_risk_score
from app.services.graph.builder import (
    compute_blast_radius,
    compute_inbound_outbound_counts,
    find_circular_dependencies,
)
from app.services.metrics.complexity import approximate_cyclomatic_complexity, count_functions_and_classes
from app.services.scanner.repository_scanner import RepositoryScanner


class ScanService:
    def __init__(self, db: Session):
        self.db = db

    def scan_repository(self, path: str, name: str | None = None) -> Project:
        scanner = RepositoryScanner(path)
        parsed_files, edges = scanner.scan()

        project_name = name or scanner.repo_root.name
        project = self.db.query(Project).filter(Project.path == str(scanner.repo_root)).first()

        if project:
            self._clear_project_data(project.id)
        else:
            project = Project(name=project_name, path=str(scanner.repo_root))
            self.db.add(project)
            self.db.flush()

        project.name = project_name
        project.updated_at = datetime.now(timezone.utc)

        scan_run = ScanRun(
            project_id=project.id,
            status="running",
            files_scanned=0,
        )
        self.db.add(scan_run)
        self.db.flush()

        try:
            inbound, _outbound = compute_inbound_outbound_counts(edges)
            blast_radius = compute_blast_radius(edges)

            for pf in parsed_files:
                fn_count, cls_count = count_functions_and_classes(pf)
                file_record = FileRecord(
                    project_id=project.id,
                    relative_path=pf.relative_path,
                    language=pf.language,
                    size_bytes=pf.size_bytes,
                    lines_of_code=pf.lines_of_code,
                    function_count=fn_count,
                    class_count=cls_count,
                    import_count=len(pf.imports),
                    is_entry_point=pf.is_entry_point,
                )
                self.db.add(file_record)

                for ep in pf.endpoints:
                    self.db.add(
                        Endpoint(
                            project_id=project.id,
                            method=ep.method,
                            path=ep.path,
                            file_path=pf.relative_path,
                            line_number=ep.line_number,
                            framework=ep.framework,
                        )
                    )

            for source, target, stmt in edges:
                self.db.add(
                    Dependency(
                        project_id=project.id,
                        source_path=source,
                        target_path=target,
                        import_statement=stmt,
                    )
                )

            for pf in parsed_files:
                complexity = approximate_cyclomatic_complexity(pf.content, pf.language)
                fn_count, cls_count = count_functions_and_classes(pf)
                dependents = inbound.get(pf.relative_path, 0)
                blast = blast_radius.get(pf.relative_path, 0.0)
                risk_score, explanation = compute_risk_score(
                    lines_of_code=pf.lines_of_code,
                    import_count=len(pf.imports),
                    dependent_count=dependents,
                    function_count=fn_count,
                    class_count=cls_count,
                    cyclomatic_complexity=complexity,
                    blast_radius=blast,
                )
                self.db.add(
                    FileMetric(
                        project_id=project.id,
                        file_path=pf.relative_path,
                        lines_of_code=pf.lines_of_code,
                        import_count=len(pf.imports),
                        dependent_count=dependents,
                        function_count=fn_count,
                        class_count=cls_count,
                        cyclomatic_complexity=complexity,
                        blast_radius=blast,
                        risk_score=risk_score,
                        risk_explanation=explanation,
                    )
                )

            scan_run.status = "completed"
            scan_run.files_scanned = len(parsed_files)
            scan_run.completed_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(project)
            return project

        except Exception as exc:
            scan_run.status = "failed"
            scan_run.error_message = str(exc)
            scan_run.completed_at = datetime.now(timezone.utc)
            self.db.commit()
            raise

    def _clear_project_data(self, project_id: int) -> None:
        self.db.query(Dependency).filter(Dependency.project_id == project_id).delete()
        self.db.query(Endpoint).filter(Endpoint.project_id == project_id).delete()
        self.db.query(FileMetric).filter(FileMetric.project_id == project_id).delete()
        self.db.query(FileRecord).filter(FileRecord.project_id == project_id).delete()
        self.db.query(ScanRun).filter(ScanRun.project_id == project_id).delete()
        self.db.flush()

    def get_circular_dependencies(self, project_id: int) -> list[list[str]]:
        deps = self.db.query(Dependency).filter(Dependency.project_id == project_id).all()
        edges = [(d.source_path, d.target_path, d.import_statement) for d in deps]
        return find_circular_dependencies(edges)
