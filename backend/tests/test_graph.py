from app.services.graph.builder import find_circular_dependencies


def test_no_cycles():
    edges = [
        ("a.py", "b.py", "import b"),
        ("b.py", "c.py", "import c"),
    ]
    cycles = find_circular_dependencies(edges)
    assert cycles == []


def test_simple_cycle():
    edges = [
        ("a.py", "b.py", "import b"),
        ("b.py", "a.py", "import a"),
    ]
    cycles = find_circular_dependencies(edges)
    assert len(cycles) >= 1
    assert set(cycles[0]) >= {"a.py", "b.py"}


def test_transitive_cycle():
    edges = [
        ("a.py", "b.py", ""),
        ("b.py", "c.py", ""),
        ("c.py", "a.py", ""),
    ]
    cycles = find_circular_dependencies(edges)
    assert len(cycles) >= 1
