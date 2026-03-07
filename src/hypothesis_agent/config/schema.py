from pydantic import BaseModel, Field
from typing import Literal

class ModelConfig(BaseModel):
    model_name: str
    temperature: float = Field(ge=0.0, le=1.0)
    max_tokens: int

class DebateConfig(BaseModel):
    rounds: int = Field(default=3, ge=1, le=5)

class ScoringConfig(BaseModel):
    novelty_weight: float
    consistency_weight: float
    plausibility_weight: float

class AppConfig(BaseModel):
    environment: Literal["dev", "prod"]
    model: ModelConfig
    debate: DebateConfig
    scoring: ScoringConfig