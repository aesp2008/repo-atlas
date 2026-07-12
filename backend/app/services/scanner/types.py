from dataclasses import dataclass, field


@dataclass
class ParsedImport:
    module: str
    names: list[str] = field(default_factory=list)
    line_number: int = 0
    raw: str = ""


@dataclass
class ParsedSymbol:
    name: str
    kind: str  # function | class
    line_number: int = 0


@dataclass
class ParsedEndpoint:
    method: str
    path: str
    line_number: int
    framework: str


@dataclass
class ParsedFile:
    relative_path: str
    language: str
    size_bytes: int
    lines_of_code: int
    imports: list[ParsedImport] = field(default_factory=list)
    symbols: list[ParsedSymbol] = field(default_factory=list)
    endpoints: list[ParsedEndpoint] = field(default_factory=list)
    is_entry_point: bool = False
    content: str = ""
