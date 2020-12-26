from __future__ import annotations
from typing import List, NamedTuple, Dict

"""
In this game, the players take turns saying numbers. 
They begin by taking turns reading from a list of starting numbers (your puzzle input). 
Then, each turn consists of considering the most recently spoken number:
If that was the first time the number has been spoken, the current player says 0.
Otherwise, the number had been spoken before; the current player announces how many turns 
apart the number is from when it was previously spoken.

0,3,6 -> 0, 3, 6, 0, 3, 3, 1, 0, 4,
"""


class Game:
    turn: int
    prev: int
    last_spoken: Dict[int, int]

    def __init__(self, start: List[int]) -> Game:
        last_spoken = {}
        turn = 1
        for i in start[:-1]:
            last_spoken[i] = turn
            turn += 1
        self.turn = turn
        self.prev = start[-1]
        self.last_spoken = last_spoken

    def take_turn(self) -> Game:
        turn = self.turn + 1
        if self.prev in self.last_spoken:
            prev = self.turn - self.last_spoken[self.prev]
        else:
            prev = 0
        self.last_spoken[self.prev] = self.turn
        self.prev = prev
        self.turn = turn


g = Game([0, 3, 6])
while g.turn < 2020:
    g.take_turn()
assert g.prev == 436

g = Game([1, 3, 2])
while g.turn < 2020:
    g.take_turn()
assert g.prev == 1

g = Game([1, 2, 3])
while g.turn < 2020:
    g.take_turn()
assert g.prev == 27

g = Game([2, 1, 3])
while g.turn < 2020:
    g.take_turn()
assert g.prev == 10


# g = Game([0, 3, 6])
# while g.turn < 30000000:
#     if g.turn % 100000 == 0:
#         print(g.turn)
#         print(len(g.last_spoken))
#     g.take_turn()
# assert g.prev == 175594

# g = Game.from_list([1, 3, 2])
# while g.turn < 30000000:
#     g = g.take_turn()
# assert g.prev == 2578

# g = Game.from_list([1, 2, 3])
# while g.turn < 30000000:
#     g = g.take_turn()
# assert g.prev == 261214

# g = Game.from_list([2, 1, 3])
# while g.turn < 30000000:
#     g = g.take_turn()
# assert g.prev == 3544142


g = Game([11, 18, 0, 20, 1, 7, 16])
while g.turn < 30000000:
    if g.turn % 1000000 == 0:
        print(g.turn)
        print(len(g.last_spoken))
    g.take_turn()
print(g.prev)
