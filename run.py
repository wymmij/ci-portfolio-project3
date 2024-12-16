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
