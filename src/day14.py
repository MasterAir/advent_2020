from __future__ import annotations

from typing import Dict, NamedTuple


def to_36_binary(i: int) -> str:
    return bin(int(i)).replace("0b", "").zfill(36)


class Instruction(NamedTuple):
    inst: str
    loc: int
    val: str

    def parse(line: str) -> Instruction:
        a1, a2 = line.split("=")
        if "[" in a1:
            inst, loc = a1.split("[")
            inst = inst.strip()
            loc = int(loc.strip()[:-1])
            val = bin(int(a2)).replace("0b", "").zfill(36)
        else:
            inst = a1.strip()
            loc = 0
            val = a2.strip()
        return Instruction(inst, loc, val)


def apply_mask(mask: str, xs: str, val: str) -> str:
    answer = ""
    xs = list(xs)
    for c, v in zip(mask, val):
        if c == "0":
            answer += v
        elif c == "1":
            answer += c
        elif c == "X":
            answer += xs.pop()
        else:
            raise RuntimeError(f"unexpected mask {mask}")
    return answer


class Computer:
    memory: Dict[int:str]  # binary representation of mem i
    mask: str

    def __init__(self):
        self.mask = "X" * 36
        self.memory = {}

    def execute(self, inst: Instruction) -> None:
        if inst.inst == "mask":
            self.mask = inst.val

        if inst.inst == "mem":
            to_mem = "".join(
                [m if m != "X" else v for m, v in zip(self.mask, inst.val)]
            )
            try:
                self.memory[inst.loc] = to_mem
            except Exception as e:
                print(e)
                breakpoint()

    def execute2(self, inst: Instruction) -> None:
        if inst.inst == "mem":
            for i in range(2 ** self.mask.count("X")):
                mask_float = bin(i).replace("0b", "").zfill(self.mask.count("X"))
                addr = to_36_binary(inst.loc)
                addr = apply_mask(self.mask, mask_float, addr)
                addr = int(addr, 2)
                self.memory[addr] = inst.val
        elif inst.inst == "mask":
            self.mask = inst.val
        else:
            raise RuntimeError(f"bad instruction {inst}")


## Unit test
RAW = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

instructions = []
for line in RAW.split("\n"):
    instructions.append(Instruction.parse(line))

test_c = Computer()
for inst in instructions:
    test_c.execute(inst)

# assert (sum(int(i, 2) for i in test_c.memory.values())) == 165

## Problem
with open("../inputs/day14.txt") as f:
    insts = [Instruction.parse(line) for line in f]

real_comp = Computer()

for inst in insts:
    real_comp.execute(inst)
print(sum(int(i, 2) for i in real_comp.memory.values()))

real_comp2 = Computer()
for inst in insts:
    real_comp2.execute2(inst)
print(sum(int(i, 2) for i in real_comp2.memory.values()))