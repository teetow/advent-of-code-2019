import time

from lib.utils import timestamp


def has_ascending_only(s: int) -> bool:
    def is_descending(s1: str, s2: str) -> bool:
        return int(s1) > int(s2)

    has_descending = any(is_descending(s[i], s[i+1]) for i, v in enumerate(s) if i < len(s) - 1)
    return not has_descending


def recur_next(s: str, c: str):
    if len(s) >= 1 and s[0] == c:
        return c + recur_next(s[1:], c)
    return ""


def get_repeats(s: str):
    repeats = []
    i = 0
    while i < len(s) - 1:
        recur = recur_next(s[i:], s[i])
        if len(recur) > 1:
            repeats.append(recur)
        i += len(recur)
    return repeats


def has_doubles_only(s: int) -> bool:
    rps = get_repeats(s)
    return any(len(rp) == 2 for rp in rps)


def test_1(n: int) -> bool:
    return has_ascending_only(str(n)) and any(get_repeats(str(n)))


def test_2(n: int) -> bool:
    return has_ascending_only(str(n)) and has_doubles_only(str(n))


def test():
    # part 1 tests
    assert test_1(111111) is True
    assert test_1(223450) is False
    assert test_1(123789) is False
    print("Part 1 tests passed.")

    # part 2 tests
    assert test_2(112233) is True
    assert test_2(123444) is False
    assert test_2(111122) is True
    print("Part 2 tests passed.")


test()

MIN = 382345
MAX = 843167


def part1():
    start = time.time()
    valid = [x for x in range(MIN, MAX) if test_1(x)]
    timestamp(start, f"Part 1: {len(valid)}")


def part2():
    start = time.time()
    valid = [x for x in range(MIN, MAX) if test_2(x)]
    timestamp(start, f"Part 2: {len(valid)}")


part1()
part2()
