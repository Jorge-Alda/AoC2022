import re
from copy import deepcopy
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


class Valve:
    def __init__(self, name: str, id: int, pressure: int, neighbors: list[str]) -> None:
        self.name = name
        self.id = id
        self.pressure = pressure
        self.neighbors = neighbors
        self.opened = False


class GraphPlotter:
    g = None

    def __call__(self, g: nx.Graph, fig: Figure, current: str):
        if self.g is not None:
            self.g.clear()
        self.g = deepcopy(g)
        fig.clear()
        fig.canvas.draw()
        node_colors = []
        widths = []
        for n, data in self.g.nodes(data=True):
            if n == current:
                alpha = 1.0
            else:
                alpha = 0.3
            if data["opened"] or data["pressure"] == 0:
                node_colors.append((0.0, 1.0, 0.0, alpha))
            else:
                node_colors.append((1.0, 0.0, 0.0, alpha))

        pos = nx.kamada_kawai_layout(self.g)
        nx.draw_networkx(self.g, pos=pos, node_color=node_colors)


def parse_valve(inp: str, id: int) -> Valve:
    regex = r"Valve ([A-Z][A-Z]) has flow rate=([0-9]+); tunnel[s]? lead[s]? to valve[s]? ([A-Z, ]*)"
    m = re.match(regex, inp)
    if m:
        return Valve(m.group(1), id, int(m.group(2)), m.group(3).split(', '))
    else:
        raise ValueError


def parse_graph(inp: str) -> nx.Graph:
    valves = [parse_valve(l, i) for i, l in enumerate(inp.split('\n'))]
    valves_dict = {valve.name: valve for valve in valves}
    g = nx.Graph()
    for v in valves:
        g.add_node(v.name, opened=False, pressure=v.pressure)
    for v in valves:
        for n in v.neighbors:
            g.add_edge(v.name, n)
    return g
