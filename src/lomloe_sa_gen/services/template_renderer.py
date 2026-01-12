from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined


class TemplateRenderer:
    def __init__(self, templates_root: Path) -> None:
        self._env = Environment(
            loader=FileSystemLoader(str(templates_root)),
            autoescape=False,  # Markdown
            undefined=StrictUndefined,  # falla si falta un campo
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render(self, template_path: str, context: dict) -> str:
        tmpl = self._env.get_template(template_path)
        return tmpl.render(**context).strip() + "\n"
