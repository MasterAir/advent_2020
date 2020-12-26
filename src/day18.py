from __future__ import annotations
import re


def get_first_brackets(math: str, inc_parentheses: bool = False) -> str:
    counter = 0
    out = ""
    for c in math[math.index("(") + 1 :]:
        out += c
        if c == "(":
            counter += 1
        if c == ")":
            counter -= 1
        if counter < 0:
            if inc_parentheses:
                return f"({out}"
            else:
                return out[:-1]
    raise RuntimeError(f"Unmatched parenthesis in {math}")


def get_first_add(math: str) -> str:
    return re.search("[0-9]+\s*[\+]\s*[0-9]+", math).group()


def get_first_sum(math: str) -> str:
    return re.search("[0-9]+\s*[\+|\*]\s*[0-9]+", math).group()


def calc_simple_sum(math: str) -> str:
    if "+" in math:
        a, b = math.split("+")
        return str(int(a) + int(b))
    elif "*" in math:
        a, b = math.split("*")
        return str(int(a) * int(b))


def bad_calc(math: str) -> str:
    if not re.search("\*|\+|\(", math):
        return math

    if "(" in math:
        math = math.replace(
            get_first_brackets(math, True), bad_calc(get_first_brackets(math)), 1
        )
        return bad_calc(math)
    if re.search("\+|\*", math):
        math = math.replace(
            get_first_sum(math), calc_simple_sum(get_first_sum(math)), 1
        )
        return bad_calc(math)


def bad_calc2(math: str) -> str:
    if not re.search("\*|\+|\(", math):
        return math

    if "(" in math:
        math = math.replace(
            get_first_brackets(math, True), bad_calc2(get_first_brackets(math)), 1
        )
        return bad_calc2(math)
    elif "+" in math:
        math = math.replace(
            get_first_add(math), calc_simple_sum(get_first_add(math)), 1
        )
        return bad_calc2(math)
    elif "*" in math:
        math = math.replace(
            # this works because there's no + in math
            get_first_sum(math),
            calc_simple_sum(get_first_sum(math)),
            1,
        )
        return bad_calc2(math)


## Unit tests
assert int(bad_calc("2 * 3 + (4 * 5)")) == 26
assert int(bad_calc("5 + (8 * 3 + 9 + 3 * 4 * 3)")) == 437
assert int(bad_calc("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")) == 12240
assert int(bad_calc("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")) == 13632

assert int(bad_calc2("1 + (2 * 3) + (4 * (5 + 6))")) == 51
assert int(bad_calc2("2 * 3 + (4 * 5)")) == 46
assert int(bad_calc2("5 + (8 * 3 + 9 + 3 * 4 * 3)")) == 1445
assert int(bad_calc2("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")) == 669060
assert int(bad_calc2("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")) == 23340
## problem

with open("../inputs/day18.txt") as f:
    answers = [int(bad_calc(line)) for line in f]

with open("../inputs/day18.txt") as f:
    answers2 = [int(bad_calc2(line)) for line in f]
print(sum(answers))
print(sum(answers2))
