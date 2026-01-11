from lomloe_sa_gen.core.models import SASpec, SessionSpec
from lomloe_sa_gen.services.markdown import render_sa_markdown


def test_render_sa_markdown_contains_sections():
    spec = SASpec(
        nivel="1º Bachillerato",
        materia="Tecnología e Ingeniería I",
        titulo="SA de prueba",
        competencias=["CE1"],
        criterios=["C1"],
        producto_final="Un prototipo sencillo.",
        metodologia="ABP y trabajo cooperativo.",
        atencion_diversidad="Medidas ordinarias.",
        instrumentos_evaluacion=["Rúbrica"],
        sesiones=[
            SessionSpec(
                title="Introducción",
                minutes=55,
                activities="Presentación y grupos.",
                evidence="Lista de roles",
            )
        ],
    )
    md = render_sa_markdown(spec)
    assert "# SA de prueba" in md
    assert "## Competencias específicas" in md
    assert "## Secuenciación de sesiones" in md
