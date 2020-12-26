from __future__ import annotations
from typing import NamedTuple, Tuple, Dict


class Rule(NamedTuple):
    baserule: bool  # Is this rule a single character
    rulesets: List[List[int]]
    character: str

    def __repr__(self) -> str:
        if self.baserule:
            return f'"{self.character}"'
        else:
            strings = [" ".join([str(i) for i in group]) for group in self.rulesets]
            return " | ".join(strings)

    @staticmethod
    def parse(line: str) -> Rule:
        if '"' in line:
            baserule = True
            ruleset = []
            character = line.strip().strip('"')
        else:
            baserule = False
            ruleset = [[int(i) for i in rule.split()] for rule in line.split("|")]
            character = ""
        return Rule(baserule, ruleset, character)


level = 0


class Ruleset:
    rules = Dict[int, Rule]
    level: int

    def __init__(self, raw: str):
        rules = {}
        for line in raw.split("\n"):
            if ":" in line:
                i, rule = line.split(":")
                rules[int(i)] = Rule.parse(rule)
            else:
                print(f"{line} not parsed")
        self.rules = rules
        self.level = 0

    def is_valid(
        self, rule_id: int, s: str, depth: int = 0, verbose: bool = False
    ) -> Tuple[bool, int]:
        rule = self.rules[rule_id]
        if verbose:
            print()
            print(depth * ">", f"checking {rule_id}: {rule} with string {s}")
        if rule.baserule:
            self.level -= 1
            if rule.character in s:
                substring = s[s.index(rule.character) + 1 :]
                if verbose:
                    print(
                        ">" * depth,
                        f"{rule} is valid for {s} leaving substring {substring}",
                    )
                return rule.character in s, substring
            else:
                if verbose:
                    print(">" * depth, f"{rule_id}: {rule} is invalid for {s}")
                return False, s

        else:
            long_substring = ""
            valid = False
            for r in rule.rulesets:
                substring = s

                for i in r:
                    validity, substring = self.is_valid(
                        i, substring, depth=depth + 1, verbose=verbose
                    )
                    if not validity:
                        break
                if validity and len(substring) >= len(long_substring):
                    long_substring = substring
                    valid = validity
            if valid:
                if verbose:
                    print(
                        depth * ">", f"{rule} is valid for {s} leaving {long_substring}"
                    )
                return True, long_substring
            else:
                if verbose:
                    print(depth * ">", f"{rule} is invalid for {s}")
                return False, s

    def is_0_valid_repeating(self, s: str) -> bool:
        breakpoint()
        v, sub = self.is_valid(42, s)
        if not v:
            return False
        while v:
            v, sub = self.is_valid(31, sub)
            if sub == "":
                return True
        return False


### Unit test
RAW = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"
"""

strings = """ababbb
bababa
abbbab
aaabbb
aaaabbb"""

rules_str = RAW.split("\n\n")[0]
print(rules_str)
RULES = Ruleset(rules_str)

STRINGS = strings.split("\n")

VALID_STRINGS = []
for string in STRINGS:
    v, subs = RULES.is_valid(0, string)
    if v:
        print(v, subs)
    if v and len(subs) == 0:
        VALID_STRINGS.append(string)
print(len(VALID_STRINGS))


RAW2 = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1"""

STRINGS2 = """abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""

RULES2 = Ruleset(RAW2)
STRINGS2 = STRINGS2.split("\n")

valid_strings = []
for string in STRINGS2:
    v, subs = RULES2.is_valid(0, string)
    if v and len(subs) == 0:
        valid_strings.append(string)
print(len(valid_strings))


valid_rep_strings = []
for string in STRINGS2:
    if RULES2.is_0_valid_repeating(string):
        valid_rep_strings.append(string)
print(valid_rep_strings)
print(len(valid_rep_strings))


## Problem

# with open("../inputs/day19.txt") as f:
#     raw = f.read()
# rules, strings = raw.split("\n\n")
# the_rules = Ruleset(rules)
# strings = strings.split("\n")


# valid_strings = []
# for string in strings:
#     v, subs = the_rules.is_valid(0, string)
#     if v and len(subs) == 0:
#         valid_strings.append(string)
# print(len(valid_strings))


# valid_rep_strings = []
# for string in strings:
#     if the_rules.is_0_valid_repeating(string):
#         valid_rep_strings.append(string)

# print(len(valid_rep_strings))