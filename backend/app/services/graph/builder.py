from collections import defaultdict, deque
from dataclasses import dataclass, field

from app.services.scanner.types import ParsedFile


@dataclass
class GraphData:
    edges: list[tuple[str, str, str]] = field(default_factory=list)  # source, target, import_stmt
    node_languages: dict[str, str] = field(default_factory=dict)
    node_entry_points: set[str] = field(default_factory=set)


def build_dependency_graph(parsed_files: list[ParsedFile], resolved_edges: list[tuple[str, str, str]]) -> GraphData:
    graph = GraphData()
    graph.edges = resolved_edges

    for pf in parsed_files:
        graph.node_languages[pf.relative_path] = pf.language
        if pf.is_entry_point:
            graph.node_entry_points.add(pf.relative_path)

    # Ensure all nodes referenced in edges exist
    for source, target, _ in resolved_edges:
        graph.node_languages.setdefault(source, "unknown")
        graph.node_languages.setdefault(target, "unknown")

    return graph


def find_circular_dependencies(edges: list[tuple[str, str, str]]) -> list[list[str]]:
    adjacency: dict[str, list[str]] = defaultdict(list)
    nodes: set[str] = set()

    for source, target, _ in edges:
        adjacency[source].append(target)
        nodes.add(source)
        nodes.add(target)

    cycles: list[list[str]] = []
    visited: set[str] = set()
    rec_stack: set[str] = set()
    path: list[str] = []

    def dfs(node: str) -> None:
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in adjacency.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)
            elif neighbor in rec_stack:
                if neighbor in path:
                    idx = path.index(neighbor)
                    cycle = path[idx:] + [neighbor]
                    normalized = _normalize_cycle(cycle)
                    if normalized not in [_normalize_cycle(c) for c in cycles]:
                        cycles.append(cycle)

        path.pop()
        rec_stack.remove(node)

    for node in sorted(nodes):
        if node not in visited:
            dfs(node)

    return cycles


def _normalize_cycle(cycle: list[str]) -> tuple[str, ...]:
    if not cycle:
        return tuple()
    # Remove duplicate closing node if present
    if cycle[0] == cycle[-1] and len(cycle) > 1:
        cycle = cycle[:-1]
    if not cycle:
        return tuple()
    min_idx = cycle.index(min(cycle))
    rotated = cycle[min_idx:] + cycle[:min_idx]
    return tuple(rotated)


def compute_blast_radius(edges: list[tuple[str, str, str]]) -> dict[str, float]:
    """Compute blast radius as count of transitive dependents (inbound reachability)."""
    reverse_adj: dict[str, set[str]] = defaultdict(set)
    nodes: set[str] = set()

    for source, target, _ in edges:
        reverse_adj[target].add(source)
        nodes.add(source)
        nodes.add(target)

    blast: dict[str, float] = {}

    for node in nodes:
        queue: deque[str] = deque([node])
        seen: set[str] = {node}
        while queue:
            current = queue.popleft()
            for dependent in reverse_adj.get(current, set()):
                if dependent not in seen:
                    seen.add(dependent)
                    queue.append(dependent)
        blast[node] = float(max(0, len(seen) - 1))

    return blast


def compute_inbound_outbound_counts(edges: list[tuple[str, str, str]]) -> tuple[dict[str, int], dict[str, int]]:
    inbound: dict[str, int] = defaultdict(int)
    outbound: dict[str, int] = defaultdict(int)

    for source, target, _ in edges:
        outbound[source] += 1
        inbound[target] += 1

    return dict(inbound), dict(outbound)
