from copy import deepcopy
from enum import IntEnum
from typing import Dict, List, NamedTuple


class Opcode(IntEnum):
    Add = 1
    Mul = 2
    Input = 3
    Output = 4
    JumpIfTrue = 5
    JumpIfFalse = 6
    LessThan = 7
    Equals = 8
    ChangePtrOffset = 9
    Halt = 99


class ParamMode(IntEnum):
    Positional = 0
    Immediate = 1
    Relative = 2


class Instruction:
    opcode: Opcode
    params: List[int]
    modes: List[ParamMode]

    def __init__(self, opcode: Opcode):
        self.opcode = opcode
        num_params = PARAM_COUNTS[opcode]
        self.params = [0] * num_params
        self.modes = [ParamMode.Positional] * num_params

    def __repr__(self):
        mergedparams = [f"{x}({self.modes[i].name})" for i, x in enumerate(self.params)]
        return f"{self.opcode.name}[{', '.join(mergedparams)}]"

    @property
    def num_params(self):
        return PARAM_COUNTS[self.opcode]

    @property
    def size(self):
        return self.num_params + 1


PARAM_COUNTS = {
    Opcode.Add: 3,
    Opcode.Mul: 3,
    Opcode.Input: 1,
    Opcode.Output: 1,
    Opcode.JumpIfTrue: 2,
    Opcode.JumpIfFalse: 2,
    Opcode.LessThan: 3,
    Opcode.Equals: 3,
    Opcode.ChangePtrOffset: 1,
    Opcode.Halt: 0,
}


class RunResult(IntEnum):
    Halted = 0,
    NeedInput = 1,
    HasOutput = 2,


class ReturnVal(NamedTuple):
    result: RunResult
    output: int


class Mem(list):
    values: Dict[int, int]

    def __init__(self, data):
        super().__init__()
        self.values = {}
        self.init(data)

    def init(self, data: List):
        for i in range(len(data)):
            self.values[i] = data[i]

    def __setitem__(self, key, value):
        self.values[key] = value

    def __getitem__(self, index):
        if index in self.values:
            return self.values[index]
        return 0


class Intcoder:
    data: Mem
    ptr: int
    ptroffset: int
    inbuffer: List[int]
    outbuffer: List[int]

    def __init__(self, data, input_buffer: List[int] = None):
        self.data = Mem(data)
        self.ptr = 0
        self.ptroffset = 0
        self.inbuffer = deepcopy(input_buffer) if input_buffer else []
        self.outbuffer = []

    def run(self, input_buffer: List[int] = None):
        if input_buffer:
            self.inbuffer = deepcopy(input_buffer)
        rs = None
        while rs is None:
            instr = self.next_instr()
            rs = self.call(instr)
        return rs

    def run_until_input(self) -> ReturnVal:
        while True:
            instr = self.next_instr()
            rs = self.call(instr)

            if rs or instr.opcode == Opcode.Halt:
                return ReturnVal(RunResult.Halted, rs)

            if self.peek_instr().opcode == Opcode.Input and not self.inbuffer:
                return ReturnVal(RunResult.NeedInput, 0)

    def run_until_io(self) -> ReturnVal:  # result, output
        while True:
            instr = self.next_instr()

            rs = self.call(instr)
            if rs or instr.opcode == Opcode.Halt:
                return ReturnVal(RunResult.Halted, rs)

            if self.peek_instr().opcode == Opcode.Input and not self.inbuffer:
                return ReturnVal(RunResult.NeedInput, 0)

            if instr.opcode == Opcode.Output:
                return ReturnVal(RunResult.HasOutput, self.outbuffer[-1])

    def finalstate(self):
        self.run()
        return self.data

    def putaddr(self, idx: int, val=0):
        self.data[idx] = val

    def next_instr(self) -> Instruction:
        instr = self.peek_instr()
        self.step(instr.size)
        return instr

    def peek_instr(self) -> Instruction:
        raw_opcode = str(self.data[self.ptr])
        instr = Instruction(Opcode(int(raw_opcode[-2:])))

        def get_mode(param_no: int) -> ParamMode:
            offset = -3 - param_no
            modeflag = int(raw_opcode[offset]) if len(raw_opcode) >= abs(offset) else 0
            return ParamMode(modeflag)

        for x in range(0, instr.num_params):
            mode = get_mode(x)
            instr.modes[x] = mode
            instr.params[x] = self.data[self.ptr + x + 1]
        return instr

    def call(self, instr: Instruction):
        def resolve_addr(i: int):
            if instr.modes[i] == ParamMode.Positional:
                return instr.params[i]
            elif instr.modes[i] == ParamMode.Relative:
                return self.ptroffset + instr.params[i]

        def deref(i: int):
            if instr.modes[i] == ParamMode.Immediate:
                return instr.params[i]
            return self.data[resolve_addr(i)]

        if instr.opcode == Opcode.Add:
            self.putaddr(resolve_addr(2), deref(0) + deref(1))

        elif instr.opcode == Opcode.Mul:
            self.putaddr(resolve_addr(2), deref(0) * deref(1))

        elif instr.opcode == Opcode.Input:
            self.putaddr(resolve_addr(0), self.readbuffer())

        elif instr.opcode == Opcode.Output:
            self.outbuffer.append(deref(0))

        elif instr.opcode == Opcode.JumpIfTrue:
            if not deref(0) == 0:
                self.ptr = deref(1)

        elif instr.opcode == Opcode.JumpIfFalse:
            if deref(0) == 0:
                self.ptr = deref(1)

        elif instr.opcode == Opcode.LessThan:
            self.putaddr(resolve_addr(2), 1 if deref(0) < deref(1) else 0)

        elif instr.opcode == Opcode.Equals:
            self.putaddr(resolve_addr(2), 1 if deref(0) == deref(1) else 0)

        elif instr.opcode == Opcode.ChangePtrOffset:
            self.ptroffset += deref(0)

        elif instr.opcode == Opcode.Halt:
            return self.halt()

        else:
            raise Exception(f"Illegal opcode {instr.opcode}. System on fire.")

    def step(self, steps=1):
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
