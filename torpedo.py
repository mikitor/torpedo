import string
import os


# creating the boards
def creating_boards():
    first_player_board = [[0 for row in range(0, 10)] for col in range(0, 10)]
    second_player_board = [[0 for row in range(0, 10)] for col in range(0, 10)]

    COORDINATE_LETTERS = [chr(i) for i in range(ord('A'), ord('I') + 1)]
    j = 0
    while j < len(COORDINATE_LETTERS):
        first_player_board[j + 1][0] = COORDINATE_LETTERS[j]
        second_player_board[j + 1][0] = COORDINATE_LETTERS[j]
        j += 1

    COORDINATE_NUMBERS = []
    i = 1
    for i in range(10):
        first_player_board[0][i] = i
        second_player_board[0][i] = i
        i += 1
        COORDINATE_NUMBERS.append(str(i))

    first_player_board[0][0] = " "
    second_player_board[0][0] = " "

    return first_player_board, second_player_board, COORDINATE_LETTERS, COORDINATE_NUMBERS


def storing_ships(COORDINATE_LETTERS, COORDINATE_NUMBERS):
    POSSIBLE_SHIPS = ["carrier", "battleship", "submarine", "destroyer"]
    POSSIBLE_DIRECTION = ["v", "h"]
    POSSIBLE_COORDINATES = [COORDINATE_LETTERS, COORDINATE_NUMBERS]
    SHIP_LENGTH = {"carrier": 5, "battleship": 4, "submarine": 3, "destroyer": 2}

    # storing coordinates of the ships
    first_carrier = []
    first_battleship = []
    first_submarine = []
    first_destroyer = []

    first_ships = [
        first_carrier,
        first_battleship,
        first_submarine,
        first_destroyer]

    second_carrier = []
    second_battleship = []
    second_submarine = []
    second_destroyer = []

    second_ships = [
        second_carrier,
        second_battleship,
        second_submarine,
        second_destroyer]
    return POSSIBLE_SHIPS, POSSIBLE_DIRECTION, POSSIBLE_COORDINATES, SHIP_LENGTH, first_ships, second_ships


# drawing the player's own board
def draw_own_table(board):
    print("_" * 20)
    for row in board:
        for col in row:
            print('\x1b[6;30;44m' + "{}".format(col), end="|" + '\x1b[0m')
        print(end="\n")


# drawing the enemy's board containing the fog of war
def draw_enemy_table(board):
    print("_" * 20)
    for row in range(10):
        for col in range(10):
            if "S" in str(board[int(row)][int(col)]):
                print('\x1b[6;30;44m' + "0", end="|" + '\x1b[0m')
            elif "M" in str(board[int(row)][int(col)]):
                print('\x1b[6;30;43m' + "{}".format("M"), end="|" + '\x1b[0m')
            else:
                print('\x1b[6;30;44m' + "{}".format(board[row][col]), end="|" + '\x1b[0m')
        print(end="\n")


# check whether the users coordinates make any sense
def value_check(board, ship_direction, i, x, y, POSSIBLE_SHIPS, SHIP_LENGTH):
    if "v" in ship_direction:
        for k in range(SHIP_LENGTH[POSSIBLE_SHIPS[i]]):
            if board[int(x) + k][int(y)] != 0:
                return False
            else:
                return True
    elif "h" in ship_direction:
        for k in range(SHIP_LENGTH[POSSIBLE_SHIPS[i]]):
            if board[int(x)][int(y) + k] != 0:
                return False
            else:
                return True


# check whether we can place the ship there
def ship_check(board, i, ship_direction, x, y, POSSIBLE_SHIPS, SHIP_LENGTH):
        def try_again():
            print("""
            You can not place your ship there!
                    """)
            return "again"
        if "v" == ship_direction:
            if POSSIBLE_SHIPS[i] in SHIP_LENGTH:
                k = 0
                if value_check(board, ship_direction, i, x, y, POSSIBLE_SHIPS, SHIP_LENGTH):
                    for k in range(SHIP_LENGTH[POSSIBLE_SHIPS[i]]):
                        board[int(x)][int(y)] = '\x1B[0;30;47m' + "S" + '\x1b[6;30;44m'
                        board[int(x) + k][int(y)] = '\x1B[0;30;47m' + "S" + '\x1b[6;30;44m'
                else:
                    try_again()
            else:
                try_again()
        elif "h" == ship_direction:
            if POSSIBLE_SHIPS[i] in SHIP_LENGTH:
                k = 0
                if value_check(board, ship_direction, i, x, y, POSSIBLE_SHIPS, SHIP_LENGTH):
                    for k in range(SHIP_LENGTH[POSSIBLE_SHIPS[i]]):
                        board[int(x)][int(y)] = '\x1B[0;30;47m' + "S" + '\x1b[6;30;44m'
                        board[int(x)][int(y) + k] = '\x1B[0;30;47m' + "S" + '\x1b[6;30;44m'
                else:
                    try_again()
            else:
                try_again()
        else:
            try_again()


def placement(user_ships, board, POSSIBLE_SHIPS, POSSIBLE_DIRECTION, SHIP_LENGTH, COORDINATE_LETTERS, COORDINATE_NUMBERS):
    i = 0
    while i < len(user_ships):
        print('Place your %s' % POSSIBLE_SHIPS[i])

        ship_direction = None
        while ship_direction not in POSSIBLE_DIRECTION:
            ship_direction = input("What direction do you want your %s to face(v or h):" % POSSIBLE_SHIPS[i])

        ship_coordinates = input("What should be the starting coordinate of your %s:" % POSSIBLE_SHIPS[i])

        x = [ship_coordinates.split('-', 1)[0]]
        if x[0] in COORDINATE_LETTERS:
            number = ord(x[0]) - 64
            x[0] = number
            x = "".join(str(e) for e in x)
        else:
            print("""
    You can not place your ship there!
                """)
            continue

        y = [ship_coordinates.split('-', 1)[1]]
        print(y[0])
        if y[0] in COORDINATE_NUMBERS:
            y = "".join(str(e) for e in y)
            if ship_check(board, i, ship_direction, x, y, POSSIBLE_SHIPS, SHIP_LENGTH) == "again":
                continue
            else:
                pass
        else:
            print("""
    You can not place your ship there!
                """)
            continue

        user_ships[i].append(ship_direction)
        user_ships[i].append(x)
        user_ships[i].append(y)
        os.system('clear')
        draw_own_table(board)
        i += 1


def hit(board, COORDINATE_NUMBERS, COORDINATE_LETTERS):
    while True:
        ship_coordinates = input("Where do you want to shoot (e.g. A-2)?")
        x = [ship_coordinates.split('-', 1)[0]]
        if x[0] in COORDINATE_LETTERS:
            number = ord(x[0]) - 64
            x[0] = number
            x = "".join(str(e) for e in x)
        else:
            print("""
        You can not shoot there!
            """)
            continue

        y = [ship_coordinates.split('-', 1)[1]]
        if y[0] in COORDINATE_NUMBERS:
            y = "".join(str(e) for e in y)
        else:
            print("""
        You can not shoot there!
            """)
            continue

        if "S" in str(board[int(x)][int(y)]):
            os.system('clear')
            print("You hit the enemy ship!")
            board[int(x)][int(y)] = '\x1B[0;30;41m' + "X" + '\x1b[6;30;44m'
            draw_enemy_table(board)
            print("You can shoot again!")
            hit(board, COORDINATE_NUMBERS, COORDINATE_LETTERS)
        else:
            print("You missed!")
            board[int(x)][int(y)] = '\x1B[0;30;43m' + "M" + '\x1b[6;30;44m'
            draw_enemy_table(board)


def check_win(board):
    for i in range(10):
        for j in range(10):
            if "S" in str(board[i][j]):
                return False
    return True


def main():
    first_player_board, second_player_board, COORDINATE_LETTERS, COORDINATE_NUMBERS = creating_boards()
    POSSIBLE_SHIPS, POSSIBLE_DIRECTION, POSSIBLE_COORDINATES, SHIP_LENGTH, first_ships, second_ships = storing_ships(COORDINATE_LETTERS,
                                                                                                                COORDINATE_NUMBERS)
    # placement phase
    print("Welcome to Our amazing TORpedo simulator, where you can check your battleship skills.")
    print("""First player

        """)
    placement(first_ships, first_player_board, POSSIBLE_SHIPS, POSSIBLE_DIRECTION, SHIP_LENGTH, COORDINATE_LETTERS, COORDINATE_NUMBERS)
    os.system('clear')
    print("""Second player

        """)
    placement(second_ships, second_player_board, POSSIBLE_SHIPS, POSSIBLE_DIRECTION, SHIP_LENGTH, COORDINATE_LETTERS, COORDINATE_NUMBERS)

    # battle phase
    os.system('clear')
    print("The battle commences NOW!")
    player_one = True
    while not check_win(second_player_board) and not check_win(first_player_board):
        if player_one:
            board = second_player_board
            print("First player's turn")
            draw_enemy_table(board)
            hit(board, COORDINATE_NUMBERS, COORDINATE_LETTERS)
            check_win(board)
            if check_win(board):
                print("First player WON!!!")
            player_one = False
            continue
        elif not player_one:
            board = first_player_board
            print("Second player's turn")
            draw_enemy_table(board)
            hit(board, COORDINATE_NUMBERS, COORDINATE_LETTERS)
            check_win(board)
            if check_win(board):
                print("Second player WON!!!")
            player_one = True
            continue


main()