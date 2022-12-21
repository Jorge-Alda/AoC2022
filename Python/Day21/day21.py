import re
from pathlib import Path
from typing import Callable, Self
from copy import deepcopy

basepath = Path(__file__).parent


class Unknown:
    def __init__(self, m=1.0, b=0.0) -> None:
        # mx + b
        self.m = m
        self.b = b

    def __add__(self, y: float | int) -> Self:
        return Unknown(self.m, self.b + y)

    def __radd__(self, y: float | int) -> Self:
        return self + y

    def __sub__(self, y: float | int) -> Self:
        return Unknown(self.m, self.b - y)

    def __rsub__(self, y: float | int) -> Self:
        return -1.0 * self + y

    def __mul__(self, y: float | int) -> Self:
        return Unknown(y * self.m, y*self.b)

    def __rmul__(self, y: float | int) -> Self:
        return self * y

    def __truediv__(self, y: float | int) -> Self:
        return Unknown(self.m/y, self.b/y)

    def __repr__(self) -> str:
        return f"{self.m}x + {self.b}"

    def solve(self) -> int:
        return round(-self.b/self.m)


def parse(inp: str) -> tuple[dict[str, int | float], dict[str, tuple[str, str, str]]]:
    values: dict[str, int | float] = {}
    operations: dict[str, tuple[str, str, str]] = {}
    for l in inp.splitlines():
        m_val = re.match(r"([a-z]{4}): ([0-9]+)", l)
        if m_val:
            values[m_val.group(1)] = int(m_val.group(2))
        m_op = re.match(r"([a-z]{4}): ([a-z]{4}) ([+\-*/]) ([a-z]{4})", l)
        if m_op:
            operations[m_op.group(1)] = (
                m_op.group(2), m_op.group(3), m_op.group(4))
    return values, operations


def calculate(v: dict[str, int | float | Unknown], operations: dict[str, tuple[str, str, str]]) -> int | Unknown:
    values = deepcopy(v)
    while 1:
        for monkey, (m1, op, m2) in operations.items():
            if (monkey not in values) and (m1 in values) and (m2 in values):
                match op:
                    case "+":
                        res = values[m1] + values[m2]
                    case "-":
                        res = values[m1] - values[m2]
                    case "*":
                        res = values[m1] * values[m2]
                    case "/":
                        res = values[m1] / values[m2]
                    case _:
                        raise ValueError
                if monkey == "root":
                    return res
                values[monkey] = res
    return 0


def part1(inp: str) -> int:
    return calculate(*parse(inp))


def part2(inp: str) -> int:
    values, operations = parse(inp)
    operations["root"] = (operations["root"][0], "-", operations["root"][2])
    values["humn"] = Unknown()
    res = calculate(values, operations)
    print(res)
    if isinstance(res, Unknown):
        return res.solve()
    else:
        return round(res)

if __name__ == "__main__":
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

    out2 = part2(inp)
    with open(basepath/"output2", "wt") as f:
        f.write(str(out2))
