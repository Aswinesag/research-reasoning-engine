from functools import lru_cache
import re

import numpy as np

from hypothesis_agent.app.services.retrieval_service import retrieval_service
from hypothesis_agent.reasoning.generate import HypothesisGenerator


generator = HypothesisGenerator()


@lru_cache(maxsize=512)
def extract_entities(text: str):
    """
    Simple entity extraction using regex patterns for biomedical terms.
    """
    entities = []
    patterns = [
        r"\b[A-Z][a-z]+(?:tion|sis|ty|cy|gy|ism|ment|osis|pathy)\b",
        r"\b[A-Z]{2,}\b",
        r"\b[a-z]+-?[a-z]+\b",
        r"\b\w+ing\b",
        r"\b\w+ation\b",
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        entities.extend([match.capitalize() for match in matches])

    entities = list(set([entity for entity in entities if len(entity) > 2]))
    return entities[:10]


def run_analysis_pipeline(query: str):
    return _run_analysis_pipeline_cached(query)


@lru_cache(maxsize=128)
def _run_analysis_pipeline_cached(query: str):
    """
    Main backend orchestration layer.
    """
    snippets = retrieval_service.search(query, top_k=5)

    if len(snippets) < 2:
        return empty_response()

    graph = generator.build_graph(snippets)
    hypothesis_text, conflicts = generator.generate_from_graph(graph)
    confidence = generator.compute_confidence(graph, conflicts)

    edges = graph.get_edges()
    chains = graph.find_chains(depth=3)

    nodes_dict = {}
    for edge in edges:
        nodes_dict.setdefault(edge.source, 0)
        nodes_dict.setdefault(edge.target, 0)
        nodes_dict[edge.source] += 1
        nodes_dict[edge.target] += 1

    nodes = [
        {
            "id": name,
            "label": name,
            "frequency": frequency,
        }
        for name, frequency in nodes_dict.items()
    ]

    graph_edges = [
        {
            "id": f"{index}",
            "source": edge.source,
            "target": edge.target,
            "polarity": edge.polarity,
            "weight": edge.weight,
            "conflict": False,
        }
        for index, edge in enumerate(edges)
    ]

    evidence_items = []
    for snippet in snippets:
        snippet_entities = extract_entities(snippet.text)
        relations_count = sum(
            1
            for edge in edges
            if edge.source in snippet_entities or edge.target in snippet_entities
        )
        evidence_items.append(
            {
                "id": snippet.id,
                "doc_id": snippet.doc_id,
                "score": snippet.score,
                "excerpt": snippet.text[:300],
                "entities": snippet_entities,
                "relations_count": relations_count,
                "used": True,
                "conflict": False,
            }
        )

    mean_weight = np.mean([edge.weight for edge in edges]) if edges else 0
    reinforcement_factor = min(len(edges) / 5, 1.0)
    graph_density = len(edges) / max(len(nodes), 1)

    return {
        "overview": {
            "total_edges": len(edges),
            "conflicts": len(conflicts),
            "confidence": confidence,
            "strongest_chain": chains[0] if chains else [],
        },
        "evidence": evidence_items,
        "graph": {
            "nodes": nodes,
            "edges": graph_edges,
        },
        "hypothesis": {
            "mechanism": hypothesis_text,
            "supporting_chains": chains[:3],
            "conflicts": conflicts,
            "testable_predictions": [],
        },
        "metrics": {
            "mean_weight": round(float(mean_weight), 3),
            "reinforcement_factor": reinforcement_factor,
            "graph_density": round(graph_density, 3),
            "new_metric": 0.5,
        },
    }


def empty_response():
    return {
        "overview": {
            "total_edges": 0,
            "conflicts": 0,
            "confidence": 0,
            "strongest_chain": [],
        },
        "evidence": [],
        "graph": {"nodes": [], "edges": []},
        "hypothesis": {
            "mechanism": "Insufficient structured evidence retrieved.",
            "supporting_chains": [],
            "conflicts": [],
            "testable_predictions": [],
        },
        "metrics": {
            "mean_weight": 0,
            "reinforcement_factor": 0,
            "graph_density": 0,
        },
    }
