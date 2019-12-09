import time
from copy import deepcopy
from typing import Dict, List

from lib.intcoder import Intcoder, ReturnVal, RunResult
from lib.utils import readnumbers_csv, timestamp


class Ampchain:
    amps: List[Intcoder]

    def __init__(self, data, num_amps=5):
        self.amps = []
        for _ in range(num_amps):
            self.init_amp(data)

    def init_amp(self, data):
        amp = Intcoder(deepcopy(data))
        self.amps.append(amp)

    @property
    def num_amps(self):
        return len(self.amps)

    def run(self, phases: List[int], input_val: int) -> int:
        input_buffer = input_val
        for i in range(len(self.amps)):
            input_buffer = self.amps[i].run([input_buffer, phases[i]])  # FIFO
        return input_buffer


class Amploop(Ampchain):
    def run(self, phases, input_val=0) -> int:
        buffers: List[List[int]] = [[] for i in range(5)]
        buffers[4].append(input_val)

        states: List[ReturnVal] = [None] * 5
        for i in range(self.num_amps):
            buffers[i].append(phases[i])
            self.amps[i].inbuffer = buffers[i]
            self.amps[i].outbuffer = buffers[(i+1) % self.num_amps]

        done = False
        while not done:
            for i in range(self.num_amps):
                states[i] = self.amps[i].run_until_io()

            done = any(x.result == RunResult.Halted for x in states)
        outval = buffers[4].pop()
        return outval


def test1():
    # Part 1 tests
    t0code = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    t0phases = [4, 3, 2, 1, 0]
    c = Ampchain(t0code)
    t0result = c.run(t0phases, 0)
    assert t0result == 43210

    t1code = [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]
    t1phases = [0, 1, 2, 3, 4]
    c = Ampchain(t1code)
    t1result = c.run(t1phases, 0)
    assert t1result == 54321

    t2code = [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0]
    t2phases = [1, 0, 4, 3, 2]
    c = Ampchain(t2code)
    t2result = c.run(t2phases, 0)
    assert t2result == 65210

    print("Part 1 tests passed.")


def test2():
    # Part 2 tests

    t3code = [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5]
    t3phases = [9, 8, 7, 6, 5]
    t3machine = Amploop(t3code)
    t3result = t3machine.run(t3phases, 0)
    assert t3result == 139629729

    t4code = [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54, -5, 54, 1105, 1, 12, 1,
              53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4, 53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10]
    t4phases = [9, 7, 8, 5, 6]
    t4machine = Amploop(t4code)
    t4result = t4machine.run(t4phases, 0)
    assert t4result == 18216

    print("Part 2 tests passed.")


# test1()
# test2()


def unique_phases(numiterations=5*5*5*5*5+1, offset=0) -> List[int]:
    phases = [0, 0, 0, 0, 0]
    for x in range(numiterations):
        phases[0] = (x // (5*5*5*5)) % 5 + offset
        phases[1] = (x // (5*5*5)) % 5 + offset
        phases[2] = (x // (5*5)) % 5 + offset
        phases[3] = (x // 5) % 5 + offset
        phases[4] = x % 5 + offset

        if len(set(phases)) != 5:
            continue

        yield phases


def part1(data):
    start = time.time()
    results: Dict[str, int] = {}

    for phases in unique_phases():
        result = Ampchain(data).run(phases, 0)
        index = "-".join([str(n) for n in phases])
        results[index] = result

    best = max(results, key=lambda x: results[x])
    result = results[best]
    timestamp(start, f"Part 1: {best}: {result}")


def part2(data):
    start = time.time()

    results: Dict[str, str] = {}

    for phases in unique_phases(offset=5):
        result = Amploop(data).run(phases, 0)
        index = "-".join([str(n) for n in phases])
        results[index] = result

    best = max(results, key=lambda x: results[x])
    result = results[best]
    timestamp(start, f"Part 2: {best}: {result}")


testdata = readnumbers_csv("day7.csv")[0]
before = deepcopy(testdata)

part1(testdata)  # 22012
part2(testdata)  # 4039164
