from __future__ import annotations

from datetime import datetime, timezone

from lomloe_sa_gen.core.models import SASpec


def build_metadata(
    spec: SASpec, resumen: str, rubric: dict | None = None, rubric_type: str = "proyecto"
) -> dict:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "app": {"name": "lomloe-sa-gen"},
        "input": spec.model_dump(),
        "derived": {
            "resumen": resumen,
            "rubric": rubric,
            "rubric_type": rubric_type,
        },
    }
