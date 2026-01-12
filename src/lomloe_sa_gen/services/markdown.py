from __future__ import annotations

from pathlib import Path

from lomloe_sa_gen.core.models import SASpec
from lomloe_sa_gen.services.template_renderer import TemplateRenderer


def render_sa_markdown(spec: SASpec, template_type: str = "sa_generic") -> str:
    templates_root = Path(__file__).resolve().parent.parent / "templates"
    renderer = TemplateRenderer(templates_root=templates_root)

    context = spec.model_dump()
    template_path = f"{template_type}/sa.md.j2"
    return renderer.render(template_path=template_path, context=context)
