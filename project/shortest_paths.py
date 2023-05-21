from math import inf
from typing import List

from pygraphblas import Matrix, FP64


def single_bellman_ford(matrix: Matrix, start: int):
    """Calculates the shortest paths in a directed graph from a given vertex.

    Parameters:
    ----------
    matrix: Matrix
        Bool adjacency matrix of the undirected matrix.
    start: int
        Starting vertex.

    Returns:
    -------
    result: list[int]
        The list where the distance to it from the specified starting vertex is indicated for each vertex.
    """
    return multiple_bellman_ford(matrix, [start])[0][1]


def multiple_bellman_ford(matrix: Matrix, starts: List[int]):
    """Calculates the shortest paths in a directed graph from a given verteces.

    Parameters:
    ----------
    matrix: Matrix
        Bool adjacency matrix of the undirected matrix.
    start: List[int])
        The list of starting vertex.

    Returns:
    -------
    result: list[int]
        The list of pairs: a vertex, and an array where for each vertex the distance to it from the specified one is specified.
    """
    for i in range(matrix.ncols):
        matrix[i, i] = 0
    dists = Matrix.sparse(FP64, nrows=len(starts), ncols=matrix.ncols)
    for i, start in enumerate(starts):
        dists[i, start] = 0
    for i in range(matrix.ncols - 1):
        dists.mxm(matrix, semiring=FP64.MIN_PLUS, out=dists)
    new = dists.mxm(matrix, semiring=FP64.MIN_PLUS)
    if dists.isne(new):
        raise ValueError("Negative cycle")
    return [
        (start, [dists.get(i, j, inf) for j in range(matrix.ncols)])
        for i, start in enumerate(starts)
    ]


def floyd_warshall(matrix: Matrix):
    """Calculates the shortest paths in a directed graph for all pairs of vertices.

    Parameters:
    ----------
    matrix: Matrix
        Bool adjacency matrix of the undirected matrix.

    Returns:
    -------
    result: list[Tuple[int, list[int]]]
        The list of pairs: a vertex, and an array where for each vertex the distance to it from the specified one is specified.
    """
    dists = matrix.dup()
    for i in range(matrix.ncols):
        dists[i, i] = 0
    for i in range(matrix.ncols):
        row = dists.extract_matrix(row_index=i)
        col = dists.extract_matrix(col_index=i)
        dists.eadd(col.mxm(row, semiring=FP64.MIN_PLUS), FP64.MIN, out=dists)
    for i in range(matrix.ncols):
        row = dists.extract_matrix(row_index=i)
        col = dists.extract_matrix(col_index=i)
        if dists.isne(
            dists.eadd(col.mxm(row, semiring=FP64.MIN_PLUS), FP64.MIN, out=dists)
        ):
            raise ValueError("Negative cycle")
    return [
        (i, [dists.get(i, j, default=inf) for j in range(matrix.nrows)])
        for i in range(matrix.ncols)
    ]
