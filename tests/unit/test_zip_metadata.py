import io
import json
import zipfile

from lomloe_sa_gen.services.packaging import build_zip


def test_zip_contains_metadata_json():
    z = build_zip({"x__metadata.json": b'{"ok": true}'})
    with zipfile.ZipFile(io.BytesIO(z)) as zf:
        data = json.loads(zf.read("x__metadata.json").decode("utf-8"))
        assert data["ok"] is True
