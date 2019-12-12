import time

from lib.intcoder import Intcoder
from lib.utils import readnumbers_csv, timestamp


def test():
    # Part 1 tests
    t0code = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    t0coder = Intcoder(t0code)
    t0coder.run()
    assert t0coder.outbuffer == t0code

    t1code = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    t1coder = Intcoder(t1code)
    t1result = t1coder.run()
    assert len(str(t1result)) == 16

    t2code = [104, 1125899906842624, 99]
    t2coder = Intcoder(t2code)
    t2result = t2coder.run()
    assert t2result == t2code[1]

    print("Part 1 tests passed.")


test()


def part1(data):
    start = time.time()
    coder = Intcoder(data)
    result = coder.run([1])
    timestamp(start, (f"Part 1: {result}"))

def part2(data):
    start = time.time()
    coder = Intcoder(data)
    result = coder.run([2])
    timestamp(start, (f"Part 2: {result}"))
    print(coder.outbuffer)

testdata = readnumbers_csv("day9.csv")[0]
part1(testdata)
part2(testdata)
