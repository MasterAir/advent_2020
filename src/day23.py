from __future__ import annotations
from typing import List

# Cups is the list of cups, the current cup is in position 0 and the list is clockwise
Cups = List[int]

"""
Each move, the crab does the following actions:

* The crab picks up the three cups that are immediately clockwise of the current cup. They are removed from the circle; cup spacing is adjusted as necessary to maintain the circle.
* The crab selects a destination cup: the cup with a label equal to the current cup's label minus one. If this would select one of the cups that was just picked up, the crab will keep subtracting one until it finds a cup that wasn't just picked up. If at any point in this process the value goes below the lowest value on any cup's label, it wraps around to the highest value on any cup's label instead.
* The crab places the cups it just picked up so that they are immediately clockwise of the destination cup. They keep the same order as when they were picked up.
* The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
"""


def create_a_hundred_cups(raw: str) -> Cups:
    some_cups = [int(c) for c in raw]
    a_hundred_cups = some_cups + list(range(len(some_cups) + 1, 10 ** 2 + 1))
    return a_hundred_cups


def create_n_cups(raw: str, n: int) -> Cups:
    cups = {i: i + 1 for i in range(n)}
    # rearrange the first few
    for c, nc in zip(raw, raw[1:]):
        cups[int(c)] = int(nc)
    # make it a loop
    if len(raw) == n:
        cups.pop(0)
        cups[int(raw[-1])] = int(raw[0])
    elif len(raw) == n - 1:
        cups[0] = int(raw[0])
        cups[int(raw[-1])] = 0
    else:
        cups[0] = int(raw[0])
        cups[int(raw[-1])] = max([int(c) for c in raw]) + 1
        cups[n - 1] = 0
    return cups


def take_turn2(place: int, cups: Dict[int]) -> int:
    next_3 = []
    cup = place

    for _ in range(3):
        cup = cups[cup]
        next_3.append(cup)
    cups[place] = cups[next_3[-1]]

    destination = place - 1
    while destination in next_3 or destination < 0:
        destination = destination - 1
        if destination < 0:
            destination = max(cups)

    cups[next_3[-1]] = cups[destination]
    cups[destination] = next_3[0]
    return cups[place]


def print_cups(cups: Dict[int], place: int, char: int = 9):
    out = ""
    for _ in range(char):
        out += str(place) + " "
        place = cups[place]
    return out


def create_cups(raw: str) -> Cups:
    return [int(c) for c in raw]


def take_turn(cups: Cups) -> None:
    """
    Update the list of cups for after the crab has taken a turn

    Parameters
    ----------
    cups : Cups
        starting position of the cups
    """
    highest = max(cups)
    current_cup = cups[0]
    picked_up = cups[1:4]
    cups = cups[:1] + cups[4:]

    destination_cup = current_cup - 1
    lookup = set(cups)
    while destination_cup not in lookup:
        destination_cup = (destination_cup - 1) % (highest + 1)
    # print(destination_cup)
    # Put the cups back after the location of the destination cup
    destination = cups.index(destination_cup) + 1

    cups = cups[:destination] + picked_up + cups[destination:]
    cups = cups[1:] + cups[:1]
    return cups


def print_after_1(cups: Cups) -> str:
    after_1 = cups.index(1) + 1
    return "".join(str(i) for i in (cups[after_1:] + cups[: after_1 - 1]))


## Unit test:
cups = create_cups("389125467")
for _ in range(10):
    print(cups)
    cups = take_turn(cups)
assert print_after_1(cups) == "92658374"


cups = create_cups("389125467")
for _ in range(100):
    cups = take_turn(cups)
assert print_after_1(cups) == "67384529"

# cups = create_n_cups("389125467", 1_000_000)
# place = 3
# for i in range(10_000_000):
#     if i // 100_000 == 0:
#         print(100 * i / 10_000_000)
#     place = take_turn2(place, cups)
# print(print_cups(cups, 1))


# Problem

# cups = create_cups("925176834")

# for _ in range(100):
#     cups = take_turn(cups)
# print(print_after_1(cups))

cups = create_n_cups("925176834", 1_000_000)
place = 9
for i in range(10_000_000):
    if i // 100_000 == 0:
        print(100 * i / 10_000_000)
    place = take_turn2(place, cups)
print(print_cups(cups, 1))