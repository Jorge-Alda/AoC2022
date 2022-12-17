from abc import ABC, abstractmethod
from typing import Generator, Self
from pathlib import Path

basepath = Path(__file__).parent


class BaseShape(ABC):
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @abstractmethod
    def coordinates(self) -> list[tuple[int, int]]:
        pass

    def move(self, direction: str) -> Self:
        if direction == '>':
            return self.__class__(self.x+1, self.y)
        elif direction == '<':
            return self.__class__(self.x-1, self.y)
        raise ValueError

    def fall(self) -> Self:
        return self.__class__(self.x, self.y-1)

    def collision(self, rocks: set[tuple[int, int]]) -> bool:
        coords = self.coordinates()
        return any(c[0] < 0 for c in coords) or any(c[0] > 6 for c in coords) or any(c in rocks for c in coords)


class Horizontal(BaseShape):
    def coordinates(self) -> list[tuple[int, int]]:
        return [(self.x, self.y), (self.x+1, self.y), (self.x+2, self.y), (self.x+3, self.y)]


class Plus(BaseShape):
    def coordinates(self) -> list[tuple[int, int]]:
        return [(self.x, self.y+1), (self.x+1, self.y), (self.x+1, self.y+1), (self.x+1, self.y+2), (self.x+2, self.y+1)]


class Angle(BaseShape):
    def coordinates(self) -> list[tuple[int, int]]:
        return [(self.x, self.y), (self.x+1, self.y), (self.x+2, self.y), (self.x+2, self.y+1), (self.x+2, self.y+2)]


class Vertical(BaseShape):
    def coordinates(self) -> list[tuple[int, int]]:
        return [(self.x, self.y), (self.x, self.y+1), (self.x, self.y+2), (self.x, self.y+3)]


class Block(BaseShape):
    def coordinates(self) -> list[tuple[int, int]]:
        return [(self.x, self.y), (self.x+1, self.y), (self.x, self.y+1), (self.x+1, self.y+1)]


def directions(text: str) -> Generator[str, None, None]:
    l = len(text)
    n = 0
    while 1:
        yield text[n]
        n = (n+1) % l


def newrock() -> Generator[BaseShape, int | None, None]:
    n = 0
    shapes = [Horizontal, Plus, Angle, Vertical, Block]
    y = 4
    while 1:
        res = shapes[n](2, y)
        k = (yield res)
        if k is not None:
            y = k + 4
        n = (n+1) % 5


def delete_rows(rocks: set[tuple[int, int]]) -> set[tuple[int, int]]:
    base = min(r[1] for r in rocks)
    height = max(r[1] for r in rocks)
    holes = [{x for x in range(7) if (x, y) not in rocks}
             for y in range(base, height+1)]
    limit = base
    for i in range(max(0, len(holes)-4)):
        if len(holes[i] & holes[i+1] & holes[i+2] & holes[i+3]) == 0:
            limit += 1
    res = {r for r in rocks if r[1] >= limit-1}
    return res


def part1(dirs: str, n: int) -> int:
    rocks: set[tuple[int, int]] = set((x, 0) for x in range(7))
    height = 0
    generate_rocks = newrock()
    rock = generate_rocks.send(None)
    generate_dirs = directions(dirs)
    i = 0
    while i < n:
        d = next(generate_dirs)
        r_moved = rock.move(d)
        if not r_moved.collision(rocks):
            rock = r_moved
        r_fall = rock.fall()
        if r_fall.collision(rocks):
            i += 1
            rocks |= set(rock.coordinates())
            height = max(c[1] for c in rocks)
            rock = generate_rocks.send(height)
            rocks = delete_rows(rocks)
            if i % 1_000_000 == 0:
                print(i)
        else:
            rock = r_fall
    return height


if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp, 2022)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

    out2 = part1(inp, 1_000_000_000_000)
    with open(basepath/"output2", "wt") as f:
        f.write(str(out2))
