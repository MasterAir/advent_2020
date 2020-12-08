from __future__ import annotations

from typing import NamedTuple, List
from copy import deepcopy


class Instruction:
    op: str
    arg: int
    exe: bool

    def __init__(self, op, arg, exe):
        self.op = op
        self.arg = arg
        self.exe = exe

    def run(self) -> Tuple(int, int):
        """
        returns change to accumulator and change to pointer
        """
        if self.exe:
            raise RuntimeError("This instruction is part of an infinite loop")
        else:
            self.exe = True

        if self.op == "nop":
            return (0, 1)
        elif self.op == "jmp":
            return (0, self.arg)
        elif self.op == "acc":
            return (self.arg, 1)
        else:
            raise ValueError(f"Unexpected operation: {self.op}")

    def swap_inst(self):
        self.op = {"nop": "jmp", "jmp": "nop", "acc": "acc"}[self.op]

    @staticmethod
    def parse(line: str) -> Instruction:
        op, arg = line.split()
        arg = int(arg)
        exe = False
        return Instruction(op, arg, exe)


class Program:
    prog: List[Instruction]
    pointer: int

    def __init__(self, prog, pointer):
        self.prog = prog
        self.pointer = pointer

    def run(self, pointer=None, switch_inst=None):
        prog = deepcopy(self.prog)

        if pointer is None:
            pointer = self.pointer

        if switch_inst is not None:
            prog[switch_inst].swap_inst()

        acc = 0
        try:
            while pointer < len(prog):
                acc_, point_ = prog[pointer].run()
                acc += acc_
                pointer += point_
                # print(acc, pointer)
            return acc
        except RuntimeError:
            print(f"Encountered an infinite loop at instruction {pointer} acc = {acc}")
            raise RuntimeError

    @staticmethod
    def parse(raw: str) -> Program:
        prog = []
        for line in raw.split("\n"):
            prog.append(Instruction.parse(line))
        return Program(prog, 0)


RAW = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""


with open("../inputs/day08.txt") as f:
    prog = Program.parse(f.read())

for inst in range(len(prog.prog)):
    try:
        acc = prog.run(switch_inst=inst)
        working_inst = inst
        working_acc = acc
    except:
        pass
