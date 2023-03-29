import pygraphblas as gb
from pygraphblas import Matrix, INT64

from project.utils import is_undirected


def naive_count_triangles(matrix: Matrix):
    """Calculates for each vertex of an undirected graph the number of triangles in which it participates.

    Parameters:
    ----------
    matrix: Matrix
        Bool adjacency matrix of the undirected matrix.

    Returns:
    -------
    result: list[int]
        A list of number of triangles for each vertex.
    """
    if not is_undirected(matrix):
        raise TypeError("Undirected matrix is expected.")
    squared = matrix.mxm(matrix, mask=matrix, semiring=gb.INT64.PLUS_TIMES)
    result = squared.reduce_vector()
    return [result.get(i, 0) / 2 for i in range(result.size)]


def cohen(matrix: Matrix):
    """Calculates the number of triangles of an undirected graph, using Cohen algorithm.

    Parameters:
    ----------
    matrix: Matrix
        Bool adjacency matrix of the undirected matrix.

    Returns:
    -------
    result: int
        Number of triangles.
    """
    if not is_undirected(matrix):
        raise TypeError("Undirected matrix is expected.")
    l, u = matrix.tril(), matrix.triu()
    result = l.mxm(u, mask=matrix, semiring=INT64.PLUS_TIMES)
    return result.reduce_int() / 2


def sandia(matrix: Matrix):
    """Calculates the number of triangles of an undirected graph, using Sandia algorithm.

    Parameters:
    ----------
    matrix: Matrix
        Bool adjacency matrix of the undirected matrix.

    Returns:
    -------
    result: int
        Number of triangles.
    """
    if not is_undirected(matrix):
        raise TypeError("Undirected matrix is expected.")
    l = matrix.tril()
    result = l.mxm(l, mask=l, semiring=INT64.PLUS_TIMES)
    return result.reduce_int()
