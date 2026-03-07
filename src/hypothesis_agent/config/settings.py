import os
from dotenv import load_dotenv
from .schema import AppConfig

load_dotenv()

def load_config() -> AppConfig:
    return AppConfig(
        environment=os.getenv("ENVIRONMENT", "dev"),
        model={
            "model_name": os.getenv("MODEL_NAME"),
            "temperature": float(os.getenv("TEMPERATURE", 0.2)),
            "max_tokens": int(os.getenv("MAX_TOKENS", 1024)),
        },
        debate={"rounds": 3},
        scoring={
            "novelty_weight": 0.4,
            "consistency_weight": 0.3,
            "plausibility_weight": 0.3,
        }
    )