from lomloe_sa_gen.services.rubric_templates import list_rubric_templates, load_rubric_template


def test_list_templates_non_empty():
    items = list_rubric_templates()
    assert any(i["id"] == "proyecto" for i in items)


def test_load_template_levels_patterns_len():
    t = load_rubric_template("proyecto")
    assert len(t.levels) == 4
    assert len(t.descriptor_patterns) == 4
