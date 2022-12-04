from pathlib import Path
from typing import TypeVar, Iterable
from itertools import islice

basepath = Path(__file__).parent

T = TypeVar('T')


def priority(c: str) -> int:
    p = ord(c)
    if p > 96:
        return p-96
    else:
        return p-38


def triplet(it: Iterable[T]) -> Iterable[tuple[T, T, T]]:
    itt = iter(it)
    while (batch := tuple(islice(itt, 3))):
        yield batch


def part1(inp: str) -> int:
    tot = 0
    for rucksack in inp.split('\n'):
        l = int(len(rucksack)/2)
        comp1 = rucksack[:l]
        comp2 = rucksack[l:]
        for it in comp1:
            if it in comp2:
                tot += priority(it)
                break
    return tot


def part2(inp: str) -> int:
    tot = 0
    rucksacks = inp.split('\n')
    for r1, r2, r3 in triplet(rucksacks):
        for it in r1:
            if (it in r2) and (it in r3):
                tot += priority(it)
                break
    return tot


if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

    out2 = part2(inp)
    with open(basepath/"output2", "wt") as f:
        f.write(str(out2))
