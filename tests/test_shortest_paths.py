import pytest

from project.shortest_paths import *
from tests.utils import load_json

shortest_paths_filename = "tests/src/test_shortest_paths.json"


@pytest.mark.parametrize(
    "I, J, V, start, expected",
    [
        (test["I"], test["J"], test["V"], test["start"], test["expected"])
        for test in load_json(shortest_paths_filename, "single_bellman_ford")
    ],
)
def test_single_bellman_ford(I, J, V, start, expected):
    matrix = Matrix.from_lists(I, J, V)
    expected = [float(i) for i in expected]
    assert single_bellman_ford(matrix, start) == expected


@pytest.mark.parametrize(
    "I, J, V, start, expected",
    [
        (test["I"], test["J"], test["V"], test["start"], test["expected"])
        for test in load_json(shortest_paths_filename, "multiple_bellman_ford")
    ],
)
def test_multiple_bellman_ford(I, J, V, start, expected):
    matrix = Matrix.from_lists(I, J, V)
    expected = [(i, [float(k) for k in j]) for [i, j] in expected]
    assert multiple_bellman_ford(matrix, start) == expected


@pytest.mark.parametrize(
    "I, J, V, expected",
    [
        (test["I"], test["J"], test["V"], test["expected"])
        for test in load_json(shortest_paths_filename, "floyd_warshall")
    ],
)
def test_floyd_warshall(I, J, V, expected):
    matrix = Matrix.from_lists(I, J, V)
    expected = [(i, [float(k) for k in j]) for [i, j] in expected]
    assert floyd_warshall(matrix) == expected
