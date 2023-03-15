import pytest

from pygraphblas import Matrix
from project.bfs import *


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
