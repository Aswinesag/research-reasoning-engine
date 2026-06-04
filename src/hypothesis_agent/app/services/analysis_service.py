from functools import lru_cache
from statistics import mean
from time import perf_counter
import re

from hypothesis_agent.app.services.job_store import job_store
from hypothesis_agent.app.services.retrieval_service import retrieval_service


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

    job = job_store.create(query)
    job_store.update(job.id, status="processing", progress=10, stage="retrieving evidence")

    snippets = retrieval_service.search(query, top_k=3)
    print(f"[analysis] retrieval_complete elapsed={perf_counter() - start_time:.2f}s snippets={len(snippets)}")

    if len(snippets) < 2:
        response = complete_response(query, job.id, snippets, [], [], [], [])
        job_store.update(job.id, status="complete", progress=100, stage="complete", result=response)
        return response

    job_store.update(job.id, progress=25, stage="assembling evidence")

    evidence_items = []
    nodes_map = {}
    entities_by_snippet = []
    for snippet in snippets:
        snippet_entities = extract_entities(snippet.text)
        entities_by_snippet.append(snippet_entities)
        for entity in snippet_entities:
            nodes_map[entity] = nodes_map.get(entity, 0) + 1
        evidence_items.append(
            {
                "id": snippet.id,
                "doc_id": snippet.doc_id,
                "score": snippet.score,
                "excerpt": snippet.text[:300],
                "entities": snippet_entities,
                "relations_count": 0,
                "used": True,
                "conflict": False,
            }
        )

    nodes = [
        {"id": name, "label": name, "frequency": frequency}
        for name, frequency in nodes_map.items()
    ]
    edges = build_edges(snippets, entities_by_snippet)
    chains = build_chains(edges)
    conflicts = []
    confidence = confidence_from_snippets(snippets, len(edges))
    hypothesis_text = summarize_query(query, nodes, snippets)
    mean_weight = mean([edge["weight"] for edge in edges]) if edges else 0
    result = complete_response(
        query=query,
        job_id=job.id,
        snippets=snippets,
        evidence_items=evidence_items,
        nodes=nodes,
        edges=edges,
        chains=chains,
        conflicts=conflicts,
        hypothesis_text=hypothesis_text,
        confidence=confidence,
        mean_weight=mean_weight,
    )

    job_store.update(job.id, status="complete", progress=100, stage="complete", result=result)
    print(f"[analysis] fast_complete job_id={job.id} elapsed={perf_counter() - start_time:.2f}s")
    return result


def build_edges(snippets, entities_by_snippet):
    edges = []
    seen = set()
    for index, snippet in enumerate(snippets):
        entities = entities_by_snippet[index]
        for source, target in zip(entities, entities[1:]):
            key = (source, target)
            if key in seen:
                continue
            seen.add(key)
            edges.append(
                {
                    "id": f"{len(edges)}",
                    "source": source,
                    "target": target,
                    "polarity": "supports",
                    "weight": round(min(1.0, max(0.2, snippet.score)), 3),
                    "conflict": False,
                }
            )
    return edges[:8]


def build_chains(edges):
    if not edges:
        return []
    chain = []
    for edge in edges[:4]:
        chain.append(f"{edge['source']} → {edge['target']}")
    return [chain]


def confidence_from_snippets(snippets, edge_count):
    average_score = mean([snippet.score for snippet in snippets]) if snippets else 0
    base = int(average_score * 60) + edge_count * 4
    return max(10, min(85, base))


def summarize_query(query, nodes, snippets):
    if not nodes:
        return "Insufficient structured evidence retrieved."
    lead = nodes[0]["id"]
    secondary = nodes[1]["id"] if len(nodes) > 1 else "the retrieved evidence"
    snippet_hint = snippets[0].text[:140].rstrip()
    return (
        f"The evidence suggests {lead} may influence {secondary} in the context of {query.lower()}. "
        f"The strongest retrieved snippet indicates: {snippet_hint}"
    )


def complete_response(
    query,
    job_id,
    snippets,
    evidence_items,
    nodes,
    edges,
    chains,
    conflicts,
    hypothesis_text,
    confidence,
    mean_weight,
):
    return {
        "status": "complete",
        "job_id": job_id,
        "progress": 100,
        "stage": "complete",
        "overview": {
            "total_edges": len(edges),
            "conflicts": len(conflicts),
            "confidence": confidence,
            "strongest_chain": chains[0] if chains else [],
        },
        "evidence": evidence_items,
        "graph": {
            "nodes": nodes,
            "edges": edges,
        },
        "hypothesis": {
            "mechanism": hypothesis_text,
            "supporting_chains": chains[:3],
            "conflicts": conflicts,
            "testable_predictions": build_predictions(query, nodes),
        },
        "metrics": {
            "mean_weight": round(float(mean_weight), 3),
            "reinforcement_factor": min(len(edges) / 5, 1.0),
            "graph_density": round(len(edges) / max(len(nodes), 1), 3),
            "new_metric": 0.5,
        },
    }


def build_predictions(query, nodes):
    if not nodes:
        return []
    anchor = nodes[0]["id"]
    return [
        f"If {anchor} is central to the query, perturbing it should alter the downstream response described by {query.lower()}.",
        f"Independent validation should find the strongest effect near {anchor} rather than distant nodes.",
    ]


def get_job_result(job_id: str):
    job = job_store.get(job_id)
    if job is None:
        return None
    return {
        "job_id": job.id,
        "status": job.status,
        "progress": job.progress,
        "stage": job.stage,
        "query": job.query,
        "result": job.result,
        "error": job.error,
        "created_at": job.created_at,
        "updated_at": job.updated_at,
    }
