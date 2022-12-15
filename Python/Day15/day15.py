import re
from pathlib import Path

basepath = Path(__file__).parent


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


def part1(input: str, target: int) -> int:
    covered = set()
    for l in input.split('\n'):
        sensor, beacon = parse_line(l)
        try:
            range_y = covered_sensor(sensor, beacon, target)
            covered |= set(range(range_y[0], range_y[1]))
        except ValueError:
            pass
    return len(covered)


if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp, 2000000)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))
