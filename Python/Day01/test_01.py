from day01 import part1


def test_part1():
    input = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""
    output = part1(input)
    assert output == 24000
