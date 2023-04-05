from pygraphblas import Matrix


def is_undirected(graph: Matrix):
    return graph.iseq(graph.transpose())
