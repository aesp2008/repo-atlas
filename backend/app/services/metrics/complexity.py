import re


def approximate_cyclomatic_complexity(content: str, language: str) -> float:
    """Approximate cyclomatic complexity by counting decision points."""
    if language == "python":
        patterns = [
            r"\bif\b",
            r"\belif\b",
            r"\bfor\b",
            r"\bwhile\b",
            r"\band\b",
            r"\bor\b",
            r"\bexcept\b",
            r"\bwith\b",
            r"\?\.",  # rarely in python
        ]
    else:
        patterns = [
            r"\bif\b",
            r"\belse if\b",
            r"\bfor\b",
            r"\bwhile\b",
            r"\bcase\b",
            r"\?\?",  # nullish coalescing
            r"\?\.",  # optional chaining
            r"&&",
            r"\|\|",
            r"\bcatch\b",
        ]

    count = 1  # base complexity
    for pattern in patterns:
        count += len(re.findall(pattern, content))

    return float(count)


def count_functions_and_classes(parsed_file) -> tuple[int, int]:
    functions = sum(1 for s in parsed_file.symbols if s.kind == "function")
    classes = sum(1 for s in parsed_file.symbols if s.kind == "class")
    return functions, classes
