from __future__ import annotations

import re
import unicodedata

from lomloe_sa_gen.core.models import SASpec


def slugify(text: str, max_len: int = 80) -> str:
    text = text.strip()
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    text = re.sub(r"-{2,}", "-", text)
    text = text[:max_len].strip("-")
    return text or "sa"


def pack_basename(spec: SASpec) -> str:
    return f"{slugify(spec.nivel)}__{slugify(spec.titulo, max_len=100)}"
