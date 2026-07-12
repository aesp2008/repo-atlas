from app.services.analyzers.risk import compute_risk_score


def test_low_risk_score():
    score, explanation = compute_risk_score(
        lines_of_code=50,
        import_count=2,
        dependent_count=0,
        function_count=2,
        class_count=1,
        cyclomatic_complexity=3,
        blast_radius=0,
    )
    assert score < 40
    assert "Low risk" in explanation or "Moderate" in explanation or "Risk factors" in explanation


def test_high_risk_score():
    score, explanation = compute_risk_score(
        lines_of_code=800,
        import_count=25,
        dependent_count=15,
        function_count=30,
        class_count=10,
        cyclomatic_complexity=45,
        blast_radius=20,
    )
    assert score >= 60
    assert len(explanation) > 10


def test_risk_score_capped_at_100():
    score, _ = compute_risk_score(
        lines_of_code=5000,
        import_count=100,
        dependent_count=50,
        function_count=100,
        class_count=50,
        cyclomatic_complexity=200,
        blast_radius=100,
    )
    assert score <= 100
