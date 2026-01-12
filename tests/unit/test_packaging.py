import io
import zipfile

from lomloe_sa_gen.services.packaging import build_zip


def test_build_zip_contains_files():
    z = build_zip({"a.txt": b"hello", "b.txt": b"world"})
    with zipfile.ZipFile(io.BytesIO(z)) as zf:
        assert set(zf.namelist()) == {"a.txt", "b.txt"}
        assert zf.read("a.txt") == b"hello"
