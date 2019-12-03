import time
from copy import copy

from lib.intcoder import Intcoder
from lib.utils import readnumbers_csv, timestamp


def part1(rom):
    ram = copy(rom)
    ram[1] = 12
    ram[2] = 2
    m = Intcoder(ram)
    return m.run()


def part2(rom):
    for noun in range(0, 99):
        for verb in range(0, 99):
            ram = copy(rom)
            ram[1] = noun
            ram[2] = verb
            vm = Intcoder(ram)
            result = vm.run()
            if result == 19690720:
                return noun*100+verb


image = readnumbers_csv("day2.csv")[0]

start = time.time()
timestamp(start, f"Part 1: {part1(image)}")

start = time.time()
timestamp(start, f"Part 2: {part2(image)}")
