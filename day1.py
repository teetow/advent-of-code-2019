import math as m
import time

from lib.utils import readnumbers, timestamp


def get_fuel(mass: int) -> int:
    return m.floor(mass / 3) - 2


def get_total_fuel(fuelmass: int) -> int:
    fuel = get_fuel(fuelmass)
    if fuel > 0:
        return fuel + get_total_fuel(fuel)
    return 0


def test():
    # Part 1 tests
    assert get_fuel(12) == 2
    assert get_fuel(14) == 2
    assert get_fuel(1969) == 654
    assert get_fuel(100756) == 33583
    print("Part 1 tests passed.")

    # Part 2 tests
    assert get_total_fuel(14) == 2
    assert get_total_fuel(1969) == 966
    assert get_total_fuel(100756) == 50346
    print("Part 2 tests passed.")


test()


def part1(data):
    start = time.time()
    fuels = [get_fuel(x) for x in data]
    timestamp(start, f"Answer 1: {sum(fuels)}")


def part2(data):
    start = time.time()
    totalfuels = [get_total_fuel(x) for x in data]
    timestamp(start, f"Answer 2: {sum(totalfuels)}")


testdata = readnumbers("day1.csv")
part1(testdata)
part2(testdata)
