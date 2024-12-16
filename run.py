from random import choice


class PlayingBoard:

    def __init__(self):
        self.fields = [
            (row, column) for row in range(10) for column in range(10)
        ]
        self.initial_board = """
         ________________________________________
        |                                        |
        | 00  01  02  03  04  05  06  07  08  09 |
        |                                        |
        | 10  11  12  13  14  15  16  17  18  19 |
        |                                        |
        | 20  21  22  23  24  25  26  27  28  29 |
        |                                        |
        | 30  31  32  33  34  35  36  37  38  39 |
        |                                        |
        | 40  41  42  43  44  45  46  47  48  49 |
        |                                        |
        | 50  51  52  53  54  55  56  57  58  59 |
        |                                        |
        | 60  61  62  63  64  65  66  67  68  69 |
        |                                        |
        | 70  71  72  73  74  75  76  77  78  79 |
        |                                        |
        | 80  81  82  83  84  85  86  87  88  89 |
        |                                        |
        | 90  91  92  93  94  95  96  97  98  99 |
        |________________________________________|
        """

    def populate_board(self, fleet):
        """
        Populate the playing board with the fleet of ships.
        Returns a list of fields occupied by the fleet.
        """
        vacant_fields = self.fields.copy()
        excluded_fields = []
        fleet_fields = []
        for ship in fleet:
            while True:
                try:
                    # if unpacking fails it's because return value isn't
                    # a tuple, which was a result of 'generate_ship_position()'
                    # generating a ship with invalid coordinates. See the
                    # function for further detail.
                    ship_coords, exclusion_coords = ship.generate_ship_position(
                        ship.size, vacant_fields, fleet_fields
                    )
                    break
                except TypeError:
                    pass

            excluded_fields += exclusion_coords
            fleet_fields += ship_coords
            for field in range(len(ship.fields)):
                ship.fields[field] = ship_coords[field]
            vacant_fields = [x for x in vacant_fields if x not in excluded_fields]
        return fleet_fields

    def update_board(self, hits, misses):
        """
        Update the board after each turn
        """
        updated = self.initial_board
        for field in hits:
            row, column = field
            updated = updated.replace(f" {row}{column} ", "<[]>")
        for field in misses:
            row, column = field
            updated = updated.replace(f" {row}{column} ", "~~~~")
        return updated
    

class Ship:

    def __init__(self, size):
        self.size = size
        self.fields = []
        match size:
            case 1:
                self.type = "submarine"
            case 2:
                self.type = "destroyer"
            case 3:
                self.type = "cruiser"
            case 4:
                self.type = "battleship"
        for i in range(size):
            self.fields.append(tuple())

    def generate_ship_position(self, size, vacant_fields, fleet_fields):
        row, column = choice(vacant_fields)
        adjusted_size = size - 1
        if choice(["latitude", "longitude"]) == "latitude":
            if choice(["north", "south"]) == "north":
                if is_valid_coordinate((row - adjusted_size, column)):
                    direction = "north"
                else:
                    direction = "south"
            else:
                if is_valid_coordinate((row + adjusted_size, column)):
                    direction = "south"
                else:
                    direction = "north"
        else:
            if choice(["east", "west"]) == "east":
                if is_valid_coordinate((row, column + adjusted_size)):
                    direction = "east"
                else:
                    direction = "west"
            else:
                if is_valid_coordinate((row, column - adjusted_size)):
                    direction = "west"
                else:
                    direction = "east"

        ship_coords = []
        for step in range(size):
            match direction:
                case "north":
                    ship_coords.append((row - step, column))
                case "south":
                    ship_coords.append((row + step, column))
                case "east":
                    ship_coords.append((row, column + step))
                case "west":
                    ship_coords.append((row, column - step))

        exclusion_coords = set()
        for ship in ship_coords:
            row, col = ship
            rows = generate_exclusion_digits(row)
            cols = generate_exclusion_digits(col)
            for r in rows:
                for c in cols:
                    exclusion_coords.add((r, c))

        if not exclusion_coords & set(fleet_fields):
            return (ship_coords, list(exclusion_coords))


class InputException(Exception):
    pass


def is_valid_coordinate(coord):
    row, column = coord
    if row >= 0 and row < 10 and column >= 0 and column < 10:
        return True
    else:
        return False


def generate_exclusion_digits(digit):
    digit_list = [digit]
    if digit > 0:
        digit_list.insert(0, digit - 1)
    if digit < 9:
        digit_list.append(digit + 1)
    return digit_list


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

    board = PlayingBoard()
    fleet = [
        Ship(4),
        Ship(3),
        Ship(3),
        Ship(2),
        Ship(2),
        Ship(2),
        Ship(1),
        Ship(1),
        Ship(1),
        Ship(1),
    ]

    fleet_fields = board.populate_board(fleet)

    shots = []
    hits = []
    misses = []
    missiles_launched = 0
    missiles_remaining = 0

    difficulty_levels = [level for level in range(1, 6)]
    print("There are 5 levels of difficulty, level 1 being the easiest.")
    while True:
        try:
            difficulty = int(
                input("Please enter the desired difficulty level (digit):\n> ")
            )
            if difficulty > 5 or difficulty < 1:
                raise InputException
            break
        except (ValueError, InputException):
            print("Please enter a digit between 1 and 5.")

    match difficulty:
        case 1:
            missiles_remaining = 80
        case 2:
            missiles_remaining = 70
        case 3:
            missiles_remaining = 60
        case 4:
            missiles_remaining = 50
        case 5:
            missiles_remaining = 40

    print(board.initial_board)

    while missiles_launched < missiles_remaining:
        while True:
            try:
                target = input("Enter the digits of the next target:\n> ")
                row, column = target
                target = (int(row), int(column))
                break
            except ValueError:
                print("Please enter a 2 digit number (0-9) only.")

        if target in shots:
            print("\nA waste! You've already fired at this target.")
        elif target in fleet_fields:
            print("\nHit!")
            hits.append(target)
            for ship in fleet:
                for field in ship.fields:
                    if (
                        target == field 
                        and all(field in hits for field in ship.fields)
                    ):
                        print(f"A {ship.type} has been sunk")

        else:
            print("\nMissed")
            misses.append(target)

        shots.append(target)
        missiles_launched += 1
        if (
            len(fleet_fields) == len(hits)
            or missiles_remaining == missiles_launched
            or missiles_remaining - missiles_launched < len(fleet_fields) - len(hits)
        ):
            break
        else:
            print(board.update_board(hits, misses))
            print("-" * 24)
            print(f"Direct hits:        {len(hits):2d}")
            print(f"Missiles launched:  {missiles_launched:2d}")
            print(f"Missiles remaining: {missiles_remaining - missiles_launched:2d}")
            print("-" * 24, "\n")

    if len(fleet_fields) == len(hits):
        print("\nYou win!!")
        print("You sunk the whole fleet!")
        games_won += 1
    elif missiles_remaining == missiles_launched:
        print("\nYou lose!!")
        print("You used all your missiles.")
        games_lost += 1
    elif missiles_remaining - missiles_launched < len(fleet_fields) - len(hits):
        print("\nYou lose!!")
        print("You don't have enough missiles to destroy the fleet.")
        games_lost += 1

    print(board.reveal_board(fleet_fields))
    print("-" * 24)
    print(f"Direct hits:        {len(hits):2d}")
    print(f"Missiles launched:  {missiles_launched:2d}")
    print(f"Missiles remaining: {missiles_remaining - missiles_launched:2d}")
    print("-" * 24, "\n")
    games_played += 1
    print(f"Games played: {games_played:2d}")
    print(f"Games won:    {games_won:2d}")
    print(f"Games lost:   {games_lost:2d}")

    another_game = input("\nPress Enter for another game (or q to quit):\n> ")
    if another_game == "q":
        print(f"Thanks for the game! Bye!")
    else:
        play_game(games_played, games_won, games_lost)


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
