from __future__ import annotations

import io
import zipfile


def build_zip(files: dict[str, bytes]) -> bytes:
    """
    files: mapping {filename: content_bytes}
    """
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name, content in files.items():
            zf.writestr(name, content)
    return buffer.getvalue()
