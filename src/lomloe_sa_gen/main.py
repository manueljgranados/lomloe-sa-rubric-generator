from pathlib import Path

from fastapi import FastAPI, Request, Form
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
        s1_title: str = Form(...),
        s1_minutes: int = Form(...),
        s1_activities: str = Form(...),
        s1_evidence: str = Form(...),
        s2_title: str = Form(...),
        s2_minutes: int = Form(...),
        s2_activities: str = Form(...),
        s2_evidence: str = Form(...),
        s3_title: str = Form(...),
        s3_minutes: int = Form(...),
        s3_activities: str = Form(...),
        s3_evidence: str = Form(...),
    ):
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
            sesiones=[
                SessionSpec(
                    title=s1_title.strip(),
                    minutes=s1_minutes,
                    activities=s1_activities.strip(),
                    evidence=s1_evidence.strip(),
                ),
                SessionSpec(
                    title=s2_title.strip(),
                    minutes=s2_minutes,
                    activities=s2_activities.strip(),
                    evidence=s2_evidence.strip(),
                ),
                SessionSpec(
                    title=s3_title.strip(),
                    minutes=s3_minutes,
                    activities=s3_activities.strip(),
                    evidence=s3_evidence.strip(),
                ),
            ],
        )

        md = render_sa_markdown(spec)

        filename = "situacion_aprendizaje.md"
        return Response(
            content=md,
            media_type="text/markdown; charset=utf-8",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    return app


app = create_app()
