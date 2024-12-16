def print_rules():
    print("\nThe fleet consists of 10 ships:")
    print("  4 submarines  (1 field)")
    print("  3 destroyers  (2 fields)")
    print("  2 cruisers    (3 fields)")
    print("  1 battleship  (4 fields)")
    print("Ships cannot occupy contiguous fields.")
    print("The game is won by sinking the whole fleet")
    print("A ship is sunk by hitting all of its fields.")
    print("There are 5 difficulty levels, level 1 being the easiest.")
    print("At level 1 you start with 80 missiles, but for every higher level")
    print("  the arsenal reduces by 10 missiles.\n")


def play_game():
    pass


def new_session():
    """
    Begins a new session. Welcomes user, prompts for name, offers to display
    rules then starts the first game.
    """
    print("\nWelcome to Battleship.\n")

    player = input("Enter your name:\n> ")

    rules = input("Enter ? for the rules, otherwise any other key to continue:\n> ")
    if rules == "?":
        print_rules()

    play_game()


new_session()
