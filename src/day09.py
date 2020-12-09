from typing import List, Tuple


def find_summing_pair(code, target) -> bool:
    needs = set(target - i for i in code)
    for i in code:
        if (i in needs) and (target / 2 != i):
            return True
    return False


def xmas_breaker(code: List[int], preamble: int) -> int:
    recent = code[:preamble]
    for i in code[preamble:]:
        if not find_summing_pair(recent, i):
            return i
        recent.pop(0)
        recent.append(i)
    raise RuntimeError("Could not find breaker")


def find_set(code: List[int], target: int) -> Tuple[int, int]:
    for i in range(len(code)):
        total = 0
        j = i
        while total < target:
            total += code[j]
            j += 1
        if total == target:
            return min(code[i:j]), max(code[i:j])
    raise RuntimeError("Did not find sequence")


recent = list(range(1, 26))
find_summing_pair(recent, 26)

RAW = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""

CODE = [int(i) for i in RAW.split("\n")]
assert xmas_breaker(CODE, 5) == 127
assert find_set(CODE, 127) == (15, 47)
print(find_set(CODE, 127))
with open("../inputs/day09.txt") as f:
    code = [int(line) for line in f]

secret = xmas_breaker(code, 25)
print(secret)
min_c, max_c = find_set(code, secret)
print(min_c + max_c)
