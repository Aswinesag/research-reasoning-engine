import os
import json
import numpy as np
from typing import List
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv

from hypothesis_agent.reasoning.causal_graph import CausalGraph, Edge
from hypothesis_agent.core.models import EvidenceSnippet

load_dotenv(override=True)

MODEL_NAME = "llama-3.1-8b-instant"
TEMPERATURE = 0.3
GROQ_TIMEOUT_SECONDS = 20.0


class HypothesisGenerator:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key or api_key == "your_api_key":
            raise ValueError("Valid GROQ_API_KEY not set")

        self.client = Groq(
            api_key=api_key,
            timeout=GROQ_TIMEOUT_SECONDS,
            max_retries=0,
        )

    def _call_groq(self, prompt: str, temperature: float):
        try:
            return self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
            )
        except Exception as exc:
            raise TimeoutError(f"Groq request failed or timed out after {GROQ_TIMEOUT_SECONDS}s") from exc

    # ===================================================
    # 1️⃣ STRICT RELATION EXTRACTION
    # ===================================================

    def extract_relations(self, text: str):

        prompt = (
            "Extract only explicit directed causal biological relations from the text. "
            "Return strict JSON array only with objects: {source, target, polarity}. "
            "Polarity must be '+' or '-'. Return [] if none. "
            f"Text: {text}"
        )

        response = self._call_groq(prompt, temperature=0.0)

        content = response.choices[0].message.content.strip()

        # Remove markdown fences if present
        if content.startswith("```"):
            content = content.split("```")[1]

        # Extract JSON safely
        start = content.find("[")
        end = content.rfind("]")

        if start == -1 or end == -1:
            return []

        json_str = content[start:end + 1]

        try:
            data = json.loads(json_str)

            # Schema validation
            clean_relations = []
            for item in data:
                if (
                    isinstance(item, dict)
                    and "source" in item
                    and "target" in item
                    and "polarity" in item
                    and item["polarity"] in ["+", "-"]
                ):
                    clean_relations.append(item)

            return clean_relations

        except Exception:
            return []

    # ===================================================
    # 2️⃣ BUILD CAUSAL GRAPH
    # ===================================================

    def build_graph(self, snippets: List[EvidenceSnippet]) -> CausalGraph:

        graph = CausalGraph()

        for snippet in snippets:

            relations = self.extract_relations(snippet.text)

            for rel in relations:

                edge = Edge(
                    source=rel["source"],
                    target=rel["target"],
                    polarity=rel["polarity"],
                    evidence_id=snippet.id,
                    weight=snippet.score,
                    excerpt=snippet.text[:250],
                    doc_id=snippet.doc_id
                )

                graph.add_edge(edge)

        return graph

    # ===================================================
    # 3️⃣ INTEGRATED EVIDENCE SECTION
    # ===================================================

    def build_integrated_evidence_section(self, graph: CausalGraph):

        edge_map = {}

        for edge in graph.get_edges():
            key = (edge.source, edge.target, edge.polarity)
            edge_map.setdefault(key, []).append(edge)

        section = "\n### Integrated Evidence\n"

        for (source, target, polarity), edges in edge_map.items():

            section += f"\nEdge: {source} ({polarity})→ {target}\n"

            for e in edges:
                section += (
                    f"- Evidence ID: {e.evidence_id}\n"
                    f"  Document ID: {e.doc_id}\n"
                    f"  Similarity Score: {e.weight:.3f}\n"
                    f"  Excerpt: \"{e.excerpt}\"\n"
                )

        return section

    # ===================================================
    # 4️⃣ GRAPH-DRIVEN HYPOTHESIS GENERATION
    # ===================================================

    def generate_from_graph(self, graph: CausalGraph):

        edges = graph.get_edges()

        if not edges:
            raise ValueError(
                "No causal relations extracted. Aborting to prevent hallucinated hypothesis."
            )

        chains = graph.find_chains(depth=3)
        conflicts = graph.detect_conflicts()

        # Build edge text
        edge_text = ""
        for e in edges:
            edge_text += (
                f"{e.source} ({e.polarity})→ {e.target} "
                f"[evidence {e.evidence_id}, weight={e.weight:.2f}]\n"
            )

        # Build chain text
        chain_text = "\n".join(
            [" → ".join(chain) for chain in chains[:10]]
        )

        # Restrict entity space (anti-hallucination)
        entity_set = list(
            set([e.source for e in edges] + [e.target for e in edges])
        )

        prompt = (
            "Generate a concise research hypothesis using only the allowed entities. "
            "Use the causal edges, chains, and conflicts as grounding. "
            "Keep the answer direct and testable.\n"
            f"Allowed entities: {entity_set}\n"
            f"Causal edges: {edge_text}\n"
            f"Chains: {chain_text}\n"
            f"Conflicts: {conflicts}"
        )

        response = self._call_groq(prompt, temperature=TEMPERATURE)

        return response.choices[0].message.content, conflicts

    # ===================================================
    # 5️⃣ GRAPH-BASED CONFIDENCE SCORING
    # ===================================================

    def compute_confidence(self, graph: CausalGraph, conflicts):

        edges = graph.get_edges()

        if not edges:
            return 0

        mean_weight = np.mean([e.weight for e in edges])

        reinforcement_factor = min(len(edges) / 5, 1.0)

        conflict_penalty = 0.2 if conflicts else 0.0

        confidence = int(
            max(
                0,
                (0.6 * mean_weight + 0.4 * reinforcement_factor - conflict_penalty)
                * 100
            )
        )

        return confidence

    # ===================================================
    # 6️⃣ MAIN ENTRYPOINT
    # ===================================================

    def generate(self, query: str, snippets: List[EvidenceSnippet]):

        if len(snippets) < 2:
            raise ValueError("Need at least two snippets for graph synthesis.")

        # 1️⃣ Build graph
        graph = self.build_graph(snippets)

        # Fail fast if extraction failed
        if len(graph.get_edges()) == 0:
            raise ValueError(
                "No causal relations extracted. Check relation extraction prompt or model output."
            )

        # 2️⃣ Integrated evidence
        integrated_evidence = self.build_integrated_evidence_section(graph)

        # 3️⃣ Hypothesis generation
        hypothesis_text, conflicts = self.generate_from_graph(graph)

        # 4️⃣ Confidence scoring
        confidence = self.compute_confidence(graph, conflicts)

        metadata = f"""
### Graph Metadata
Total edges: {len(graph.get_edges())}
Conflicts detected: {len(conflicts)}
Model: {MODEL_NAME}
Temperature: {TEMPERATURE}
Timestamp: {datetime.utcnow().isoformat()} UTC

### Confidence Score (Graph-Based)
{confidence}%
"""

        final_output = (
            integrated_evidence
            + "\n\n"
            + hypothesis_text
            + "\n\n"
            + metadata
        )

        return final_output
