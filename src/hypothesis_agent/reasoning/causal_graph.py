# src/hypothesis_agent/reasoning/causal_graph.py

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Edge:
    source: str
    target: str
    polarity: str
    evidence_id: int
    weight: float
    excerpt: str
    doc_id: str


class CausalGraph:
    def __init__(self):
        self.graph: Dict[str, List[Edge]] = {}

    def add_edge(self, edge: Edge):
        if edge.source not in self.graph:
            self.graph[edge.source] = []
        self.graph[edge.source].append(edge)

    def get_edges(self):
        edges = []
        for edge_list in self.graph.values():
            edges.extend(edge_list)
        return edges

    def detect_conflicts(self):
        conflicts = []
        edge_map = {}

        for edge in self.get_edges():
            key = (edge.source, edge.target)
            edge_map.setdefault(key, []).append(edge)

        for key, edges in edge_map.items():
            polarities = set(e.polarity for e in edges)
            if len(polarities) > 1:
                conflicts.append({
                    "source": key[0],
                    "target": key[1],
                    "polarities": list(polarities),
                    "evidence_ids": [e.evidence_id for e in edges]
                })

        return conflicts

    def find_chains(self, depth=3):
        chains = []

        def dfs(current, path, d):
            if d == 0:
                return
            if current not in self.graph:
                return
            for edge in self.graph[current]:
                new_path = path + [edge.target]
                chains.append(new_path)
                dfs(edge.target, new_path, d - 1)

        for node in self.graph.keys():
            dfs(node, [node], depth)

        return chains