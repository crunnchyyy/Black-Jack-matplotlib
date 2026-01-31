import random
from types import new_class


class Card:
    def __init__(self, rank, suit, value):

        self.rank = rank
        self.suit = suit
        self.value = value

        self.card_list = []
        self.suit_list = ["Spades", "Hearts", "Clubs", "Diamonds"]

    def new_shoe(self, decks):

        for x in range(decks):
            # Add full deck of cards to card_list
            self.new_deck()

        # Shuffle full shoe
        random.shuffle(self.card_list)

        # Get cut card location
        cc_loc = int(len(self.card_list) * 0.75)
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
                self.card_list.append(Card(str(x+2), suit, x+2))

            # Add Face cards
            self.card_list.append(Card("Jack", suit, 10))
            self.card_list.append(Card("Queen", suit, 10))
            self.card_list.append(Card("King", suit, 10))


instance = Card("Ace", "Spades", 11)
instance.new_shoe(1)


