import math as m
import time

from lib.utils import readnumbers, timestamp


def getFuel(mass: int) -> int:
    return m.floor(mass / 3) - 2


def getTotalFuel(fuelmass: int) -> int:
    fuel = getFuel(fuelmass)
    if fuel > 0:
        return fuel + getTotalFuel(fuel)
    return 0


data = readnumbers("day1.csv")

# step 1
start = time.time()
fuels = [getFuel(x) for x in data]
timestamp(start, f"Answer 1: {sum(fuels)}")

# step 2
start = time.time()
totalfuels = [getTotalFuel(x) for x in data]
timestamp(start, f"Answer 2: {sum(totalfuels)}")
