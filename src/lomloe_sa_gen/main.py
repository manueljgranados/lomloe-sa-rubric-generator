from pathlib import Path
import json

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from fastapi.templating import Jinja2Templates

from lomloe_sa_gen.core.models import SASpec, SessionSpec
from lomloe_sa_gen.services.markdown import render_sa_markdown

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "adapters" / "web" / "templates"))


def _split_lines(text: str) -> list[str]:
    return [x.strip() for x in (text or "").splitlines() if x.strip()]


def create_app() -> FastAPI:
    app = FastAPI(title="Generador SA + Rúbricas (LOMLOOE)", version="0.1.0")

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
    ):
        try:
            sessions_raw = json.loads(sessions_json)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail=f"sessions_json inválido: {e.msg}") from e

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

        md = render_sa_markdown(spec, template_type="sa_generic")

        return Response(
            content=md,
            media_type="text/markdown; charset=utf-8",
            headers={"Content-Disposition": 'attachment; filename="situacion_aprendizaje.md"'},
        )

    return app


app = create_app()
