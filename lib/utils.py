import time
from typing import List


def readnumbers(fn: str) -> List[int]:
    with open(fn, "r") as infile:
        return [int(x.strip()) for x in infile.readlines()]


def readnumbers_csv(fn: str) -> List[List[int]]:
    with open(fn, "r") as infile:
        return [[int(n) for n in x.split(",")] for x in infile.readlines()]


def timestamp(start, msg=""):
    delta = (time.time() - start)*1000
    unit = "ms"
    if delta < 1/1000:
        delta = delta * 1000
        unit = "µs"
    print(f"{delta:8.2f} {unit}\t{msg}")
