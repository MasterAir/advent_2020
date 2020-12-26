from typing import Set, Dict


class Problem:
    ingredients: Set[str]
    alergens: Dict[str, Set[str]]
    known_ingredients: Dict[str, str]

    def __init__(self):
        self.ingredients = set()
        self.alergens = {}
        self.known_ingredients = {}

    def parse_line(self, line: str) -> None:
        ingredients, names = line.split(" (contains")
        ingredients = set(ingredients.split())
        names = [name.strip() for name in names[:-1].split(", ")]

        for name in names:
            if name in self.known_ingredients:
                # I already know what this is
                continue
            if name not in self.alergens:
                self.alergens[name] = ingredients
            else:
                these_alergens = self.alergens[name].intersection(ingredients)
                these_alergens = {
                    alergin
                    for alergin in these_alergens
                    if alergin not in self.known_ingredients.values()
                }
                self.alergens[name] = these_alergens
            if len(self.alergens[name]) == 1:
                self.known_ingredients[name] = min(self.alergens[name])

    def count_not_allergen(self, raw: str) -> int:
        all_allergens = set.union(*[aler for aler in self.alergens.values()])
        non_allergens = 0
        for line in raw.split("\n"):
            ingredients, names = line.split(" (contains")
            non_allergens += len(
                [
                    ingredient.strip()
                    for ingredient in ingredients.split()
                    if ingredient.strip() not in all_allergens
                ]
            )
            print(
                [
                    ingredient.strip()
                    for ingredient in ingredients.split()
                    if ingredient.strip() not in all_allergens
                ]
            )

        return non_allergens

    def print_deathlist(self):
        return ",".join(
            self.known_ingredients[s] for s in sorted(self.known_ingredients)
        )


## Unit Test
RAW = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""

old_known_ingredients = (
    1  # known ingredients starts at 0, I want the loop to execute at least once
)
problem = Problem()
while old_known_ingredients != len(problem.known_ingredients):
    old_known_ingredients = len(problem.known_ingredients)
    for line in RAW.split("\n"):
        problem.parse_line(line)

assert problem.count_not_allergen(RAW) == 5
assert problem.print_deathlist() == "mxmxvkd,sqjhc,fvjkl"

## Problem

with open("../inputs/day21.txt") as f:
    raw = f.read()

old_known_ingredients = (
    1  # known ingredients starts at 0, I want the loop to execute at least once
)
problem = Problem()
while old_known_ingredients != len(problem.known_ingredients):
    old_known_ingredients = len(problem.known_ingredients)
    for line in raw.split("\n"):
        problem.parse_line(line)

print(problem.count_not_allergen(raw))
print(problem.print_deathlist())