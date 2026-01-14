import pytest
from lomloe_sa_gen.core.models import RubricSpec


def test_rubric_spec_valid():
    r = RubricSpec(
        levels=["L1 ok", "L2 ok", "L3 ok", "L4 ok"],
        rows=[{"criterion": "C1 criterio", "descriptors": ["aaa", "bbb", "ccc", "ddd"]}],
    )
    assert r.levels[0] == "L1 ok"


def test_rubric_spec_invalid_levels():
    with pytest.raises(Exception):
        RubricSpec(
            levels=["x", "y", "z", "w"],
            rows=[{"criterion": "C1", "descriptors": ["aa", "bb", "cc", "dd"]}],
        )
