import pytest

from project.bfs import *
from tests.utils import load_json


@pytest.mark.parametrize(
    "I, J, start_vertex, expected",
    [
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8, 0],
            0,
            [0, 1, 2, 3, 4, 5, 6, 7, 8],
        ),
        (
            [0, 1, 3, 2, 4, 5, 7, 6],
            [1, 3, 2, 1, 5, 7, 6, 4],
            0,
            [0, 1, 3, 2, -1, -1, -1, -1],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8, 2],
            5,
            [-1, -1, 4, 5, 6, 0, 1, 2, 3],
        ),
    ],
)
def test_bfs(I, J, start_vertex, expected):
    matrix = Matrix.from_lists(I, J)
    assert bfs(matrix, start_vertex) == expected


msbfs_filename = "tests/src/test_bfs.json"


def get_test_data():
    return [
        (test["I"], test["J"], test["starts"], [tuple(k) for k in test["expected"]])
        for test in load_json(msbfs_filename, "msbfs")
    ]


@pytest.mark.parametrize("I, J, starts, expected", get_test_data())
def test_msbfs(I, J, starts, expected):
    matrix = Matrix.from_lists(I, J)
    assert msbfs(matrix, starts) == expected
