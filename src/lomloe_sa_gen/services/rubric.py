from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from lomloe_sa_gen.core.models import SASpec
from lomloe_sa_gen.services.template_renderer import TemplateRenderer


@dataclass(frozen=True)
class RubricRow:
    criterion: str
    descriptors: list[str]


def _default_levels() -> list[str]:
    return ["4 - Excelente", "3 - Notable", "2 - Suficiente", "1 - En proceso"]


def _build_rows(spec: SASpec) -> list[RubricRow]:
    placeholder = "Definir descriptor."
    return [
        RubricRow(criterion=c, descriptors=[placeholder, placeholder, placeholder, placeholder])
        for c in spec.criterios
    ]


def render_rubric_markdown(spec: SASpec, template_type: str = "sa_generic") -> str:
    templates_root = Path(__file__).resolve().parent.parent / "templates"
    renderer = TemplateRenderer(templates_root=templates_root)

    context = spec.model_dump()
    context["rubric_levels"] = _default_levels()
    context["rubric_rows"] = [r.__dict__ for r in _build_rows(spec)]

    template_path = f"{template_type}/rubric.md.j2"
    return renderer.render(template_path=template_path, context=context)
