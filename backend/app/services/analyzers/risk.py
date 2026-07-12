def compute_risk_score(
    lines_of_code: int,
    import_count: int,
    dependent_count: int,
    function_count: int,
    class_count: int,
    cyclomatic_complexity: float,
    blast_radius: float,
) -> tuple[float, str]:
    """Compute a 0-100 risk score with plain-English explanation."""
    loc_score = min(lines_of_code / 500 * 25, 25)
    import_score = min(import_count / 20 * 15, 15)
    dependent_score = min(dependent_count / 10 * 20, 20)
    symbol_score = min((function_count + class_count) / 30 * 10, 10)
    complexity_score = min(cyclomatic_complexity / 30 * 20, 20)
    blast_score = min(blast_radius / 15 * 10, 10)

    total = loc_score + import_score + dependent_score + symbol_score + complexity_score + blast_score
    risk_score = round(min(total, 100), 1)

    reasons: list[str] = []

    if lines_of_code > 300:
        reasons.append(f"large file ({lines_of_code} lines of code)")
    if import_count > 10:
        reasons.append(f"high import count ({import_count})")
    if dependent_count > 5:
        reasons.append(f"many dependents ({dependent_count} files rely on this)")
    if cyclomatic_complexity > 20:
        reasons.append(f"high cyclomatic complexity (~{int(cyclomatic_complexity)})")
    if blast_radius > 8:
        reasons.append(f"high blast radius ({int(blast_radius)} transitive dependents)")
    if function_count + class_count > 20:
        reasons.append(f"many symbols ({function_count + class_count} functions/classes)")

    if not reasons:
        if risk_score < 30:
            explanation = "Low risk: this file is small, focused, and has limited downstream impact."
        elif risk_score < 60:
            explanation = "Moderate risk: some complexity or coupling detected, but manageable."
        else:
            explanation = "Elevated risk: multiple moderate factors contribute to overall score."
    else:
        explanation = "Risk factors: " + "; ".join(reasons) + "."

    return risk_score, explanation
