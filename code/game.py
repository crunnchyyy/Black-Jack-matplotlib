import time
from settings import *
import setup
from matplotlib import pyplot as plt


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

        # Graph data
        self.chips_data = [self.chips]
        self.hands_data = [0]

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

    def clear_data(self):
        # Clear data
        self.hand_list.clear()
        self.dl_hand_list.clear()
        self.hand_value = 0
        self.dl_hand_value = 0

    def new_hand(self):

        self.clear_data()

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

        # Reveal cards in hand
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

    def bet(self):

        try:
            self.bet_chips = int(input(f"How many chips do you want to bet? (max {int(self.chips)}): "))
            if self.bet_chips < 1:
                print("Please bet at least 1 chip\n")
            elif self.bet_chips == 1 and self.chips >= 1:
                print(f"only {self.bet_chips} chip wagered? okay then")
                return
            elif self.bet_chips <= self.chips:
                print(f"{self.bet_chips} chips wagered\n")
                return
            else:
                print(f"You do not have enough chips to bet {self.bet_chips} (max {self.chips}\n)")

        # If input is not an integer
        except ValueError:
            print("Please input an integer")

        # If not returned, ask to bet again
        self.bet()


    def add_card(self, player):

        data = player
        # Draw card
        data.append(self.card_list.pop(0))

        # Check if cut card drawn
        if data[-1].rank == "Cut Card":
            self.shuffle_shoe(data)

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

        if self.hand_value == 21 and len(self.hand_list) == 2:
            self.payout("Blackjack")


        while self.hand_value < 21:
            time.sleep(0.5)
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
                self.player_turn()

        if self.hand_value == 21:
            self.dealer_turn()

        # Check if there are any aces
        if self.hand_value > 21:
            for card in self.hand_list:
                if card.rank == "Ace":
                    self.hand_value = self.hand_value - 10
                    card.rank = "Ace(1)"
                    print("\nAce counted as 1")
                    print(f"Hand value: {self.hand_value}")
                    self.player_turn()
        if self.hand_value > 21:
            self.check_win()

    def dealer_turn(self):
        print(f"{self.dash_small}\nDealer's turn")

        for card in self.dl_hand_list:
            time.sleep(0.5)
            print(f"{card.rank} of {card.suit}")

        # Reveal hand value
        time.sleep(0.5)
        print(f"\nHand value: {self.dl_hand_value}\n{self.dash_small}")

        while self.dl_hand_value < 17:
            time.sleep(0.5)

            self.add_card(self.dl_hand_list)

            new_rank = self.dl_hand_list[-1].rank
            new_suit = self.dl_hand_list[-1].suit
            new_value = self.dl_hand_list[-1].value
            self.dl_hand_value = self.dl_hand_value + new_value

            time.sleep(0.5)
            print(f"{new_rank} of {new_suit}")
            time.sleep(0.5)
            print(f"Hand value: {self.dl_hand_value}")

        # If dealer busts
        if self.dl_hand_value > 21:
            print("\n\n")
            for card in self.dl_hand_list:
                time.sleep(0.5)
                # Check for aces
                if card.rank == "Ace":
                    # Count aces as 1 if applicable
                    self.dl_hand_value = self.dl_hand_value - 10
                    card.rank = "Ace(1)"
                    print("\nAces counted as 1")
                    print(f"Hand value: {self.dl_hand_value}")
                print(f"{card.rank} of {card.suit}")
            time.sleep(0.5)
            print(f"Hand value: {self.dl_hand_value}")
            if self.dl_hand_value > 21:
                time.sleep(0.5)
                print(f"\nDealer busted")

        self.check_win()

    def check_win(self):

        # Output results in easily readable format
        print(f"{self.dash}\nRESULTS\n{self.dash}\n")
        print(f"Player hand: {self.hand_value}")
        print(f"Dealer hand: {self.dl_hand_value}")

        # Check if both hands are valid
        if self.dl_hand_value < 22 and self.hand_value < 22:

                # If player hand has higher number
                if self.hand_value > self.dl_hand_value:
                    self.payout("Player")
                # If player and dealer have same number
                elif self.hand_value == self.dl_hand_value:
                    self.payout("Push")
                # If dealer has higher number
                elif self.hand_value < self.dl_hand_value:
                    self.payout("Dealer")

        # Check if player or dealer busted
        elif self.hand_value > 21:
            self.payout("Dealer")
        elif self.dl_hand_value > 21:
            self.payout("Player")


    def payout(self, win):

        time.sleep(1)

        if win == "Blackjack":
            self.chips = self.chips + (int(self.bet_chips * dealer_pay_rate))
            print("You got a blackjack!")
            time.sleep(1)
            print(f"Payout: {int(self.bet_chips * dealer_pay_rate)}")
            print(f"Chips: {int(self.chips)}\n")

        if win == "Player":
            self.chips = self.chips + (int(self.bet_chips * dealer_pay_rate))
            print("You win!")
            time.sleep(1)
            print(f"Payout: {int(self.bet_chips * dealer_pay_rate)}")
            print(f"Chips: {int(self.chips)}\n")

        if win == "Draw":
            print("Draw!")
            time.sleep(1)
            print("No chips exchanged")
            print(f"Chips: {int(self.chips)}\n")

        if win == "Dealer":
            self.chips = self.chips - self.bet_chips
            print("You lose!")
            time.sleep(1)
            print(f"Loss: {self.bet_chips}")
            print(f"Chips: {int(self.chips)}\n")

        # add data to lists
        self.chips_data.append(int(self.chips))
        self.hands_data.append(int(self.hand_num))
        self.next_hand()

    def next_hand(self):

        if self.chips >= 1:
            try:
                play_again = str(input("Play another hand? (y/n): ")).lower()
                if play_again == "y":
                    self.new_hand()
                if play_again == "n":
                    self.game_over()
                else:
                    print("please enter either y or n")
                    self.next_hand()
            except ValueError:
                print("Unexpected input received")
                self.game_over()
                self.next_hand()
        if self.chips < 1:
            print("Out of chips")
            self.game_over()

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

        print("Making graph...")

        # Plot chart using hand and chips data
        plt.plot(self.hands_data, self.chips_data)

        # Give chart a title
        plt.title("Chips over rounds")

        # Label axis
        plt.xlabel("Rounds")
        plt.ylabel("Chips")

        # Ensure X axis only shows round numbers as integers
        plt.xticks(range(1,len(self.hands_data)))

        # Open window
        plt.show()
