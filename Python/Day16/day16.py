import re
from copy import deepcopy
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from time import sleep
from pathlib import Path
import itertools

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
        fig.canvas.flush_events()


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


def part1(inp: str) -> int:
    g = parse_graph(inp)
    pressurized = ["AA"]
    distances = {}
    for node in g.nodes():
        if g.nodes[node]["pressure"] > 0:
            pressurized.append(node)
    for i in range(len(pressurized)):
        for j in range(1+i, len(pressurized)):
            d = nx.shortest_path_length(g, pressurized[i], pressurized[j])
            distances |= {(pressurized[i], pressurized[j]): d,
                          (pressurized[j], pressurized[i]): d}
    return follow_path(g, distances, "AA", 30, set(pressurized[1:]), 0)


def follow_path(g: nx.Graph,
                distances: dict[tuple[str, str], int],
                pos: str,
                t: int,
                valves: set[str],
                max_pres: int) -> int:
    if len(valves) == 0:
        return max_pres
    pres: list[int] = []
    for v in valves:
        dist = distances[(pos, v)]
        if t > dist:
            new_pres = max_pres + (t - dist - 1) * g.nodes[v]["pressure"]
            p = follow_path(g, distances, v, t-dist-1,
                            valves - {v}, new_pres)
            pres.append(p)
        else:
            pres.append(max_pres)
    return max(pres)


def follow_2_paths(g: nx.Graph,
                   distances: dict[tuple[str, str], int],
                   pos_h: str,
                   t_h: int,
                   pos_e: str,
                   t_e: int,
                   valves: set[str],
                   max_pres: int) -> int:
    if len(valves) == 0:
        return max_pres
    if len(valves) == 1:
        pres_e = follow_path(g, distances, pos_e, t_e, valves, max_pres)
        pres_h = follow_path(g, distances, pos_h, t_h, valves, max_pres)
        return max(pres_e, pres_h)
    pres: list[int] = []
    for v_h, v_e in itertools.permutations(valves, 2):
        dist_h = distances[(pos_h, v_h)]
        dist_e = distances[(pos_e, v_e)]
        times = (t_h > dist_h, t_e > dist_e)
        match times:
            case (True, True):
                pres_h = (t_h - dist_h - 1) * g.nodes[v_h]["pressure"]
                pres_e = (t_e - dist_e - 1) * g.nodes[v_e]["pressure"]
                new_pres = max_pres + pres_h + pres_e
                p = follow_2_paths(g, distances, v_h, t_h - dist_h - 1,
                                   v_e, t_e - dist_e - 1, valves - {v_h, v_e}, new_pres)
                pres.append(p)
            case (True, False):
                pres_h = (t_h - dist_h - 1) * g.nodes[v_h]["pressure"]
                new_pres = max_pres + pres_h
                p = follow_path(g, distances, v_h, t_h -
                                dist_h - 1, valves - {v_h}, new_pres)
                pres.append(p)
            case (False, True):
                pres_e = (t_e - dist_e - 1) * g.nodes[v_e]["pressure"]
                new_pres = max_pres + pres_e
                p = follow_path(g, distances, v_e, t_e -
                                dist_e - 1, valves - {v_e}, new_pres)
                pres.append(p)
            case (False, False):
                pres.append(max_pres)
    return max(pres)


def part2(inp: str) -> int:
    g = parse_graph(inp)
    pressurized = ["AA"]
    distances = {}
    for node in g.nodes():
        if g.nodes[node]["pressure"] > 0:
            pressurized.append(node)
    for i in range(len(pressurized)):
        for j in range(1+i, len(pressurized)):
            d = nx.shortest_path_length(g, pressurized[i], pressurized[j])
            distances |= {(pressurized[i], pressurized[j]): d,
                          (pressurized[j], pressurized[i]): d}
    return follow_2_paths(g, distances, "AA", 26, "AA", 26, set(pressurized[1:]), 0)


if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

    out2 = part2(inp)
    with open(basepath/"output2", "wt") as f:
        f.write(str(out2))
