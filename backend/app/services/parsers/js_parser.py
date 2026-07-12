import re
from pathlib import Path

from app.services.scanner.types import ParsedEndpoint, ParsedFile, ParsedImport, ParsedSymbol


IMPORT_PATTERNS = [
    re.compile(r"""import\s+(?:type\s+)?(?:\{[^}]+\}|[\w*]+)\s+from\s+['"]([^'"]+)['"]"""),
    re.compile(r"""import\s+['"]([^'"]+)['"]"""),
    re.compile(r"""require\s*\(\s*['"]([^'"]+)['"]\s*\)"""),
    re.compile(r"""from\s+['"]([^'"]+)['"]\s+import"""),
]

EXPRESS_ROUTE_PATTERN = re.compile(
    r"""(?:(?:app|router|server)\.)?(get|post|put|patch|delete|all)\(\s*['"]([^'"]+)['"]""",
    re.IGNORECASE,
)

FUNCTION_PATTERN = re.compile(
    r"(?:export\s+)?(?:async\s+)?function\s+(\w+)",
)
CLASS_PATTERN = re.compile(
    r"(?:export\s+)?class\s+(\w+)",
)
ARROW_FN_PATTERN = re.compile(
    r"(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>",
)


def parse_js_ts_file(relative_path: str, content: str, size_bytes: int, language: str) -> ParsedFile:
    lines = content.splitlines()
    loc = sum(
        1
        for line in lines
        if line.strip() and not line.strip().startswith("//") and not line.strip().startswith("*")
    )

    imports: list[ParsedImport] = []
    symbols: list[ParsedSymbol] = []
    endpoints: list[ParsedEndpoint] = []
    is_entry_point = relative_path.endswith(
        ("index.ts", "index.js", "main.ts", "main.js", "server.ts", "server.js", "app.ts", "app.js")
    )

    for pattern in IMPORT_PATTERNS:
        for match in pattern.finditer(content):
            module = match.group(1)
            line_number = content[: match.start()].count("\n") + 1
            imports.append(
                ParsedImport(
                    module=module,
                    line_number=line_number,
                    raw=match.group(0),
                )
            )

    for match in FUNCTION_PATTERN.finditer(content):
        symbols.append(
            ParsedSymbol(name=match.group(1), kind="function", line_number=content[: match.start()].count("\n") + 1)
        )
    for match in CLASS_PATTERN.finditer(content):
        symbols.append(
            ParsedSymbol(name=match.group(1), kind="class", line_number=content[: match.start()].count("\n") + 1)
        )
    for match in ARROW_FN_PATTERN.finditer(content):
        symbols.append(
            ParsedSymbol(name=match.group(1), kind="function", line_number=content[: match.start()].count("\n") + 1)
        )

    for match in EXPRESS_ROUTE_PATTERN.finditer(content):
        line_number = content[: match.start()].count("\n") + 1
        method = match.group(1).upper()
        if method == "ALL":
            method = "GET"
        endpoints.append(
            ParsedEndpoint(
                method=method,
                path=match.group(2),
                line_number=line_number,
                framework="express",
            )
        )

    return ParsedFile(
        relative_path=relative_path,
        language=language,
        size_bytes=size_bytes,
        lines_of_code=loc,
        imports=imports,
        symbols=symbols,
        endpoints=endpoints,
        is_entry_point=is_entry_point,
        content=content,
    )


def resolve_js_import(source_path: str, module: str, repo_root: Path) -> str | None:
    if module.startswith("."):
        source_dir = Path(source_path).parent
        base = (source_dir / module).resolve()
        candidates = [
            base,
            Path(str(base) + ".ts"),
            Path(str(base) + ".tsx"),
            Path(str(base) + ".js"),
            Path(str(base) + ".jsx"),
            base / "index.ts",
            base / "index.js",
        ]
        for candidate in candidates:
            try:
                if candidate.is_file():
                    root_resolved = repo_root.resolve()
                    if str(candidate.resolve()).startswith(str(root_resolved)):
                        return str(candidate.resolve().relative_to(root_resolved)).replace("\\", "/")
            except OSError:
                continue
        return None

    # External package - don't create internal edge
    return None
