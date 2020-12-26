from collections import deque
import itertools
from typing import Set, Tuple


class Deck:
    cards: deque

    def __init__(self, raw: str) -> None:
        self.cards = deque([int(card) for card in reversed(raw.splitlines()[1:])])

    def add_to_deck(self, card1: int, card2: int, winner: int) -> None:
        if winner == 1:
            self.cards.appendleft(card1)
            self.cards.appendleft(card2)
        else:
            self.cards.appendleft(card2)
            self.cards.appendleft(card1)

    def calc_score(self):
        return sum(c * n for c, n in zip(self.cards, itertools.count(1)))


class Game:
    player1: Deck
    player2: Deck
    recursive: bool
    history: Set[Tuple[int]]

    def __init__(
        self,
        raw: str = None,
        recursive: bool = False,
        deck1: Deck = None,
        deck2: Deck = None,
    ) -> None:
        if deck1:
            if not deck2:
                raise RuntimeError("either both or neither deck must be given")
            self.player1 = deck1
            self.player2 = deck2
        elif raw:
            self.player1, self.player2 = [Deck(block) for block in raw.split("\n\n")]
        else:
            raise RuntimeError("You need to give a deck or a string")
        self.recursive = recursive
        self.history = set()

    def log_turn(self) -> bool:
        record = tuple(self.player1.cards) + (-1,) + tuple(self.player2.cards)
        if record in self.history:
            print("player 1 wins by repetition")
            return True
        else:
            self.history.add(record)
            return False

    def take_turn(self) -> None:
        card1 = self.player1.cards.pop()
        card2 = self.player2.cards.pop()

        if (
            self.recursive
            and len(self.player1.cards) >= card1
            and len(self.player2.cards) >= card2
        ):
            # print(self.write_gamestate(card1, card2))
            sub_game = Game(self.write_gamestate(card1, card2), recursive=True)
            score = sub_game.play_to_end()
            if score > 0:
                winner = 1
            else:
                winner = 2
        else:
            if card1 > card2:
                winner = 1
            else:
                winner = 2
        if winner == 1:
            self.player1.add_to_deck(card1, card2, winner)
            # print([c for c in reversed(self.player1.cards)])
            # print([c for c in reversed(self.player2.cards)])
            return 1
        else:
            self.player2.add_to_deck(card1, card2, winner)
            # print([c for c in reversed(self.player1.cards)])
            # print([c for c in reversed(self.player2.cards)])
            return 2

    def play_to_end(self) -> None:
        turn = 0
        while self.player1.cards and self.player2.cards:
            turn += 1
            winner = self.take_turn()
            # print(f"Player {winner} wins round {turn}!")
            # print([c for c in reversed(self.player1.cards)])
            # print([c for c in reversed(self.player2.cards)])
            if self.log_turn():
                break
        if self.player1.cards:
            # print("Player 1 wins, score = ", self.player1.calc_score())
            return self.player1.calc_score()
        else:
            # print("Player 2 wins, score = ", self.player2.calc_score())
            return -self.player2.calc_score()

    def write_gamestate(self, card1, card2) -> str:
        out = ""
        out += "Player 1:\n"
        p1 = self.player1.cards.copy()
        for _ in range(card1):
            out += str(p1.pop()) + "\n"
        out += "\n"
        out += "Player 2:\n"
        p2 = self.player2.cards.copy()
        for _ in range(card2):
            out += str(p2.pop()) + "\n"
        return out


RAW = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
"""

# game = Game(RAW)
# assert game.play_to_end() == -306

game = Game(RAW, recursive=True)
print(game.play_to_end())


# RAW2 = """Player 1:
# 43
# 19

# Player 2:
# 2
# 29
# 14"""

# repeat_game = Game(RAW2)
# repeat_game.play_to_end()

## Problem
# with open("../inputs/day22.txt") as f:
#     raw = f.read()
# the_game = Game(raw)
# print(the_game.play_to_end())


with open("../inputs/day22.txt") as f:
    raw = f.read()
the_game = Game(raw, recursive=True)
print(the_game.play_to_end())