from hypothesis_agent.core.models import EvidenceSnippet
from hypothesis_agent.reasoning.generate import HypothesisGenerator
from hypothesis_agent.app.services.retrieval_service import retrieval_service
import re

import numpy as np


generator = HypothesisGenerator()


def extract_entities(text: str):
    """
    Simple entity extraction using regex patterns for biomedical terms.
    """
    entities = []
    
    # Pattern for biological/medical terms (capitalized words, acronyms, etc.)
    patterns = [
        r'\b[A-Z][a-z]+(?:tion|sis|ty|cy|gy|ism|ment|osis|pathy)\b',  # Medical terms
        r'\b[A-Z]{2,}\b',  # Acronyms
        r'\b[a-z]+-?[a-z]+\b',  # Hyphenated terms
        r'\b\w+ing\b',  # -ing words
        r'\b\w+ation\b',  # -ation words
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        entities.extend([match.capitalize() for match in matches])
    
    # Remove duplicates and filter for meaningful entities
    entities = list(set([e for e in entities if len(e) > 2]))
    
    return entities[:10]  # Limit to top 10


def run_analysis_pipeline(query: str):
    """
    Main backend orchestration layer.
    """

    # � REAL RETRIEVAL
    snippets = retrieval_service.search(query, top_k=5)

    if len(snippets) < 2:
        return empty_response()

    # 🔹 Generate graph & hypothesis
    graph = generator.build_graph(snippets)
    hypothesis_text, conflicts = generator.generate_from_graph(graph)
    confidence = generator.compute_confidence(graph, conflicts)

    edges = graph.get_edges()
    chains = graph.find_chains(depth=3)

    # -------------------------
    # Build structured response
    # -------------------------

    nodes_dict = {}
    for e in edges:
        nodes_dict.setdefault(e.source, 0)
        nodes_dict.setdefault(e.target, 0)
        nodes_dict[e.source] += 1
        nodes_dict[e.target] += 1

    nodes = [
        {
            "id": name,
            "label": name,
            "frequency": freq,
        }
        for name, freq in nodes_dict.items()
    ]

    graph_edges = [
        {
            "id": f"{i}",
            "source": e.source,
            "target": e.target,
            "polarity": e.polarity,
            "weight": e.weight,
            "conflict": False,
        }
        for i, e in enumerate(edges)
    ]

    evidence_items = [
        {
            "id": s.id,
            "doc_id": s.doc_id,
            "score": s.score,
            "excerpt": s.text[:300],
            "entities": extract_entities(s.text),
            "relations_count": len([e for e in edges if e.source in extract_entities(s.text) or e.target in extract_entities(s.text)]),
            "used": True,
            "conflict": False,
        }
        for s in snippets
    ]

    mean_weight = np.mean([e.weight for e in edges]) if edges else 0
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
            "new_metric": 0.5
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