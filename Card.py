import random
from types import new_class


class Card:
    def __init__(self, rank, suit, value):

        self.rank = rank
        self.suit = suit
        self.value = value

        print(f"Card rank: {self.rank}")
        print(f"Card suit: {self.suit}")
        print(f"Card value: {self.value}")



instance = Card("Ace", "Spades", 11)


