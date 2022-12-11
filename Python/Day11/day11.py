from typing import Callable, Self
from collections import deque
from pathlib import Path
from functools import reduce

basepath = Path(__file__).parent


class Monkey:
    def __init__(self,
                 items: list[int],
                 operation: Callable[[int], int],
                 test: int,
                 throw_true: int,
                 throw_false: int):
        self.items = deque(items)
        self.operation = operation
        self.test = test
        self.throw_true = throw_true
        self.throw_false = throw_false
        self.inspected = 0

    @classmethod
    def from_descr(cls, descr: str) -> Self:
        lines = descr.split('\n')
        items = [int(i) for i in lines[1].removeprefix(
            "  Starting items: ").split(', ')]
        op = lines[2].removeprefix("  Operation: new = old ")
        if op[0] == '+':
            @staticmethod
            def operation(x: int) -> int: return (x + int(op[2:]))
        elif op == "* old":
            @staticmethod
            def operation(x: int) -> int: return x * x
        else:
            @staticmethod
            def operation(x: int) -> int: return x * int(op[2:])
        test = int(lines[3].removeprefix("  Test: divisible by "))
        throw_true = int(lines[4].removeprefix(
            "    If true: throw to monkey "))
        throw_false = int(lines[5].removeprefix(
            "    If false: throw to monkey "))
        return cls(items, operation, test, throw_true, throw_false)

    def append(self, item: int):
        self.items.append(item)

    def process_item(self, d: int = 3, masterdiv: int | None = None) -> tuple[int, int]:
        item = self.items.popleft()
        worry = (self.operation(item) // d)
        if masterdiv is not None:
            worry %= masterdiv
        self.inspected += 1
        if worry % self.test == 0:
            return (self.throw_true, worry)
        else:
            return (self.throw_false, worry)


def part1(inp: str) -> int:
    monkeys = [Monkey.from_descr(l) for l in inp.split('\n\n')]
    for _ in range(20):
        for m in monkeys:
            while len(m.items) > 0:
                t, w = m.process_item()
                monkeys[t].append(w)
    max1 = 0
    max2 = 0
    for m in monkeys:
        if m.inspected > max1:
            max2 = max1
            max1 = m.inspected
        elif m.inspected > max2:
            max2 = m.inspected
    return max1 * max2


def part2(inp: str) -> int:
    monkeys = [Monkey.from_descr(l) for l in inp.split('\n\n')]
    masterdiv = reduce(lambda x, y: x*y, [m.test for m in monkeys])
    for _ in range(10000):
        for m in monkeys:
            while len(m.items) > 0:
                t, w = m.process_item(1, masterdiv)
                monkeys[t].append(w)
    max1 = 0
    max2 = 0
    for m in monkeys:
        if m.inspected > max1:
            max2 = max1
            max1 = m.inspected
        elif m.inspected > max2:
            max2 = m.inspected
    return max1 * max2


if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

    out2 = part2(inp)
    with open(basepath/"output2", "wt") as f:
        f.write(str(out2))
