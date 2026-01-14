from __future__ import annotations

from lomloe_sa_gen.config import Settings
from lomloe_sa_gen.adapters.llm.providers import DisabledProvider, RulesProvider, SuggestProvider


def get_suggest_provider(settings: Settings) -> SuggestProvider:
    if not settings.llm_enabled:
        return DisabledProvider()

    provider = settings.llm_provider.strip().lower()
    if provider == "rules":
        return RulesProvider()

    # Placeholder para LLM real (OpenAI/Azure/Ollama) sin tocar el núcleo:
    # si no está implementado, degradamos a disabled de forma segura.
    return DisabledProvider()
