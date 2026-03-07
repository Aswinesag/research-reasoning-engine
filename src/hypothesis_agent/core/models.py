from dataclasses import dataclass

@dataclass
class EvidenceSnippet:
    id: int
    doc_id: str
    text: str
    score: float