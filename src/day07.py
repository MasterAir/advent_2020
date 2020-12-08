from typing import Dict, Set


class Rules:
    bag_contents: Dict[str, Dict]

    def __init__(self, raw: str) -> None:
        self.bag_contents = {}
        for rule in raw.split("\n"):
            colour, content_dict = parse_rule(rule)
            self.bag_contents[colour] = content_dict

    def can_be_in(self, colour) -> Set:
        baglist = set([colour])
        no_of_colours = len(baglist)
        old_no_of_colours = 0

        while no_of_colours != old_no_of_colours:
            for bag_col in self.bag_contents:
                if baglist.intersection(self.bag_contents[bag_col]):
                    baglist.add(bag_col)
            old_no_of_colours, no_of_colours = no_of_colours, len(baglist)

        baglist.remove(colour)
        return baglist

    def how_many_bags(self, colour) -> int:
        if len(self.bag_contents[colour]) == 0:
            return 0
        bags = 0
        for col in self.bag_contents[colour]:
            bags += self.bag_contents[colour][col] + self.bag_contents[colour][
                col
            ] * self.how_many_bags(col)
        print(colour, bags)
        return bags


def parse_rule(rule: str) -> (str, Dict):
    colour, contents = rule.split(" bags contain ")
    content_dict = {}

    if contents.endswith("no other bags."):
        return colour, {}

    for rule in contents.split(","):
        words = rule.split()[:-1]
        number = int(words[0])
        bag_colour = " ".join(words[1:])
        content_dict[bag_colour] = number
    return colour, content_dict


DUMMY = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

ruleset = Rules(DUMMY)
shiny_gold = ruleset.can_be_in("shiny gold")
assert len(shiny_gold) == 4

with open("../inputs/day07.txt") as f:
    ruleset = Rules(f.read())
shiny_gold = ruleset.can_be_in("shiny gold")
print(shiny_gold)
print(len(shiny_gold))

bags = ruleset.how_many_bags("shiny gold")
print(bags)