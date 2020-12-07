from string import ascii_lowercase

all_answers = set([c for c in ascii_lowercase])


def count_unique(answers: str) -> int:
    unique = set()
    for c in answers:
        if c.isalpha():
            unique.add(c)
    return len(unique)


def count_all(answers: str, all_answers=all_answers) -> int:
    everyone = all_answers
    for person in answers.split("\n"):
        everyone = everyone.intersection(set(c for c in person))
    return len(everyone)


RAW = """abc

a
b
c

ab
ac

a
a
a
a

b"""

for s in RAW.split("\n\n"):
    print(count_all(s))

with open("../inputs/day06.txt") as f:
    inp = f.read().split("\n\n")

print(sum(count_all(group) for group in inp))