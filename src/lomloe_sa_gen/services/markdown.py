from __future__ import annotations

from lomloe_sa_gen.core.models import SASpec


def render_sa_markdown(spec: SASpec) -> str:
    lines: list[str] = []
    lines.append(f"# {spec.titulo}")
    lines.append("")
    lines.append(f"- **Nivel:** {spec.nivel}")
    lines.append(f"- **Materia:** {spec.materia}")
    lines.append("")
    lines.append("## Competencias específicas")
    for c in spec.competencias:
        lines.append(f"- {c}")
    lines.append("")
    lines.append("## Criterios de evaluación")
    for c in spec.criterios:
        lines.append(f"- {c}")
    lines.append("")
    lines.append("## Producto final")
    lines.append(spec.producto_final)
    lines.append("")
    lines.append("## Metodología")
    lines.append(spec.metodologia)
    lines.append("")
    lines.append("## Atención a la diversidad")
    lines.append(spec.atencion_diversidad)
    lines.append("")
    lines.append("## Instrumentos de evaluación")
    for i in spec.instrumentos_evaluacion:
        lines.append(f"- {i}")
    lines.append("")
    lines.append("## Secuenciación de sesiones")
    for idx, s in enumerate(spec.sesiones, start=1):
        lines.append(f"### Sesión {idx}. {s.title} ({s.minutes} min)")
        lines.append(f"- **Actividades:** {s.activities}")
        lines.append(f"- **Evidencia:** {s.evidence}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"
