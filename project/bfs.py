from typing import List

import pygraphblas as gb
from pygraphblas import Vector, Matrix, BOOL, INT64


def bfs(matrix: Matrix, start: int):
    """Breadth-first search algorithm for a given directed graph and starting vertex.

    Parameters:
    ----------
    matrix: Matrix
        Bool adjacency matrix of the graph.
    start: int
        Starting vertex.

    Returns:
    -------
    result: list[int]
        A list that specifies the number of steps required to reach the i vertex,
        where i is the index in the list. If the vertex is unreachable, there is -1.
    """
    front = Vector.sparse(BOOL, size=matrix.nrows)
    front[start] = True
    result = Vector.sparse(INT64, size=matrix.nrows)
    step = 0
    while front.nvals:
        result.assign_scalar(step, mask=front)
        front.vxm(matrix, out=front, mask=result.S, desc=gb.descriptor.RC)
        step += 1
    return [result.get(i, -1) for i in range(result.size)]


def msbfs(matrix: Matrix, starts: List[int]):
    """Multi-source breadth-first search algorithm for a given directed graph and starting vertexes.

    Parameters:
    ----------
    matrix: Matrix
        Bool adjacency matrix of the graph.
    starts: List[int]
        Starting vertexes.

    Returns:
    -------
    result: list[tuple[int, list[int]]]
        A list of pairs: the starting vertex, and a list (parents), where for each vertex of the graph it is
        indicated from which vertex we came to this one by the shortest path from the starting vertex.
        For the starting vertex it is -1, for the unreachable it is -2
    """

    front = Matrix.sparse(INT64, nrows=len(starts), ncols=matrix.ncols)
    parents = Matrix.sparse(INT64, nrows=len(starts), ncols=matrix.ncols)
    for i, start in enumerate(starts):
        front[i, start] = start
        parents[i, start] = -1
    while front.nvals:
        front.mxm(
            matrix,
            out=front,
            mask=parents.S,
            desc=gb.descriptor.RC,
            semiring=INT64.MIN_FIRST,
        )
        parents.assign(front, mask=front.S)
        front.apply(INT64.POSITIONJ, out=front, mask=front.S)
    return [
        (start, [parents.get(i, j, -2) for j in range(matrix.ncols)])
        for i, start in enumerate(starts)
    ]
