from importlib.resources import files


def test_docx_template_exists():
    template = files("lomloe_sa_gen").joinpath("assets/templates/sa_template.docx")
    assert template.is_file()
