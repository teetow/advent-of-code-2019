from typing import List, NamedTuple
from enum import IntEnum
from copy import copy, deepcopy


class Opcode(IntEnum):
    Add = 1
    Mul = 2
    Input = 3
    Output = 4
    JumpIfTrue = 5
    JumpIfFalse = 6
    LessThan = 7
    Equals = 8
    Halt = 99


class ParamMode(IntEnum):
    Positional = 0
    Immediate = 1

    @staticmethod
    def parse(val: int):
        return ParamMode(val)


class Instruction:
    opcode: Opcode
    params: List[int]
    modes: List[ParamMode]

    def __init__(self, opcode: Opcode, num_params: int):
        self.opcode = opcode
        self.params = [0] * num_params
        self.modes = [ParamMode.Positional] * self.num_params

    @property
    def num_params(self):
        return len(self.params)

    @staticmethod
    def from_opcode(raw_opcode: str) -> "Instruction":
        opcode = Opcode(int(raw_opcode))
        return deepcopy(INSTRSET[opcode])


INSTRSET = {
    Opcode.Add: Instruction(Opcode.Add, 3),
    Opcode.Mul: Instruction(Opcode.Mul, 3),
    Opcode.Input: Instruction(Opcode.Input, 1),
    Opcode.Output: Instruction(Opcode.Output, 1),
    Opcode.JumpIfTrue: Instruction(Opcode.JumpIfTrue, 2),
    Opcode.JumpIfFalse: Instruction(Opcode.JumpIfFalse, 2),
    Opcode.LessThan: Instruction(Opcode.LessThan, 3),
    Opcode.Equals: Instruction(Opcode.Equals, 3),
    Opcode.Halt: Instruction(Opcode.Halt, 0),
}


class Intcoder:
    data: List[int]
    ptr: int
    inbuffer: List[int]
    outbuffer: List[int]

    def __init__(self, data, input_buffer: List[int] = None):
        self.data = deepcopy(data)
        self.ptr = 0
        self.inbuffer = input_buffer if input_buffer else []
        self.outbuffer = []

    def run(self):
        rs = None
        while rs is None:
            instr = self.next_instr()
            rs = self.call(instr)
        return rs

    def finalstate(self):
        self.run()
        return self.data

    def putaddr(self, idx: int, val=0):
        self.data[idx] = val

    def next_instr(self):
        raw_opcode = str(self.data[self.ptr])
        instr = Instruction.from_opcode(raw_opcode[-2:])

        def get_mode(param_no: int) -> ParamMode:
            offset = -3 - param_no
            modeflag = int(raw_opcode[offset]) if len(raw_opcode) >= abs(offset) else 0
            return ParamMode(modeflag)

        self.step()
        for x in range(0, instr.num_params):
            mode = get_mode(x)
            instr.modes[x] = mode
            instr.params[x] = self.data[self.ptr + x]
        self.step(len(instr.params))
        return instr

    def call(self, instr: Instruction):
        def deref(i: int):
            if instr.modes[i] == ParamMode.Positional:
                return self.data[(instr.params[i])]
            return instr.params[i]

        if instr.opcode == Opcode.Add:
            self.putaddr(instr.params[2], deref(0) + deref(1))

        elif instr.opcode == Opcode.Mul:
            self.putaddr(instr.params[2], deref(0) * deref(1))

        elif instr.opcode == Opcode.Input:
            self.putaddr(instr.params[0], self.readbuffer())

        elif instr.opcode == Opcode.Output:
            self.outbuffer.append(deref(0))

        elif instr.opcode == Opcode.JumpIfTrue:
            if not deref(0) == 0:
                self.ptr = deref(1)

        elif instr.opcode == Opcode.JumpIfFalse:
            if deref(0) == 0:
                self.ptr = deref(1)

        elif instr.opcode == Opcode.LessThan:
            self.putaddr(instr.params[2], 1 if deref(0) < deref(1) else 0)

        elif instr.opcode == Opcode.Equals:
            self.putaddr(instr.params[2], 1 if deref(0) == deref(1) else 0)

        elif instr.opcode == Opcode.Halt:
            return self.halt()

        else:
            raise Exception(f"Illegal opcode {instr.opcode}. System on fire.")

    def step(self, steps=1):
        if self.ptr + steps > len(self.data):
            raise Exception("OOB")
        self.ptr += steps

    def readbuffer(self):
        def get_input():
            print("Enter a value: ", end="")
            return input()

        data = self.inbuffer.pop() if self.inbuffer else get_input()
        return int(data)

    def halt(self):
        if self.outbuffer:
            return self.outbuffer[-1]
        return self.data[0]
