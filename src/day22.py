from collections import deque
import itertools


class Deck:
    cards: deque

    def __init__(self, raw: str) -> None:
        self.cards = deque([int(card) for card in reversed(raw.splitlines()[1:])])

    def add_to_deck(self, card1: int, card2: int) -> None:
        cards = [card1, card2]
        for card in sorted(cards, reverse=True):
            self.cards.appendleft(card)

    def calc_score(self):
        return sum(c * n for c, n in zip(self.cards, itertools.count(1)))


class Game:
    player1: Deck
    player2: Deck

    def __init__(self, raw: str) -> None:
        self.player1, self.player2 = [Deck(block) for block in raw.split("\n\n")]

    def take_turn(self) -> None:
        card1 = self.player1.cards.pop()
        card2 = self.player2.cards.pop()
        if card1 > card2:
            self.player1.add_to_deck(card1, card2)
            print([c for c in reversed(self.player1.cards)])
            print([c for c in reversed(self.player2.cards)])
            return 1
        else:
            self.player2.add_to_deck(card1, card2)
            print([c for c in reversed(self.player1.cards)])
            print([c for c in reversed(self.player2.cards)])
            return 2

    def play_to_end(self) -> None:
        turn = 0
        while self.player1.cards and self.player2.cards:
            turn += 1
            winner = self.take_turn()
            print(f"Player {winner} wins round {turn}!")
            print([c for c in reversed(self.player1.cards)])
            print([c for c in reversed(self.player2.cards)])
        if self.player1.cards:
            print("Player 1 wins, score = ", self.player1.calc_score())
            return self.player1.calc_score()
        else:
            print("Player 2 wins, score = ", self.player2.calc_score())
            return self.player2.calc_score()


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

game = Game(RAW)
assert game.play_to_end() == 306

## Problem
with open("../inputs/day22.txt") as f:
    raw = f.read()
the_game = Game(raw)
print(the_game.play_to_end())