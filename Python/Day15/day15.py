import re
from itertools import product
from copy import deepcopy
from typing import Self
from enum import Enum
from pathlib import Path

basepath = Path(__file__).parent


class Extreme(Enum):
    Start = 0
    End = 1


class Interval:
    def __init__(self):
        self.endpoints = []

    @classmethod
    def new(cls, start: int, end: int) -> Self:
        res = cls()
        if end > start:
            res.endpoints = [(start, Extreme.Start), (end, Extreme.End)]
        else:
            res.endpoints = [(end, Extreme.Start), (start, Extreme.End)]
        return res

    def __len__(self) -> int:
        l = 0
        for i in range(len(self.endpoints)//2):
            l += self.endpoints[2*i+1] - self.endpoints[2*i] + 1
        return l

    def __repr__(self) -> str:
        return ", ".join(f"[{str(self.endpoints[2*i][0])}, {self.endpoints[2*i+1][0]}]" for i in range(len(self.endpoints)//2))

    def __eq__(self, rhs: Self) -> bool:
        if not isinstance(rhs, Interval):
            raise ValueError
        return self.endpoints == rhs.endpoints


    def __or__(self, rhs: Self) -> Self:
        if not isinstance(rhs, Interval):
            raise ValueError
        res = Interval()
        if len(self.endpoints) == 0:
            res.endpoints = rhs.endpoints
        else:
            combined = sorted(self.endpoints + rhs.endpoints,
                              key=lambda p: p[0] + 0.01*(p[1].value))
            s = 0
            start_val = 0
            new_endpoints = []
            for p in combined:
                if s == 0 and p[1] == Extreme.Start:
                    start_val = p[0]
                    s += 1
                elif s == 1 and p[1] == Extreme.End:
                    new_endpoints.append((start_val, Extreme.Start))
                    new_endpoints.append((p[0], Extreme.End))
                    s = 0
                elif p[1] == Extreme.Start:
                    s += 1
                else:
                    s -= 1
            res.endpoints.append(new_endpoints[0])
            for i in range(len(new_endpoints)//2-1):
                if new_endpoints[2*i+1][0] + 1 != new_endpoints[2*i+2][0]:
                    res.endpoints.append(new_endpoints[2*i+1])
                    res.endpoints.append(new_endpoints[2*i+2])
            res.endpoints.append(new_endpoints[-1])
        return res


"""     def __or__(self, rhs: Self) -> Self:
        if not isinstance(rhs, Interval):
            raise ValueError
        res = Interval()
        if len(self.starts) == 0:
            res.starts = rhs.starts
            res.ends = rhs.ends
        elif rhs.starts[0] > self.ends[-1]:
            res.starts = self.starts + rhs.starts
            res.ends = self.ends + rhs.ends
        elif rhs.ends[-1] < self.starts[0]:
            res.starts = rhs.starts + self.starts
            res.ends = rhs.ends + self.ends
        else:
            for i in range(len(self.starts)):
                if self.starts[i] < rhs.starts[0] and self.ends[i] > rhs.ends[-1]:
                    res.starts = self.starts
                    res.ends = self.ends

        #old_endpoints = deepcopy(self.endpoints)
        return res """


def parse_line(l: str) -> tuple[tuple[int, int], tuple[int, int]]:
    regex = r"Sensor at x=(-?[0-9]*), y=(-?[0-9]*): closest beacon is at x=(-?[0-9]*), y=(-?[0-9]*)"
    match = re.match(regex, l)
    if match is None:
        raise ValueError
    return (int(match.group(1)), int(match.group(2))), (int(match.group(3)), int(match.group(4)))


def dist(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])


def covered_sensor(sensor: tuple[int, int],
                   beacon: tuple[int, int],
                   target: int) -> tuple[int, int]:
    d = dist(sensor, beacon)
    d_target = dist(sensor, (sensor[0], target))
    if d_target > d:
        raise ValueError
    return (sensor[0]-(d-d_target), sensor[0]+(d-d_target))


def scan_line(sensors: list[tuple[int, int]],
              beacons: list[tuple[int, int]],
              target: int) -> set[int]:
    covered = set()
    for sensor, beacon in zip(sensors, beacons):
        try:
            range_y = covered_sensor(sensor, beacon, target)
            covered |= set(range(range_y[0], range_y[1]))
        except ValueError:
            pass
    return covered


def part1(input: str, target: int) -> int:
    sensors, beacons = [], []
    for l in input.split('\n'):
        sensor, beacon = parse_line(l)
        sensors.append(sensor)
        beacons.append(beacon)
    return len(scan_line(sensors, beacons, target))


def part2(input: str, dim: int) -> int:
    sensors, beacons, dists = [], [], []
    for l in input.split('\n'):
        sensor, beacon = parse_line(l)
        sensors.append(sensor)
        beacons.append(beacon)
        dists.append(dist(sensor, beacon))
    for x, y in product(range(dim+1), range(dim+1)):
        if not any(dist((x, y), s) <= d for s, d in zip(sensors, dists)):
            return 4_000_000*x+y
    return 0


if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp, 2000000)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))
