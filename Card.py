import random

import settings
from settings import *


class Card:
    def __init__(self, rank, suit, value):
        self.rank = rank
        self.suit = suit
        self.value = value


class Main:

    def __init__(self):

        self.card_list = []
        self.suit_list = ["Spades", "Hearts", "Clubs", "Diamonds"]
        self.hand_num = 1
        self.balance = starting_chips
        self.cc_loc = cut_card_location

    def run(self, decks):
        self.new_shoe(decks)
        self.new_hand()

    def new_hand(self):

        self.hand_num += 1
        hand_list = []
        hand_value = 0

        for x in range(2):
            hand_list.append(self.card_list.pop(0))

        for card in hand_list:
            if card.value == 12:
                self.new_shoe(settings.shoe_size)
            hand_value = hand_value + card.value
            print(f" {card.rank} of {card.suit}")

        print(f"Hand value: {hand_value}")

    def new_shoe(self, decks):

        for x in range(decks):
            # Add full deck of cards to card_list
            self.new_deck()

        # Shuffle full shoe
        random.shuffle(self.card_list)

        # Get cut card location
        cc_loc = int(len(self.card_list) * self.cc_loc)

        # Add cut card
        self.card_list.insert(cc_loc, Card("Cut Card", "None", 12))

        for card in self.card_list:
            print(f" {card.rank} of {card.suit}, Value: {card.value}")

    def new_deck(self):

        for y in range(4):

            # Decide suit by iterating through suit_list
            suit = self.suit_list[y]

            # Add Ace card
            self.card_list.append(Card("Ace", suit, 11))

            # Add numbered cards
            for x in range(9):
                self.card_list.append(Card(str(x + 2), suit, x + 2))

            # Add Face cards
            self.card_list.append(Card("Jack", suit, 10))
            self.card_list.append(Card("Queen", suit, 10))
            self.card_list.append(Card("King", suit, 10))


instance = Main()
instance.run(settings.shoe_size)
