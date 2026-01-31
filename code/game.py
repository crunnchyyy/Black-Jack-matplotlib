import time
from settings import *
import setup


class Game:
    def __init__(self):

        # Setup
        self.setup = setup.Setup()
        self.card_list = self.setup.new_shoe(shoe_size)

        # UI buffers
        self.dash = "------------"
        self.dash_small = "-----"

        # Chip number
        self.chips = starting_chips

        # Current hand
        self.hand_num = 0
        self.hand_list = []
        self.hand_value = 0

        self.dl_hand_list = []
        self.dl_hand_value = 0

    def run(self):

        # Make new shoe
        self.setup.new_shoe(shoe_size)

        # Update card list
        self.card_list = self.setup.new_shoe(shoe_size)

        # Start game
        self.new_hand()


    def new_hand(self):
        # Increment hand number and start hand
        self.hand_num += 1
        print(f"{self.dash}\nHand {self.hand_num}!\n{self.dash}")
        print("Player's draw:\n")
        time.sleep(1)

        # Add cards to hand
        for i in range(2):
            self.add_card()

        for card in self.hand_list:
            time.sleep(0.5)
            self.hand_value = self.hand_value + card.value
            print(f"{card.rank} of {card.suit}")
        time.sleep(0.5)

        print(f"\nHand value: {self.hand_value}\n{self.dash_small}")

        self.dealer_draw()

        self.player_turn()

    def add_card(self):
        self.hand_list.append(self.card_list.pop(0))

        # Check if cut card drawn
        if self.hand_list[-1].rank == "Cut Card":
            self.shuffle_shoe(self.hand_list)

    def dealer_draw(self):

        print("Dealer's draw:\n")
        time.sleep(1)
        # Add cards to dealer's hand
        for i in range(2):
            self.dl_hand_list.append(self.card_list.pop(0))

            # Check if cut card drawn
            if self.dl_hand_list[i].rank == "Cut Card":
                self.shuffle_shoe(self.dl_hand_list)

        for card in self.dl_hand_list:
            self.dl_hand_value = self.dl_hand_value + card.value

        time.sleep(0.5)
        print(f"{self.dl_hand_list[0].rank} of {self.dl_hand_list[0].suit}")
        time.sleep(0.5)
        print("???")

        time.sleep(0.5)
        print(f"\nHand value: {self.dl_hand_list[0].value}+\n{self.dash_small}")
        time.sleep(0.5)

    def shuffle_shoe(self, player):

        player = player
        # reshuffle shoe
        print("\nCut card drawn! reshuffling shoe...\n")
        self.setup.new_shoe(shoe_size)

        # Find and replace cut card
        cc_index = (len(player) - 1)
        player.pop(cc_index)
        player.append(self.card_list.pop(0))

    def player_turn(self):

        print("Player's turn")
        while self.hand_value < 21:
            try:
                action = str(input("Hit or Stand? (h/s): ")).lower()
                if action == "h":
                    self.hit()
                elif action == "s":
                    self.stand()
                else:
                    print("please enter either h or s")
                    self.player_turn()
            except ValueError:
                print("Unexpected input received")

    def dealer_turn(self):
        print(f"{self.dash_small}\nDealer's turn")

        for card in self.dl_hand_list:
            print(f"{card.rank} of {card.suit}")

        while self.dl_hand_value < 17:
            time.sleep(0.5)

            self.dl_hand_list.append(self.card_list.pop(0))

    
            new_rank = self.dl_hand_list[-1].rank
            new_suit = self.dl_hand_list[-1].suit
            self.dl_hand_value = self.dl_hand_value + new_rank
            print(f"{new_rank} of {new_suit}")
            print(f"Hand value: {self.dl_hand_value}")



    def hit(self):

        # Add new card to hand
        self.hand_list.append(self.card_list.pop(0))

        # Find new card
        new_rank = self.hand_list[-1].rank
        new_suit = self.hand_list[-1].suit

        # Output
        self.hand_value = self.hand_value + self.hand_list[-1].value
        print(f"{new_rank} of {new_suit}")
        print(f"\nHand value: {self.hand_value}")

    def stand(self):
        self.dealer_turn()