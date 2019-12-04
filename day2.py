import time
from copy import copy

from lib.intcoder import Intcoder
from lib.utils import readnumbers_csv, timestamp


def test():
    # Part 1 tests
    assert Intcoder([1, 0, 0, 0, 99]).finalstate() == [2, 0, 0, 0, 99]
    assert Intcoder([2, 3, 0, 3, 99]).finalstate() == [2, 3, 0, 6, 99]
    assert Intcoder([2, 4, 4, 5, 99, 0]).finalstate() == [2, 4, 4, 5, 99, 9801]
    assert Intcoder([1, 1, 1, 4, 99, 5, 6, 0, 99]).finalstate() == [30, 1, 1, 4, 2, 5, 6, 0, 99]
    print("Part 1 tests passed.")

    # Part 2 tests
    print("Part 2 has no tests.")


test()


def part1(image):
    start = time.time()
    ram = copy(image)
    ram[1] = 12
    ram[2] = 2
    m = Intcoder(ram).run()
    timestamp(start, f"Part 1: {m}")


def run_until(rom, expected_result: int):
    for noun in range(0, 99):
        for verb in range(0, 99):
            ram = copy(rom)
            ram[1] = noun
            ram[2] = verb
            vm = Intcoder(ram)
            result = vm.run()
            if result == expected_result:
                return noun * 100 + verb


def part2(image):
    start = time.time()
    timestamp(start, f"Part 2: {run_until(image, 19690720)}")


testdata = readnumbers_csv("day2.csv")[0]

part1(testdata)
part2(testdata)
