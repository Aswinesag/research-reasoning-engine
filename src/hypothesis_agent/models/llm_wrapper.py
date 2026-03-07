import time
import json
import structlog
from core.exceptions import (
    LLMError,
    LLMTimeoutError,
    LLMOutputValidationError
)

logger = structlog.get_logger()

class LLMWrapper:
    def __init__(self, client, model_name: str, temperature: float, timeout: int = 30):
        self.client = client
        self.model_name = model_name
        self.temperature = temperature
        self.timeout = timeout

    def generate(self, prompt: str, max_tokens: int = 1024, expect_json: bool = False):
        start_time = time.time()

        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                temperature=self.temperature,
                max_tokens=max_tokens,
                timeout=self.timeout,
            )

            latency = time.time() - start_time

            if not isinstance(response, str):
                raise LLMOutputValidationError("Response is not string")

            cleaned = response.strip()

            if expect_json:
                try:
                    parsed = json.loads(cleaned)
                except json.JSONDecodeError:
                    raise LLMOutputValidationError("Invalid JSON output")

                logger.info(
                    "llm_call_success",
                    latency=latency,
                    tokens=len(cleaned.split()),
                    json=True
                )

                return parsed

            logger.info(
                "llm_call_success",
                latency=latency,
                tokens=len(cleaned.split()),
                json=False
            )

            return cleaned

        except TimeoutError:
            logger.error("llm_timeout")
            raise LLMTimeoutError("LLM request timed out")

        except Exception as e:
            logger.error("llm_failure", error=str(e))
            raise LLMError(str(e))