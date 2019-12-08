import time
from copy import deepcopy
from typing import List, Dict

from lib.intcoder import Intcoder
from lib.utils import dumpdata, readnumbers_csv, timestamp


class Amplifier:
    coder: Intcoder

    def __init__(self, code):
        self.coder = Intcoder(code)

    def run(self, phase: int, inputdata: int) -> int:
        coderparams = [inputdata, phase]  # FIFO
        return self.coder.run(coderparams)


class Ampchain:
    amps: List[Amplifier]

    def __init__(self, data, num_amps=5):
        self.amps = []
        for i in range(num_amps):
            self.init_amp(data)

    def init_amp(self, data):
        amp = Amplifier(deepcopy(data))
        self.amps.append(amp)

    def run(self, phases: List[int], input_val: int) -> int:
        input_buffer = input_val
        for i in range(len(self.amps)):
            input_buffer = self.amps[i].run(phases[i], input_buffer)
        return input_buffer


def test():
    t0code = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    t0phases = [4, 3, 2, 1, 0]
    t0input = 0
    c = Ampchain(t0code)
    t0result = c.run(t0phases, t0input)
    assert t0result == 43210

    t1code = [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]
    t1phases = [0, 1, 2, 3, 4]
    t1input = 0
    c = Ampchain(t1code)
    t1result = c.run(t1phases, t1input)
    assert t1result == 54321

    t2code = [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0]
    t2phases = [1, 0, 4, 3, 2]
    t2input = 0
    c = Ampchain(t2code)
    t2result = c.run(t2phases, t2input)
    assert t2result == 65210

    print("Part 1 tests passed.")


test()


def part1(data):
    start = time.time()
    phases = [0, 0, 0, 0, 0]
    results: Dict[str, int] = {}
    numiterations = (5*5*5*5*5)+1

    for x in range(numiterations):
        phases[0] = (x // (5*5*5*5)) % 5
        phases[1] = (x // (5*5*5)) % 5
        phases[2] = (x // (5*5)) % 5
        phases[3] = (x // 5) % 5
        phases[4] = x % 5

        if len(set(phases)) != 5:
            continue

        result = Ampchain(data).run(phases, 0)
        index = "-".join([str(n) for n in phases])
        results[index] = result

    best = max(results, key=lambda x: results[x])
    result = results[best]
    timestamp(start, f"Part 1: {best}: {result}")
    dumpdata(results, "day7.out")


def part2(data):
    pass


testdata = readnumbers_csv("day7.csv")[0]

part1(testdata)
part2(testdata)
