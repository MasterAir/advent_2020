from __future__ import annotations

from typing import NamedTuple, Tuple, List, Dict
import re


class Rule(NamedTuple):
    thing: str
    ranges: List[Tuple[int, int]]

    def parse(line: str) -> Rule:
        thing = re.search("^[^:]*:", line).group().strip(":")
        ranges = re.findall("[0-9]*-[0-9]*", line)
        ranges = [tuple(int(i) for i in allowed.split("-")) for allowed in ranges]
        return Rule(thing, ranges)

    def is_valid(self, i: int) -> bool:
        return any([ok[0] <= i <= ok[1] for ok in self.ranges])


def parse_input(raw: str) -> Tuple(List[Rule], List[int], List[List[int]]):
    rules, my_ticket, other_tickets = raw.split("\n\n")

    rules = [Rule.parse(line) for line in rules.split("\n")]

    # Take the second line of the block
    my_ticket = my_ticket.split("\n")[1]
    my_ticket = [int(i) for i in my_ticket.split(",")]

    # Drop the 'other tickets' header line
    other_tickets = other_tickets.split("\n")[1:]
    other_tickets = [[int(i) for i in line.split(",")] for line in other_tickets]
    return rules, my_ticket, other_tickets


def int_is_ok(i: int, rules: List[Rule]) -> bool:
    return any(rule.is_valid(i) for rule in rules)


def ticket_is_ok(ticket: List[int], rules: List[Rule]) -> List[int]:
    return [0 if int_is_ok(i, rules) else i for i in ticket]


def ticket_is_valid(ticket: List[int], rules: List[Rule]) -> List[int]:
    return all([int_is_ok(i, rules) for i in ticket])


def work_out_order(tickets: List[List[int]], rules) -> List[Dict[str, bool]]:
    # Each thing could be anything
    possible_things = [{rule.thing: True for rule in rules} for _ in tickets[0]]

    for ticket in tickets:
        if not ticket_is_valid(ticket, rules):
            # ticket is invalid
            continue
        for idx, i in enumerate(ticket):
            for rule in rules:
                possible_things[idx][rule.thing] = possible_things[idx][
                    rule.thing
                ] and rule.is_valid(i)
    return possible_things


def find_error_rate(tickets: List[List[int]], rules: List[Rule]) -> int:
    total = 0
    for ticket in tickets:
        total = total + sum(ticket_is_ok(ticket, rules))
    return total


def find_next_answer(answers: List[str], possibles: Dict[str, bool]) -> str:
    for p in possibles:
        if possibles[p] and p not in answers:
            return p
    print(answers, possibles)
    raise RuntimeError("IMPOSSIBLE")


def solve_possible_things(possibles: List[Dict[str:bool]]) -> List[str]:
    answer = [""] * len(possibles)
    count_poss = [sum(p.values()) for p in possibles]
    print(count_poss)

    order = {v - 1: ix for ix, v in enumerate(count_poss)}

    for i in range(len(possibles)):
        idx = order[i]
        p = possibles[idx]
        # print(sum(p.values()), idx)
        if sum(p.values()) - i > 1:
            raise RuntimeError("Uh oh, this might be hard")
        answer[idx] = find_next_answer(answer, p)
        # print(p, answer[idx])
    return answer


## Unit test

RAW = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""

RULES, MY_TICKET, OTHER_TICKETS = parse_input(RAW)
assert find_error_rate(OTHER_TICKETS, RULES) == 71

RAW2 = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
15,1,5
3,9,18
5,14,9"""

RULES2, MY_TICKET2, OTHER_TICKETS2 = parse_input(RAW2)
possibles = work_out_order(OTHER_TICKETS2, RULES2)
print(possibles)
order = solve_possible_things(possibles)
labelled_ticket = {thing: value for thing, value in zip(order, MY_TICKET2)}
print(labelled_ticket)

## Problem

with open("../inputs/day16.txt") as f:
    raw = f.read()
rules, my_tickets, other_tickets = parse_input(raw)
for rule in rules:
    print(rule)
print(find_error_rate(other_tickets, rules))
possibles = work_out_order(other_tickets, rules)
order = solve_possible_things(possibles)
labelled_ticket = {thing: value for thing, value in zip(order, my_tickets)}
product = 1
for thing in labelled_ticket:
    if thing.startswith("departure"):
        print(thing, labelled_ticket[thing])
        product *= labelled_ticket[thing]

print("ANSWER:", product)
