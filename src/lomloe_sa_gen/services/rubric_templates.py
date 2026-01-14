from __future__ import annotations

import json
from dataclasses import dataclass
from importlib.resources import files
from typing import Any


@dataclass(frozen=True)
class RubricTemplate:
    id: str
    label: str
    levels: list[str]
    descriptor_patterns: list[str]  # longitud 4


def _templates_dir():
    return files("lomloe_sa_gen").joinpath("assets/rubric_templates")


def list_rubric_templates() -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for p in _templates_dir().iterdir():
        if p.is_file() and p.name.endswith(".json"):
            data = json.loads(p.read_text(encoding="utf-8"))
            items.append({"id": data["id"], "label": data["label"]})
    # Orden estable por label
    items.sort(key=lambda x: x["label"].lower())
    return items


def load_rubric_template(template_id: str) -> RubricTemplate:
    path = _templates_dir().joinpath(f"{template_id}.json")
    if not path.is_file():
        raise FileNotFoundError(f"No existe la plantilla de rúbrica: {template_id}")

    data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))

    levels = data["levels"]
    patterns = data["descriptor_patterns"]
    if len(levels) != 4 or len(patterns) != 4:
        raise ValueError("La plantilla de rúbrica debe tener exactamente 4 niveles y 4 patrones.")

    return RubricTemplate(
        id=data["id"],
        label=data["label"],
        levels=levels,
        descriptor_patterns=patterns,
    )
