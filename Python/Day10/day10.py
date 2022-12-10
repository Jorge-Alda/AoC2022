from pathlib import Path

basepath = Path(__file__).parent


def part1(inp: str) -> int:
    cycles = 0
    X = 1
    strengths = []
    target_cycle = 20
    for command in inp.split('\n'):
        instruction = command[:4]
        cycles += 1
        if instruction == 'addx':
            cycles += 1
        if cycles >= target_cycle:
            strengths.append(X * target_cycle)
            target_cycle += 40
        if instruction == 'addx':
            X += int(command[5:])
    return sum(strengths)


def part2(inp: str) -> str:
    screen = ""
    commands = list(reversed(inp.split('\n')))
    waiting = False
    X = 1
    command = ""
    for cycle in range(240):
        if abs((cycle % 40)-X) <= 1:
            screen += '#'
        else:
            screen += '.'
        if cycle % 40 == 39:
            screen += '\n'
        if waiting:
            waiting = False
            X += int(command[5:])
        else:
            command = commands.pop()
            if command[:4] == 'addx':
                waiting = True
    return screen


if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

    out2 = part2(inp)
    with open(basepath/"output2", "wt") as f:
        f.write(str(out2))
