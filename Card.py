class Card:
    def __init__(self, rank, suit, value):

        self.rank = rank
        self.suit = suit
        self.value = value

        print(f"Card rank: {self.rank}")
        print(f"Card suit: {self.suit}")
        print(f"Card value: {self.value}")


    def new_deck(self):

        self.card_list = []
        self.suit_list = ["Spades", "Hearts", "Clubs", "Diamonds"]
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

            for card in self.card_list:
                print(f" {card.rank} of {card.suit}, Value: {card.value}")

instance = Card("Ace", "Spades", 11)
instance.new_deck()


