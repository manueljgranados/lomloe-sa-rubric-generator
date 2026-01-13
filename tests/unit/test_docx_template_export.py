import io
from docx import Document

from lomloe_sa_gen.core.models import SASpec, SessionSpec
from lomloe_sa_gen.services.docx_template_export import export_sa_docx_from_template


def test_docx_from_template_contains_title():
    spec = SASpec(
        nivel="1º Bachillerato",
        materia="Tecnología e Ingeniería I",
        titulo="SA Plantilla",
        competencias=["CE1"],
        criterios=["C1. Un criterio suficientemente descriptivo."],
        producto_final="Producto final suficientemente descriptivo.",
        metodologia="Metodología suficientemente descriptiva.",
        atencion_diversidad="Atención a la diversidad suficientemente descriptiva.",
        instrumentos_evaluacion=["Rúbrica"],
        sesiones=[
            SessionSpec(
                title="Intro", minutes=55, activities="Actividades largas.", evidence="Evidencia"
            )
        ],
    )
    data = export_sa_docx_from_template(spec, resumen="Resumen suficientemente descriptivo.")
    doc = Document(io.BytesIO(data))
    assert any("SA Plantilla" in p.text for p in doc.paragraphs)
