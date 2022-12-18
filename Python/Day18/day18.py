from pathlib import Path

basepath = Path(__file__).parent


def dist(p1: tuple[int, int, int], p2: tuple[int, int, int]) -> int:
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]) + abs(p1[2]-p2[2])


def part1(inp: str) -> int:
    cubes = []
    surface = 0
    for c in inp.splitlines():
        cube = tuple(int(x) for x in c.split(','))
        surface += 6 - sum(2 for t in cubes if dist(cube, t) == 1)
        cubes.append(cube)
    return surface


def part2(inp: str) -> int:
    cubes: list[tuple[int, int, int]] = []
    surface = 0
    for c in inp.splitlines():
        cube = tuple(int(x) for x in c.split(','))
        cubes.append(cube)
    max_x = max(c[0] for c in cubes)
    max_y = max(c[1] for c in cubes)
    max_z = max(c[2] for c in cubes)
    min_x = min(c[0] for c in cubes)
    min_y = min(c[1] for c in cubes)
    min_z = min(c[2] for c in cubes)
    range_x = range(min_x-1, max_x+2)
    range_y = range(min_y-1, max_y+2)
    range_z = range(min_z-1, max_z+2)
    visited = [(min_x-1, min_y-1, min_z-1),]
    candidates = [(min_x-1, min_y-1, min_z-1),]
    while len(candidates) > 0:
        new_points: list[tuple[int, int, int]] = []
        for p in candidates:
            neighbors = [
                (p[0]-1, p[1], p[2]),
                (p[0]+1, p[1], p[2]),
                (p[0], p[1]-1, p[2]),
                (p[0], p[1]+1, p[2]),
                (p[0], p[1], p[2]-1),
                (p[0], p[1], p[2]+1)
            ]
            for n in neighbors:
                if not n in visited and n[0] in range_x and n[1] in range_y and n[2] in range_z:
                    if n in cubes:
                        surface += 1
                    else:
                        visited.append(n)
                        new_points.append(n)
        candidates = new_points
    return surface


if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

    out2 = part2(inp)
    with open(basepath/"output2", "wt") as f:
        f.write(str(out2))
