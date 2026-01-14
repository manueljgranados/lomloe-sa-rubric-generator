from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class SessionSpec(BaseModel):
    title: str = Field(..., min_length=3, description="Título de la sesión")
    minutes: int = Field(..., ge=10, le=240, description="Duración aproximada en minutos")
    activities: str = Field(..., min_length=10, description="Actividades principales")
    evidence: str = Field(..., min_length=5, description="Evidencia / producto / entregable")


class SASpec(BaseModel):
    nivel: str = Field(..., min_length=2)
    materia: str = Field(..., min_length=3)
    titulo: str = Field(..., min_length=5)

    competencias: list[str] = Field(default_factory=list, min_length=1)
    criterios: list[str] = Field(default_factory=list, min_length=1)

    sesiones: list[SessionSpec] = Field(default_factory=list, min_length=1)

    producto_final: str = Field(..., min_length=10)
    metodologia: str = Field(..., min_length=10)
    atencion_diversidad: str = Field(..., min_length=10)
    instrumentos_evaluacion: list[str] = Field(default_factory=list, min_length=1)

    @field_validator("competencias", "criterios", "instrumentos_evaluacion")
    @classmethod
    def strip_and_drop_empty(cls, v: list[str]) -> list[str]:
        cleaned = [x.strip() for x in v if x and x.strip()]
        if not cleaned:
            raise ValueError("Debe incluir al menos un elemento.")
        return cleaned


class RubricRowSpec(BaseModel):
    criterion: str = Field(..., min_length=3)
    descriptors: list[str] = Field(..., min_length=4, max_length=4)

    @field_validator("descriptors")
    @classmethod
    def descriptors_non_empty(cls, v: list[str]) -> list[str]:
        cleaned = [x.strip() for x in v]
        if any(len(x) < 3 for x in cleaned):
            raise ValueError("Cada descriptor debe tener al menos 3 caracteres.")
        return cleaned


class RubricSpec(BaseModel):
    levels: list[str] = Field(..., min_length=4, max_length=4)
    rows: list[RubricRowSpec] = Field(..., min_length=1)

    @field_validator("levels")
    @classmethod
    def levels_non_empty(cls, v: list[str]) -> list[str]:
        cleaned = [x.strip() for x in v]
        if any(len(x) < 3 for x in cleaned):
            raise ValueError("Cada nivel debe tener al menos 3 caracteres.")
        return cleaned
