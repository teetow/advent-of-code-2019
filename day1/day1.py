import math as m
from typing import List


def readData(fn: str) -> List:
    with open(fn, "r") as infile:
        return [int(x.split("\n")[0]) for x in infile.readlines()]


def getFuel(mass: int) -> int:
    return m.floor(mass / 3) - 2


def getTotalFuel(fuelmass: int) -> int:
    fuel = getFuel(fuelmass)
    if fuel > 0:
        return fuel + getTotalFuel(fuel)
    return 0


data = readData("day1/data.csv")

# step 1
fuels = [getFuel(x) for x in data]
print(f"Answer 1: {sum(fuels)}")

# step 2
totalfuels = [getTotalFuel(x) for x in data]
print(f"Answer 2: {sum(totalfuels)}")
