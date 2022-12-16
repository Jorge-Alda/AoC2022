import re
from copy import deepcopy
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from time import sleep
from pathlib import Path

basepath = Path(__file__).parent

class Valve:
    def __init__(self, name: str, id: int, pressure: int, neighbors: list[str]) -> None:
        self.name = name
        self.id = id
        self.pressure = pressure
        self.neighbors = neighbors
        self.opened = (pressure == 0)


class GraphPlotter:
    g = None

    def __call__(self, g: nx.Graph, fig: Figure, current: str):
        if self.g is not None:
            self.g.clear()
        self.g = deepcopy(g)
        fig.clear()
        fig.canvas.draw()
        node_colors = []
        max_p = max(data["pressure"] for _, data in self.g.nodes(data=True))
        for n, data in self.g.nodes(data=True):
            if n == current:
                alpha = 1.0
            else:
                alpha = 0.3
            if data["opened"]:
                node_colors.append((0.0, 1.0, 0.0, alpha))
            else:
                node_colors.append((1.0, 0.0, data["pressure"]/max_p, alpha))

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
    g = nx.Graph()
    for v in valves:
        g.add_node(v.name, opened=v.opened, pressure=v.pressure)
    for v in valves:
        for n in v.neighbors:
            g.add_edge(v.name, n)
    return g


def next_target(g: nx.Graph, pos: str, rem_t: int) -> list[str]:
    scores = {}
    for n, ndata in g.nodes(data=True):
        if n != pos and not ndata["opened"]:
            path = "".join(nx.shortest_path(g, pos, n)[1:])
            scores |= {path: ndata["pressure"]*(rem_t-len(path)//2-1)}
    if len(scores.keys()) > 0:
        path_max = max(scores.items(), key=lambda x: x[1])
        l = len(path_max[0])
        return [path_max[0][l-2*i-2:l-2*i] for i in range(l//2)]
    else:
        return []


def part1(inp: str):
    g = parse_graph(inp)
    pressure = 0
    flow = 0
    pos = "AA"
    path = []
    fig = plt.figure()
    plt.ion()
    plt.show()
    plotter = GraphPlotter()
    for t in range(30):
        if not g.nodes[pos]["opened"]:
            flow += g.nodes[pos]["pressure"]
            g.nodes[pos]["opened"] = True
        elif len(path) > 0:
            pos = path.pop()
        else:
            path = next_target(g, pos, 30-t)
            if len(path) > 0:
                pos = path.pop()
        pressure += flow
        print(f"{t}\t{flow}")
        plotter(g, fig, pos)
        sleep(2)

if __name__ == '__main__':
    with open(basepath/"test", "rt") as f:
        inp = f.read().strip()

    part1(inp)