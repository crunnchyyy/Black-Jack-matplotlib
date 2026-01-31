import random
from settings import *
from card import Card


class Setup:

    def __init__(self):

        self.card_list = []
        self.suit_list = ["Spades", "Hearts", "Clubs", "Diamonds"]
        self.cc_loc = cut_card_location

    def run(self, decks):
        self.new_shoe(decks)

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

        # For testing purposes
        #for card in self.card_list:
        #   print(f" {card.rank} of {card.suit}, Value: {card.value}")
        #print("\n\n\n\n")

        # Return to game
        return self.card_list



    def new_deck(self):

        # For each suit
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
