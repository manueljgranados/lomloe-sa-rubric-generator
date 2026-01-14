from pathlib import Path
import json

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, Response, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from lomloe_sa_gen.core.models import SASpec, SessionSpec, RubricSpec
from lomloe_sa_gen.services.markdown import render_sa_markdown

from pydantic import ValidationError, BaseModel, Field

from lomloe_sa_gen.config import Settings
from lomloe_sa_gen.services.suggest_factory import get_suggest_provider
from lomloe_sa_gen.services.docx_template_export import export_sa_docx_from_template
from lomloe_sa_gen.services.metadata import build_metadata
from lomloe_sa_gen.services.naming import pack_basename
from lomloe_sa_gen.services.packaging import build_zip
from lomloe_sa_gen.services.rubric import render_rubric_markdown


BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "adapters" / "web" / "templates"))


def _split_lines(text: str) -> list[str]:
    return [x.strip() for x in (text or "").splitlines() if x.strip()]


def create_app() -> FastAPI:
    app = FastAPI(title="Generador SA + Rúbricas (LOMLOOE)", version="0.1.0")

    class RubricSuggestRequest(BaseModel):
        criterios: list[str] = Field(..., min_length=1)
        levels: list[str] = Field(..., min_length=4, max_length=4)
        context: str = ""  # materia/nivel/titulo (texto libre)

    @app.post("/rubric/suggest")
    def rubric_suggest(payload: RubricSuggestRequest):
        settings = Settings()
        provider = get_suggest_provider(settings)

        descriptors = provider.suggest(payload.criterios, payload.levels, payload.context)

        rubric_dict = {
            "levels": payload.levels,
            "rows": [
                {"criterion": c, "descriptors": d}
                for c, d in zip(payload.criterios, descriptors, strict=False)
            ],
            "provider": provider.name,
        }
        return JSONResponse(rubric_dict)

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    @app.get("/demo")
    def demo_redirect():
        return RedirectResponse(url="/")

    @app.get("/", response_class=HTMLResponse)
    def home(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    @app.post("/generate")
    def generate(
        nivel: str = Form(...),
        materia: str = Form(...),
        titulo: str = Form(...),
        competencias: str = Form(...),
        criterios: str = Form(...),
        producto_final: str = Form(...),
        metodologia: str = Form(...),
        atencion_diversidad: str = Form(...),
        instrumentos_evaluacion: str = Form(...),
        sessions_json: str = Form(...),
        resumen: str = Form(""),
        rubric_json: str = Form(""),
    ):
        try:
            sessions_raw = json.loads(sessions_json)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail=f"sessions_json inválido: {e.msg}") from e

        try:
            sessions = [SessionSpec(**s) for s in sessions_raw]
            spec = SASpec(
                nivel=nivel,
                materia=materia,
                titulo=titulo,
                competencias=_split_lines(competencias),
                criterios=_split_lines(criterios),
                producto_final=producto_final.strip(),
                metodologia=metodologia.strip(),
                atencion_diversidad=atencion_diversidad.strip(),
                instrumentos_evaluacion=_split_lines(instrumentos_evaluacion),
                sesiones=sessions,
            )
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.errors()) from e

        rubric: RubricSpec | None = None
        if rubric_json.strip():
            try:
                rubric = RubricSpec(**json.loads(rubric_json))
            except json.JSONDecodeError as e:
                raise HTTPException(status_code=400, detail=f"rubric_json inválido: {e.msg}") from e
            except ValidationError as e:
                raise HTTPException(status_code=422, detail=e.errors()) from e

        basename = pack_basename(spec)

        sa_md = render_sa_markdown(spec, template_type="sa_generic")
        rubric_md = render_rubric_markdown(spec, rubric=rubric, template_type="sa_generic")

        docx_bytes = export_sa_docx_from_template(spec, resumen=resumen, rubric=rubric)

        resumen_text = (resumen or "").strip()
        if not resumen_text:
            from lomloe_sa_gen.services.docx_template_export import _auto_summary

            resumen_text = _auto_summary(spec)

        rubric_for_meta = json.loads(rubric_json) if rubric_json.strip() else None
        metadata = build_metadata(spec, resumen=resumen_text, rubric=rubric_for_meta)
        metadata_bytes = json.dumps(metadata, ensure_ascii=False, indent=2).encode("utf-8")

        zip_bytes = build_zip(
            {
                f"{basename}.md": sa_md.encode("utf-8"),
                f"{basename}__rubrica.md": rubric_md.encode("utf-8"),
                f"{basename}.docx": docx_bytes,
                f"{basename}__metadata.json": metadata_bytes,
            }
        )

        return Response(
            content=zip_bytes,
            media_type="application/zip",
            headers={"Content-Disposition": 'attachment; filename="{basename}.zip"'},
        )

    return app


app = create_app()
