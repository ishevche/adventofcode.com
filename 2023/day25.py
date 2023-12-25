import itertools
import operator
import random
from functools import reduce


class Vertex:
    def __init__(self, name):
        self.name = name
        self.parent = self
        self.rank = 0

    def __eq__(self, other):
        if isinstance(other, Vertex):
            return self.name == other.name
        if isinstance(other, str):
            return self.name == other
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)


class Edge:
    def __init__(self, src, dst):
        self.src = src
        self.dest = dst


class Graph:
    def __init__(self, v, e):
        self.vertices = v
        self.edges = e


def karger_min_cut(graph):
    edges = graph.edges
    groups = len(graph.vertices)

    while groups > 2:
        edge = random.randint(0, len(graph.edges) - 1)
        src_root = get_root(edges[edge].src)
        dst_root = get_root(edges[edge].dest)
        if src_root == dst_root:
            continue
        else:
            groups -= 1
            merge(src_root, dst_root)
    min_cut = 0
    for edge in edges:
        src_root = get_root(edge.src)
        dst_root = get_root(edge.dest)
        if src_root != dst_root:
            min_cut += 1
    return min_cut


def get_root(vertex):
    if vertex.parent != vertex:
        vertex.parent = get_root(vertex.parent)
    return vertex.parent


def merge(x, y):
    x_root = get_root(x)
    y_root = get_root(y)
    if x_root.rank < y_root.rank:
        x_root.parent = y_root
    elif x_root.rank > y_root.rank:
        y_root.parent = x_root
    else:
        y_root.parent = x_root
        x_root.rank += 1


def first(graph):
    min_cut = 4
    while min_cut != 3:
        for v in graph.vertices:
            v.rank = 0
            v.parent = v
        min_cut = karger_min_cut(graph)
    result = {}
    for v in graph.vertices:
        if v.parent.name not in result:
            result[v.parent.name] = 1
        else:
            result[v.parent.name] += 1
    return reduce(operator.mul, result.values())


def second(graph):
    return "Push The Big Red Button"


def solve(filename, solve_func):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]
    vertices = set()
    for line in puzzle_input:
        u, dst = line.split(': ')
        vs = dst.split(' ')
        vertices.add(Vertex(u))
        for v in vs:
            vertices.add(Vertex(v))
    vertices = list(vertices)
    edges = []
    for line in puzzle_input:
        u, dst = line.split(': ')
        u = vertices[vertices.index(u)]
        vs = dst.split(' ')
        for v in vs:
            edges.append(Edge(u, vertices[vertices.index(v)]))
    return solve_func(Graph(vertices, edges))


if __name__ == '__main__':
    print(solve("day25.txt", first))
    print(solve("sample.txt", second))
