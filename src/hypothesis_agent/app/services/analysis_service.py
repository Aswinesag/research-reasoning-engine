from functools import lru_cache
from time import perf_counter
import re

import numpy as np

from hypothesis_agent.app.services.job_store import job_store
from hypothesis_agent.app.services.retrieval_service import retrieval_service
from hypothesis_agent.reasoning.generate import HypothesisGenerator


generator = HypothesisGenerator()


@lru_cache(maxsize=512)
def extract_entities(text: str):
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


def build_fast_analysis(query: str):
    start_time = perf_counter()
    print(f"[analysis] fast_start query={query!r}")

    snippets = retrieval_service.search(query, top_k=3)
    print(f"[analysis] retrieval_complete elapsed={perf_counter() - start_time:.2f}s snippets={len(snippets)}")

    if len(snippets) < 2:
        response = empty_response()
        response["status"] = "complete"
        response["job_id"] = None
        return response

    graph = generator.build_graph(snippets)
    edges = graph.get_edges()
    chains = graph.find_chains(depth=3)
    conflicts = graph.detect_conflicts()
    confidence = generator.compute_confidence(graph, conflicts)

    nodes_dict = {}
    for edge in edges:
        nodes_dict.setdefault(edge.source, 0)
        nodes_dict.setdefault(edge.target, 0)
        nodes_dict[edge.source] += 1
        nodes_dict[edge.target] += 1

    nodes = [
        {"id": name, "label": name, "frequency": frequency}
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
            1 for edge in edges if edge.source in snippet_entities or edge.target in snippet_entities
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

    job = job_store.create(query)
    job_store.update(job.id, status="processing")

    return {
        "status": "processing",
        "job_id": job.id,
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
            "mechanism": "Hypothesis generation in progress.",
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


def complete_analysis(query: str, job_id: str):
    start_time = perf_counter()
    print(f"[analysis] hypothesis_job_start job_id={job_id} query={query!r}")

    try:
        snippets = retrieval_service.search(query, top_k=3)
        if len(snippets) < 2:
            result = empty_response()
        else:
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
                {"id": name, "label": name, "frequency": frequency}
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
                    1 for edge in edges if edge.source in snippet_entities or edge.target in snippet_entities
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

            result = {
                "status": "complete",
                "job_id": job_id,
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

        job_store.update(job_id, status="complete", result=result)
        print(f"[analysis] hypothesis_job_complete job_id={job_id} elapsed={perf_counter() - start_time:.2f}s")
        return result
    except Exception as exc:
        error_result = fallback_response(query, str(exc))
        job_store.update(job_id, status="failed", result=error_result, error=str(exc))
        print(f"[analysis] hypothesis_job_failed job_id={job_id} elapsed={perf_counter() - start_time:.2f}s error={exc!r}")
        return error_result


def get_job_result(job_id: str):
    job = job_store.get(job_id)
    if job is None:
        return None
    return {
        "job_id": job.id,
        "status": job.status,
        "query": job.query,
        "result": job.result,
        "error": job.error,
        "created_at": job.created_at,
        "updated_at": job.updated_at,
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


def fallback_response(query: str, error_message: str):
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
            "mechanism": "The backend could not complete the full reasoning pass for this query.",
            "supporting_chains": [],
            "conflicts": [],
            "testable_predictions": [],
        },
        "metrics": {
            "mean_weight": 0,
            "reinforcement_factor": 0,
            "graph_density": 0,
        },
        "debug": {
            "query": query,
            "error": error_message,
        },
    }
