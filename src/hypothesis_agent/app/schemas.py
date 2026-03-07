from pydantic import BaseModel
from typing import List


class QueryRequest(BaseModel):
    query: str


class Overview(BaseModel):
    total_edges: int
    conflicts: int
    confidence: int
    strongest_chain: List[str]


class EvidenceItem(BaseModel):
    id: str
    doc_id: str
    score: float
    excerpt: str
    entities: List[str]
    relations_count: int
    used: bool
    conflict: bool


class GraphNode(BaseModel):
    id: str
    label: str
    frequency: int


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    polarity: str
    weight: float
    conflict: bool


class HypothesisSection(BaseModel):
    mechanism: str
    supporting_chains: List[List[str]]
    conflicts: List[str]
    testable_predictions: List[str]


class Metrics(BaseModel):
    mean_weight: float
    reinforcement_factor: float
    graph_density: float


class AnalysisResponse(BaseModel):
    overview: Overview
    evidence: List[EvidenceItem]
    graph: dict
    hypothesis: HypothesisSection
    metrics: Metrics