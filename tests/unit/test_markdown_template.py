from lomloe_sa_gen.core.models import SASpec, SessionSpec
from lomloe_sa_gen.services.markdown import render_sa_markdown


def test_render_sa_markdown_uses_template():
    spec = SASpec(
        nivel="1º Bachillerato",
        materia="Tecnología e Ingeniería I",
        titulo="SA plantilla",
        competencias=["CE1"],
        criterios=["C1"],
        producto_final="Producto final.",
        metodologia="Metodología.",
        atencion_diversidad="Atención ordinaria.",
        instrumentos_evaluacion=["Rúbrica"],
        sesiones=[
            SessionSpec(title="Sesión", minutes=55, activities="Actividades.", evidence="Evidencia")
        ],
    )
    md = render_sa_markdown(spec, template_type="sa_generic")
    assert "# SA plantilla" in md
    assert "## Secuenciación de sesiones" in md
    assert "Sesión 1." in md
