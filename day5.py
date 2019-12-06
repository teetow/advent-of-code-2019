import time
from copy import copy

from lib.intcoder import Intcoder
from lib.utils import readnumbers_csv, timestamp


def test():
    # Part 1 tests
    print("Part 1 has no tests.")

    # Part 2 tests
    t1 = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
    assert Intcoder(copy(t1), [0]).run() == 0
    assert Intcoder(copy(t1), [42]).run() == 1

    t2 = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]
    assert Intcoder(copy(t2), [0]).run() == 0
    assert Intcoder(copy(t2), [666]).run() == 1

    t2a = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
    assert Intcoder(copy(t2a), [7]).run() == 0
    assert Intcoder(copy(t2a), [8]).run() == 1
    assert Intcoder(copy(t2a), [9]).run() == 0

    t2b = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
    assert Intcoder(copy(t2b), [7]).run() == 1
    assert Intcoder(copy(t2b), [8]).run() == 0
    assert Intcoder(copy(t2b), [9]).run() == 0

    t2c = [3, 3, 1108, -1, 8, 3, 4, 3, 99]
    assert Intcoder(copy(t2c), [7]).run() == 0
    assert Intcoder(copy(t2c), [8]).run() == 1
    assert Intcoder(copy(t2c), [9]).run() == 0

    t2d = [3, 3, 1107, -1, 8, 3, 4, 3, 99]
    assert Intcoder(copy(t2d), [7]).run() == 1
    assert Intcoder(copy(t2d), [8]).run() == 0
    assert Intcoder(copy(t2d), [9]).run() == 0

    t3 = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
          1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
          999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]

    assert Intcoder(copy(t3), [7]).run() == 999
    assert Intcoder(copy(t3), [8]).run() == 1000
    assert Intcoder(copy(t3), [9]).run() == 1001
    print("Part 2 tests passed.")


test()


def part1(data):
    start = time.time()
    coder = Intcoder(copy(data), [1])
    result = coder.run()
    timestamp(start, f"Part 1: {result}")


def part2(data):
    start = time.time()
    coder = Intcoder(copy(data), [5])
    result = coder.run()
    timestamp(start, f"Part 2: {result}")


testdata = readnumbers_csv("day5.csv")[0]
part1(testdata)
part2(testdata)
