from pathlib import Path

from app.core.constants import IGNORED_DIRS, MAX_FILE_SIZE_BYTES, SUPPORTED_EXTENSIONS
from app.services.parsers.js_parser import parse_js_ts_file, resolve_js_import
from app.services.parsers.python_parser import parse_python_file, resolve_python_import
from app.services.scanner.types import ParsedFile


class RepositoryScanner:
    """Safely walks a local repository and parses supported source files."""

    def __init__(self, repo_path: str | Path):
        self.repo_root = Path(repo_path).resolve()
        if not self.repo_root.exists():
            raise FileNotFoundError(f"Repository path does not exist: {repo_path}")
        if not self.repo_root.is_dir():
            raise NotADirectoryError(f"Repository path is not a directory: {repo_path}")

    def scan(self) -> tuple[list[ParsedFile], list[tuple[str, str, str]]]:
        parsed_files: list[ParsedFile] = []
        resolved_edges: list[tuple[str, str, str]] = []

        for file_path in self._iter_files():
            relative = str(file_path.relative_to(self.repo_root)).replace("\\", "/")
            try:
                size = file_path.stat().st_size
                if size > MAX_FILE_SIZE_BYTES:
                    continue
                content = file_path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue

            ext = file_path.suffix.lower()
            language = SUPPORTED_EXTENSIONS.get(ext)
            if not language:
                continue

            if language == "python":
                parsed = parse_python_file(relative, content, size)
            else:
                parsed = parse_js_ts_file(relative, content, size, language)

            parsed_files.append(parsed)

        # Resolve imports to edges
        file_paths = {pf.relative_path for pf in parsed_files}
        for pf in parsed_files:
            for imp in pf.imports:
                target: str | None = None
                if pf.language == "python":
                    target = resolve_python_import(pf.relative_path, imp, self.repo_root)
                else:
                    target = resolve_js_import(pf.relative_path, imp.module, self.repo_root)

                if target and self._is_safe_internal_path(target):
                    # Only add edge if target exists in scanned files or is a plausible internal path
                    if target in file_paths or any(target.endswith(fp) for fp in file_paths):
                        resolved_edges.append((pf.relative_path, target, imp.raw))
                    elif target in file_paths or Path(self.repo_root / target).exists():
                        resolved_edges.append((pf.relative_path, target, imp.raw))

        # Deduplicate edges
        seen: set[tuple[str, str]] = set()
        unique_edges: list[tuple[str, str, str]] = []
        for source, target, stmt in resolved_edges:
            key = (source, target)
            if key not in seen:
                seen.add(key)
                unique_edges.append((source, target, stmt))

        return parsed_files, unique_edges

    def _iter_files(self):
        for path in self.repo_root.rglob("*"):
            if not path.is_file():
                continue
            if self._should_ignore(path):
                continue
            if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue
            yield path

    def _should_ignore(self, path: Path) -> bool:
        try:
            rel_parts = path.relative_to(self.repo_root).parts
        except ValueError:
            return True

        for part in rel_parts:
            if part in IGNORED_DIRS:
                return True
            if part.endswith(".egg-info"):
                return True
        return False

    def _is_safe_internal_path(self, relative_path: str) -> bool:
        resolved = (self.repo_root / relative_path).resolve()
        try:
            resolved.relative_to(self.repo_root.resolve())
            return True
        except ValueError:
            return False
