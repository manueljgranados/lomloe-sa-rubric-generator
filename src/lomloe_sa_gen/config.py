import os
from dataclasses import dataclass


def _as_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Settings:
    llm_enabled: bool = _as_bool(os.getenv("LLM_ENABLED", "false"))
    llm_provider: str = os.getenv("LLM_PROVIDER", "disabled")  # disabled|openai|azure|...
