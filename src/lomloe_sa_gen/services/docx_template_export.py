from __future__ import annotations

import io
from datetime import date, datetime
from importlib.resources import as_file, files

from docxtpl import DocxTemplate

from lomloe_sa_gen.core.models import SASpec, RubricSpec
from lomloe_sa_gen.services.rubric import default_levels, build_default_rows


def _auto_summary(spec: SASpec) -> str:
    return (
        f"Situación de aprendizaje para {spec.nivel} en {spec.materia}, "
        f"con {len(spec.sesiones)} sesiones. Producto final: {spec.producto_final}"
    )


def export_sa_docx_from_template(
    spec: SASpec, resumen: str | None = None, rubric: RubricSpec | None = None
) -> bytes:
    template = files("lomloe_sa_gen").joinpath("assets/templates/sa_template.docx")
    resumen_text = (resumen or "").strip() or _auto_summary(spec)

    context = spec.model_dump()
    context.update(
        {
            "fecha": date.today().isoformat(),
            "resumen": resumen_text,
            "footer_text": f"{spec.materia} · {spec.nivel} · {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        }
    )

    if rubric is None:
        context["rubric_levels"] = default_levels()
        context["rubric_rows"] = [r.__dict__ for r in build_default_rows(spec)]
    else:
        context["rubric_levels"] = rubric.levels
        context["rubric_rows"] = [r.model_dump() for r in rubric.rows]

    bio = io.BytesIO()
    with as_file(template) as template_path:
        doc = DocxTemplate(str(template_path))
        doc.render(context)
        doc.save(bio)
    return bio.getvalue()
