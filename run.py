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
            ship_coords, exclusion_coords = ship.generate_ship_position(ship.size, vacant_fields, fleet_fields)
            excluded_fields += exclusion_coords
            fleet_fields += ship_coords
            for field in range(len(ship.fields)):
                ship.fields[field] = ship_coords[field]
            vacant_fields = [x for x in vacant_fields if x not in excluded_fields]
        return fleet_fields


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
