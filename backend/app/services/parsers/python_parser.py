import ast
import re
from pathlib import Path

from app.services.scanner.types import ParsedEndpoint, ParsedFile, ParsedImport, ParsedSymbol


def parse_python_file(relative_path: str, content: str, size_bytes: int) -> ParsedFile:
    lines = content.splitlines()
    loc = sum(1 for line in lines if line.strip() and not line.strip().startswith("#"))

    imports: list[ParsedImport] = []
    symbols: list[ParsedSymbol] = []
    endpoints: list[ParsedEndpoint] = []
    is_entry_point = relative_path.endswith(("main.py", "__main__.py", "app.py", "server.py"))

    try:
        tree = ast.parse(content, filename=relative_path)
    except SyntaxError:
        return ParsedFile(
            relative_path=relative_path,
            language="python",
            size_bytes=size_bytes,
            lines_of_code=loc,
            is_entry_point=is_entry_point,
            content=content,
        )

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(
                    ParsedImport(
                        module=alias.name,
                        names=[alias.asname or alias.name.split(".")[-1]],
                        line_number=getattr(node, "lineno", 0),
                        raw=f"import {alias.name}",
                    )
                )
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            names = [alias.name for alias in node.names]
            imports.append(
                ParsedImport(
                    module=module,
                    names=names,
                    line_number=getattr(node, "lineno", 0),
                    raw=f"from {module} import {', '.join(names)}",
                )
            )
        elif isinstance(node, ast.FunctionDef):
            symbols.append(
                ParsedSymbol(name=node.name, kind="function", line_number=getattr(node, "lineno", 0))
            )
        elif isinstance(node, ast.AsyncFunctionDef):
            symbols.append(
                ParsedSymbol(name=node.name, kind="function", line_number=getattr(node, "lineno", 0))
            )
        elif isinstance(node, ast.ClassDef):
            symbols.append(
                ParsedSymbol(name=node.name, kind="class", line_number=getattr(node, "lineno", 0))
            )

    endpoints.extend(_detect_fastapi_endpoints(content))
    endpoints.extend(_detect_flask_endpoints(content))

    return ParsedFile(
        relative_path=relative_path,
        language="python",
        size_bytes=size_bytes,
        lines_of_code=loc,
        imports=imports,
        symbols=symbols,
        endpoints=endpoints,
        is_entry_point=is_entry_point,
        content=content,
    )


def _detect_fastapi_endpoints(content: str) -> list[ParsedEndpoint]:
    pattern = re.compile(
        r"@(?:(?:app|router)\.)?(get|post|put|patch|delete|head|options)\(\s*[\"']([^\"']+)[\"']",
        re.IGNORECASE,
    )
    endpoints: list[ParsedEndpoint] = []
    for match in pattern.finditer(content):
        line_number = content[: match.start()].count("\n") + 1
        endpoints.append(
            ParsedEndpoint(
                method=match.group(1).upper(),
                path=match.group(2),
                line_number=line_number,
                framework="fastapi",
            )
        )
    return endpoints


def _detect_flask_endpoints(content: str) -> list[ParsedEndpoint]:
    pattern = re.compile(
        r"@(?:(?:app|bp|blueprint)\.)?route\(\s*[\"']([^\"']+)[\"'](?:,\s*methods=\[([^\]]+)\])?",
        re.IGNORECASE,
    )
    endpoints: list[ParsedEndpoint] = []
    for match in pattern.finditer(content):
        path = match.group(1)
        methods_raw = match.group(2)
        line_number = content[: match.start()].count("\n") + 1
        if methods_raw:
            methods = re.findall(r"['\"](\w+)['\"]", methods_raw)
        else:
            methods = ["GET"]
        for method in methods:
            endpoints.append(
                ParsedEndpoint(
                    method=method.upper(),
                    path=path,
                    line_number=line_number,
                    framework="flask",
                )
            )
    return endpoints


def resolve_python_import(source_path: str, imp: ParsedImport, repo_root: Path) -> str | None:
    """Resolve a Python import to a relative file path within the repo."""
    module_parts = imp.module.split(".") if imp.module else []
    source_dir = Path(source_path).parent

    # Relative import
    if imp.module is None or (imp.module == "" and source_path.endswith(".py")):
        return None

    candidates: list[Path] = []

    if module_parts and module_parts[0] == "":
        # from .module import ...
        rel_parts = [p for p in module_parts if p]
        if rel_parts:
            candidates.append(source_dir / "/".join(rel_parts))
            candidates.append(source_dir / "/".join(rel_parts) / "__init__.py")
    else:
        # Absolute import - search from repo root
        mod_path = "/".join(module_parts)
        candidates.append(repo_root / f"{mod_path}.py")
        candidates.append(repo_root / mod_path / "__init__.py")

        # Also try relative to source directory for local packages
        candidates.append(source_dir / f"{module_parts[-1]}.py" if module_parts else source_dir)
        if len(module_parts) > 1:
            candidates.append(source_dir / "/".join(module_parts) / "__init__.py")

    for candidate in candidates:
        try:
            resolved = candidate.resolve()
            root_resolved = repo_root.resolve()
            if resolved.is_file() and str(resolved).startswith(str(root_resolved)):
                return str(resolved.relative_to(root_resolved)).replace("\\", "/")
        except (OSError, ValueError):
            continue

    # Fallback: map to module path notation for graph
    if module_parts:
        return f"{ '/'.join(module_parts) }.py" if not imp.module.endswith("__init__") else "/".join(module_parts) + "/__init__.py"
    return None
