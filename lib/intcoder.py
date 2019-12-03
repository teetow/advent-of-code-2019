from typing import List


class Intcoder:
    data: List[int]
    ptr: int

    def __init__(self, data):
        self.data = data
        self.ptr = 0

    @property
    def opcode(self):
        return self.data[self.ptr]

    def run(self):
        rs = None
        while not rs:
            rs = self.call(self.opcode)
        return rs

    def get(self, offset=0):
        return self.data[self.ptr + offset + 1]  # off by one?

    def call(self, opcode):
        if opcode == 1:
            self.add(self.get(), self.get(1), self.get(2))
        elif opcode == 2:
            self.mul(self.get(), self.get(1), self.get(2))
        elif opcode == 99:
            return self.halt()
        else:
            raise Exception(f"Illegal opcode {opcode}. System on fire.")

    def step(self, steps):
        if self.ptr + steps > len(self.data):
            raise Exception("OOB")
        self.ptr += steps

    def add(self, a, b, x):
        self.data[x] = self.data[a] + self.data[b]
        self.step(4)

    def mul(self, a, b, x):
        self.data[x] = self.data[a] * self.data[b]
        self.step(4)

    def halt(self):
        return self.data[0]
