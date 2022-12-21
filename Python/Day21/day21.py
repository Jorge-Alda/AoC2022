import re
from pathlib import Path

basepath = Path(__file__).parent


def part1(inp: str) -> int:
    values: dict[str, int] = {}
    operations: dict[str, tuple[str, str, str]] = {}
    for l in inp.splitlines():
        m_val = re.match(r"([a-z]{4}): ([0-9]+)", l)
        if m_val:
            values[m_val.group(1)] = int(m_val.group(2))
        m_op = re.match(r"([a-z]{4}): ([a-z]{4}) ([+\-*/]) ([a-z]{4})", l)
        if m_op:
            operations[m_op.group(1)] = (
                m_op.group(2), m_op.group(3), m_op.group(4))
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
                        res = values[m1] // values[m2]
                    case _:
                        raise ValueError
                if monkey == "root":
                    return res
                values[monkey] = res
    return 0


if __name__ == "__main__":
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))
