import math as m
import time
from typing import List, Union

from lib.utils import read_digits, timestamp


def stretch(l: List[int], factor: float) -> List[int]:
    outlist = []
    list_size = len(l)
    for i in range(list_size * factor):
        index = m.floor(i / factor) % list_size
        outlist.append(l[index])
    return outlist[1:] + [outlist[0]]


def number_sum(l: List[int]) -> int:
    total = sum(l)
    return int(str(total)[-1:])


class FFT:
    pattern: List[int]
    phasedata: List[int]
    window_size: int

    def __init__(self, phasedata: Union[List, str]):
        self.pattern = [0, 1, 0, -1]
        self.phasedata = []
        if isinstance(phasedata, list):
            self.phasedata = phasedata
        else:
            self.phasedata = [int(x) for x in list(phasedata)]
        self.window_size = len(self.phasedata)

    def calc_digit(self, digit: int, iteration: int) -> int:
        pattern_index = ((digit + 1) // iteration) % 4
        return self.phasedata[digit] * self.pattern[pattern_index]

    def calc_phase(self, iteration: int) -> List[int]:
        row = [self.calc_digit(i, iteration + 1) for i in range(self.window_size)]
        return number_sum(row)

    def calc_phases(self, num_iterations: int) -> List[int]:
        for _ in range(num_iterations):
            self.phasedata = [self.calc_phase(i) for i in range(self.window_size)]
        return "".join([str(x) for x in self.phasedata])


def test1():
    fft = FFT("12345678")
    a = fft.calc_phases(4)
    assert a == "01029498"

    fft = FFT("80871224585914546619083218645595")
    a = fft.calc_phases(100)
    assert a[:8] == "24176176"

    fft = FFT("19617804207202209144916044189917")
    a = fft.calc_phases(100)
    assert a[:8] == "73745418"

    fft = FFT("69317163492948606335995924319873")
    a = fft.calc_phases(100)
    assert a[:8] == "52432133"

    print(f"Part 1 tests passed.")


def part1(data):
    start = time.time()
    fft = FFT(data)
    result = fft.calc_phases(100)[:8]
    timestamp(start, f"Part 1: {result}")


if __name__ == "__main__":
    # test1()

    testdata = read_digits("day16.dat")[0]
    part1(testdata)
