import pytest

from project.triangles import *
from tests.utils import load_json

triangles_filename = "tests/src/test_triangles.json"


def get_test_data():
    return [
        (test["I"], test["J"], test["expected"])
        for test in load_json(triangles_filename, "triangles")
    ]


@pytest.mark.parametrize("I, J, expected", get_test_data())
def test_naive_count_triangles(I, J, expected):
    matrix = Matrix.from_lists(I, J)
    assert naive_count_triangles(matrix) == expected


@pytest.mark.parametrize("I, J,  expected", get_test_data())
def test_cohen(I, J, expected):
    matrix = Matrix.from_lists(I, J)
    assert cohen(matrix) == sum(expected) / 3


@pytest.mark.parametrize("I, J, expected", get_test_data())
def test_sandia(I, J, expected):
    matrix = Matrix.from_lists(I, J)
    assert sandia(matrix) == sum(expected) / 3


def test_triangles_for_directed_graph():
    matrix = Matrix.from_lists([0, 1, 2], [1, 2, 0])
    with pytest.raises(TypeError):
        naive_count_triangles(matrix)
        cohen(matrix)
        sandia(matrix)
