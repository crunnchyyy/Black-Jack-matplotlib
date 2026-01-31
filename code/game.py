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
        self.bet_chips = 0
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

        self.hand_list.clear()
        self.dl_hand_list.clear()
        self.hand_value = 0
        self.dl_hand_value = 0

        # Allow for initial bet
        self.bet()
        # Increment hand number and start hand
        self.hand_num += 1
        print(f"{self.dash}\nHand {self.hand_num}!\n{self.dash}")
        print("Player's draw:\n")
        time.sleep(1)

        # Add cards to hand
        for i in range(2):
            self.add_card(self.hand_list)

        # Reveal cards
        for card in self.hand_list:
            time.sleep(0.5)
            self.hand_value = self.hand_value + card.value
            print(f"{card.rank} of {card.suit}")
        time.sleep(0.5)

        # Reveal hand value
        print(f"\nHand value: {self.hand_value}\n{self.dash_small}")

        # Initial dealer draw
        self.dealer_draw()

        # Begin player turn
        self.player_turn()

    def bet(self):

        try:
            self.bet_chips = int(input(f"How many chips do you want to bet? (max {self.chips}): "))
            if self.bet_chips < 1:
                print("Please bet at least 1 chip")
            elif self.bet_chips <= self.chips:
                print(f"{self.bet_chips} wagered")
                return
            else:
                print(f"You do not have enough chips to bet {self.bet_chips} (max {self.chips})")

        # If input is not an integer
        except ValueError:
            print("Please input an integer")

        # If not returned, ask to bet again
        self.bet()


    def add_card(self, player):

        list = player
        # Draw card
        list.append(self.card_list.pop(0))

        # Check if cut card drawn
        if list[-1].rank == "Cut Card":
            self.shuffle_shoe(list)

    def dealer_draw(self):

        # Start dealer draw
        print("Dealer's draw:\n")
        time.sleep(1)

        # Add cards to dealer's hand
        for i in range(2):
            self.add_card(self.dl_hand_list)

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
        if self.hand_value == 21:
            self.chips = self.chips + int(self.bet_chips * dealer_pay_rate)
            print(f"You got 21!\nPayout: {int(self.bet_chips * dealer_pay_rate)}")
            print(f"Chips: {self.chips}")
            self.next_hand()
        elif self.hand_value > 21:
            self.chips = self.chips - self.bet_chips
            print(f"You busted")
            print(f"You lost {self.bet_chips} chips")
            print(f"Chips: {self.chips}")
            self.next_hand()

    def dealer_turn(self):
        print(f"{self.dash_small}\nDealer's turn")

        for card in self.dl_hand_list:
            print(f"{card.rank} of {card.suit}")

        # Reveal hand value
        print(f"\nHand value: {self.dl_hand_value}\n{self.dash_small}")

        while self.dl_hand_value < 17:
            time.sleep(0.5)

            self.dl_hand_list.append(self.card_list.pop(0))

            new_rank = self.dl_hand_list[-1].rank
            new_suit = self.dl_hand_list[-1].suit
            new_value = self.dl_hand_list[-1].value
            self.dl_hand_value = self.dl_hand_value + new_value
            print(f"{new_rank} of {new_suit}")
            print(f"Hand value: {self.dl_hand_value}")


        self.check_win()

    def check_win(self):

        if self.hand_value < 22:
            if self.hand_value > self.dl_hand_value:
                self.payout("Player")
        else:
            self.payout("Dealer")

    def payout(self, win):

        if win == "Player":
            self.chips = self.chips + (self.bet_chips * dealer_pay_rate)
            print("You win!")
            print(f"Payout: {int(self.bet_chips * dealer_pay_rate)}")
            print(f"Chips: {self.chips}\n")

        if win == "Dealer":
            self.chips = self.chips - self.bet_chips

        self.next_hand()

    def next_hand(self):

        try:
            play_again = str(input("Play another hand? (y/n): ")).lower()
            if play_again == "y":
                self.new_hand()
            elif play_again == "n":
                self.game_over()
            else:
                print("please enter either y or n")
                self.next_hand()
        except ValueError:
            print("Unexpected input received")




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

    def game_over(self):
        print("game over")
