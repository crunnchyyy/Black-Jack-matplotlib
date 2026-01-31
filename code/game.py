from settings import *
import setup

class Game:
    def __init__(self):

        self.setup = setup.Setup()
        self.card_list = []
        self.hand_num = 0
        self.balance = starting_chips
        self.cc_loc = cut_card_location
        self.hand_list = []
        self.hand_value = 0

    def run(self):
        print("called")
        self.setup.new_shoe(shoe_size)
        self.card_list = self.setup.new_shoe(shoe_size)
        self.new_hand()


    def new_hand(self):

        # Increment hand number and output
        self.hand_num += 1
        print(f"\n\n Hand {self.hand_num}!")

        # Add cards to hand
        for i in range(2):
            self.hand_list.append(self.card_list.pop(0))

            # Check if cut card drawn
            if self.hand_list[i].rank == "Cut Card":
                self.shuffle_shoe()

        for card in self.hand_list:
            self.hand_value = self.hand_value + card.value
            print(f" {card.rank} of {card.suit}")

        print(f"\nHand value: {self.hand_value}")

        self.action()

    def shuffle_shoe(self):

        cc_index = (len(self.hand_list) - 1)

        # reshuffle shoe
        print("Cut card drawn! reshuffling shoe...")
        self.setup.new_shoe(shoe_size)

        # Replace cut card
        self.hand_list.pop(cc_index)
        self.hand_list.append(self.card_list.pop(0))

    def action(self):

        while self.hand_value < 21:
            try:
                action = str(input("Hit or Stand? (h/s): ")).lower()
                if action == "h":
                    self.hit()
                elif action == "s":
                    print("stand")
                else:
                    print("please enter either h or s")
                    self.action()
            except ValueError:
                print("Unexpected input received")

    def hit(self):

        # Add new card to hand
        self.hand_list.append(self.card_list.pop(0))

        # Find new card
        new_index = (len(self.hand_list) - 1)
        new_rank = self.hand_list[new_index].rank
        new_suit = self.hand_list[new_index].suit

        # Output
        self.hand_value = self.hand_value + self.hand_list[new_index].value
        print(f" {new_rank} of {new_suit}")
        print(f"\nHand value: {self.hand_value}")