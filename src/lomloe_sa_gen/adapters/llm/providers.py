from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class SuggestProvider(Protocol):
    name: str

    def suggest(self, criterios: list[str], levels: list[str], context: str) -> list[list[str]]:
        """Devuelve descriptores [n_criterios][4]."""
        ...


@dataclass(frozen=True)
class DisabledProvider:
    name: str = "disabled"

    def suggest(self, criterios: list[str], levels: list[str], context: str) -> list[list[str]]:
        placeholder = "Definir descriptor."
        return [[placeholder, placeholder, placeholder, placeholder] for _ in criterios]


@dataclass(frozen=True)
class RulesProvider:
    name: str = "rules"

    def suggest(self, criterios: list[str], levels: list[str], context: str) -> list[list[str]]:
        # Offline y determinista (sirve como “IA” sin dependencias externas).
        out: list[list[str]] = []
        for c in criterios:
            out.append(
                [
                    f"Demuestra un desempeño excelente respecto a: {c}. Evidencias claras y justificadas.",
                    f"Cumple de forma notable: {c}. Evidencias suficientes y coherentes.",
                    f"Alcanza lo mínimo en: {c}. Evidencias parciales o con alguna imprecisión.",
                    f"En proceso en: {c}. Necesita apoyo y mejora para aportar evidencias.",
                ]
            )
        return out
