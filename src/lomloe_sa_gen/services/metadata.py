from __future__ import annotations

from datetime import datetime, timezone

from lomloe_sa_gen.core.models import SASpec


def build_metadata(spec: SASpec, resumen: str, rubric: dict | None = None) -> dict:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "app": {"name": "lomloe-sa-gen", "template": "sa_template.docx"},
        "input": spec.model_dump(),
        "derived": {"resumen": resumen, "rubric": rubric},
    }
