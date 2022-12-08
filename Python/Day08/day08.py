from pathlib import Path

basepath = Path(__file__).parent


def part1(inp: str) -> int:
    rows = inp.split('\n')
    n_rows = len(rows)
    n_cols = len(rows[0])
    v_left = [[True]*n_cols for _ in range(n_rows)]
    v_right = [[True]*n_cols for _ in range(n_rows)]
    v_top = [[True]*n_cols for _ in range(n_rows)]
    v_bottom = [[True]*n_cols for _ in range(n_rows)]

    for i in range(n_rows):
        for j in range(1, n_cols):
            v_left[i][j] = all(rows[i][j] > rows[i][k] for k in range(j))
            v_right[i][n_cols-j-1] = all(rows[i][n_cols-j-1]
                                         > rows[i][n_cols-k-1] for k in range(j))

    for j in range(n_cols):
        for i in range(1, n_rows):
            v_top[i][j] = all(rows[i][j] > rows[k][j] for k in range(i))
            v_bottom[n_rows-i-1][j] = all(rows[n_rows-i-1]
                                          [j] > rows[n_rows-k-1][j] for k in range(i))

    visible = [v_left[i][j] | v_right[i][j] | v_top[i][j] | v_bottom[i][j]
               for i in range(n_rows) for j in range(n_cols)]
    return sum(int(v) for v in visible)


def part2(inp: str) -> int:
    rows = inp.split('\n')
    n_rows = len(rows)
    n_cols = len(rows[0])
    v_left = [[0,]*n_cols for _ in range(n_rows)]
    v_right = [[0,]*n_cols for _ in range(n_rows)]
    v_top = [[0,]*n_cols for _ in range(n_rows)]
    v_bottom = [[0,]*n_cols for _ in range(n_rows)]

    for i in range(n_rows):
        for j in range(1, n_cols):
            v = 1
            for k in range(1, j):
                if rows[i][j] > rows[i][j-k]:
                    v += 1
                else:
                    break
            v_left[i][j] = v

    for i in range(n_rows):
        for j in range(1, n_cols):
            v = 1
            for k in range(1, j):
                if rows[i][n_cols-j-1] > rows[i][n_cols-j+k-1]:
                    v += 1
                else:
                    break
            v_right[i][n_cols-j-1] = v

    for j in range(n_cols):
        for i in range(1, n_rows):
            v = 1
            for k in range(1, i):
                if rows[i][j] > rows[i-k][j]:
                    v += 1
                else:
                    break
            v_top[i][j] = v

    for j in range(n_cols):
        for i in range(1, n_rows):
            v = 1
            for k in range(1, i):
                if rows[n_rows-i-1][j] > rows[n_rows-i+k-1][j]:
                    v += 1
                else:
                    break
            v_bottom[n_rows-i-1][j] = v

    return max(v_left[i][j] * v_right[i][j] * v_top[i][j] * v_bottom[i][j] for i in range(n_rows) for j in range(n_cols))


if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

    out2 = part2(inp)
    with open(basepath/"output2", "wt") as f:
        f.write(str(out2))
