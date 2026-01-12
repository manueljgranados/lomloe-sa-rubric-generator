from lomloe_sa_gen.core.models import SASpec, SessionSpec
from lomloe_sa_gen.services.rubric import render_rubric_markdown


def test_render_rubric_contains_table_header():
    spec = SASpec(
        nivel="1º Bachillerato",
        materia="Tecnología e Ingeniería I",
        titulo="SA rúbrica",
        competencias=["CE1"],
        criterios=["C1. Un criterio."],
        producto_final="Producto final suficientemente descriptivo.",
        metodologia="Metodología suficientemente descriptiva.",
        atencion_diversidad="Atención a la diversidad detallada.",
        instrumentos_evaluacion=["Rúbrica"],
        sesiones=[
            SessionSpec(
                title="Intro", minutes=55, activities="Actividades largas.", evidence="Evidencia"
            )
        ],
    )
    md = render_rubric_markdown(spec)
    assert "| Criterio |" in md
    assert "Rúbrica — SA rúbrica" in md
