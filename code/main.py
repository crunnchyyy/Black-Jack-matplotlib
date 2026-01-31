from game import Game

class Main:
    def __init__(self):

        # Setup new game
        self.instance = Game().run()

# Ensure instance can only be made from this file
if __name__ == "__main__":
    # Create main class instance
    instance = Main()