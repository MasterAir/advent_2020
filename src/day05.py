from typing import List


def find_seat_id(inp: str) -> int:
    row, col = inp[:7], inp[7:]
    row = int(row.replace("F", "0").replace("B", "1"), 2)
    col = int(col.replace("L", "0").replace("R", "1"), 2)
    return row * 8 + col


"""
BFFFBBFRRR: row 70, column 7, seat ID 567.
FFFBBBFRRR: row 14, column 7, seat ID 119.
BBFFBBFRLL: row 102, column 4, seat ID 820.
"""
assert find_seat_id("BFFFBBFRRR") == 567
assert find_seat_id("FFFBBBFRRR") == 119
assert find_seat_id("BBFFBBFRLL") == 820

max_seat = 0
with open("../inputs/day05.txt") as f:
    seats = [find_seat_id(line) for line in f]


def find_missing(inp: List[int]) -> int:
    sort = sorted(inp)
    for i, j in zip(sort, sort[1:]):
        if i + 1 != j:
            return i + 1


print(find_missing(seats))