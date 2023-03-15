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
