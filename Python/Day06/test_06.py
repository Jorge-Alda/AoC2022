from day06 import part1, part2


def test_part1():
    assert (part1("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 7)
    assert (part1("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5)
    assert (part1("nppdvjthqldpwncqszvftbrmjlhg") == 6)
    assert (part1("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10)
    assert (part1("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11)


def test_part2():
    assert (part2("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 19)
    assert (part2("bvwbjplbgvbhsrlpgdmjqwftvncz") == 23)
    assert (part2("nppdvjthqldpwncqszvftbrmjlhg") == 23)
    assert (part2("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 29)
    assert (part2("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 26)
