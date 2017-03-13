import string
import os

# creating the boards
f = [[0 for row in range(0,10)] for col in range(0,10)]
s = [[0 for row in range(0,10)] for col in range(0,10)]

abc = [chr(i) for i in range(ord('A'),ord('I')+1)]
j = 0
while j < len(abc):
    f[j+1][0] = abc[j]
    s[j+1][0] = abc[j]
    j += 1

num = []
i = 1
for i in range(10):
    f[0][i] = i
    s[0][i] = i
    i += 1
    num.append(str(i))

f[0][0] = " "
s[0][0] = " "

# possible options for user
possible_ships = ["carrier","battleship","submarine","destroyer"]
possible_direction = ["v","h"]
possible_coordinates = [abc,num]
length = {"carrier" : 5, "battleship" : 4, "submarine" : 3, "destroyer" : 2}

#storing coordinates of the ships
first_carrier = []
first_battleship = []
first_submarine = []
first_destroyer = []

first_ships = [first_carrier,first_battleship,first_submarine,first_destroyer]

second_carrier = []
second_battleship = []
second_submarine = []
second_destroyer = []

second_ships = [second_carrier,second_battleship,second_submarine,second_destroyer]

# function creating the board for the user
def draw_table(board):
    print("_"*20)
    for row in board:
        for col in row:
            print('\x1b[6;30;44m'+"{}".format(col), end="|" + '\x1b[0m')
        print(end="\n")

def draw_enemy_table(board):
    print("_"*20)
    for row in range(10):
        for col in range(10):
            if "S" in str(board[int(row)][int(col)]):
                print('\x1b[6;30;44m'+ "0", end="|" + '\x1b[0m')
            elif "M" in str(board[int(row)][int(col)]):
                print('\x1b[6;30;43m'+"{}".format("M"), end="|" + '\x1b[0m')
            else:
                print('\x1b[6;30;44m'+"{}".format(board[row][col]), end="|" + '\x1b[0m')
        print(end="\n")

def value_check(board,ship_direction,i,x,y):
    if "v" in ship_direction:
        for k in range(length[possible_ships[i]]):
            if board[int(x)+k][int(y)] != 0:
                return False
            else:
                return True
    elif "h" in ship_direction:
        for k in range(length[possible_ships[i]]):
            if board[int(x)][int(y)+k] != 0:
                return False
            else:
                return True

def ship_check(board,i,ship_direction,x,y):
    try:
        if "v" == ship_direction:
            if possible_ships[i] in length:
                k = 0
                if value_check(board,ship_direction,i,x,y) == True:
                    for k in range(length[possible_ships[i]]):
                        board[int(x)][int(y)] = '\x1B[0;30;47m' + "S" + '\x1B[0m'
                        board[int(x)+k][int(y)] = '\x1B[0;30;47m' + "S" + '\x1B[0m'
                        k += 1
                else:
                    print("""
        You can not place your ship there!
                        """)
                    return "again"
        elif "h" == ship_direction:
            if possible_ships[i] in length:
                k = 0
                if value_check(board,ship_direction,i,x,y) == True:
                    for k in range(length[possible_ships[i]]):
                        board[int(x)][int(y)] = '\x1B[0;30;47m' + "S" + '\x1B[0m'
                        board[int(x)][int(y)+k] = '\x1B[0;30;47m' + "S" + '\x1B[0m'
                        k += 1
                else:
                    print("""
        You can not place your ship there!
                """)
                    return "again"
    except:
        print("""
        You can not place your ship there!
                """)
        return "again"

def placement(user_ships,board):
    i = 0
    while i < len(user_ships):
        print('Place your %s' % possible_ships[i])

        ship_direction = None
        while ship_direction not in possible_direction:
            ship_direction = input("What direction do you want your %s to face(v or h):" % possible_ships[i])
        
        ship_coordinates = input("What should be the starting coordinate of your %s:" % possible_ships[i])

        try:
            x = [ship_coordinates.split('-', 1)[0]]
            for character in x:
                    number = ord(character) -64
                    x[0] = number
            x = "".join(str(e) for e in x)
            
            y = [ship_coordinates.split('-', 1)[1]]
            y = "".join(str(e) for e in y)
        except:
            print("""
        You can not place your ship there!
                """)
            continue
        if ship_check(board,i,ship_direction,x,y) == "again":
            continue
        else:
            pass

        user_ships[i].append(ship_direction)
        user_ships[i].append(x)
        user_ships[i].append(y)
        os.system('clear')
        draw_table(board)
        i += 1

def hit(board):
    try:
        ship_coordinates = input("Where do you want to shoot (e.g. A-2)?" )
        x = [ship_coordinates.split('-', 1)[0]]
        for character in x:
                number = ord(character) -64
                x[0] = number
        x = "".join(str(e) for e in x)

        y = [ship_coordinates.split('-', 1)[1]]
        y = "".join(str(e) for e in y)

        if "S" in board[int(x)][int(y)]:
            os.system('clear')
            print("You hit the enemy ship!")
            board[int(x)][int(y)] = '\x1B[0;30;41m' + "X" + '\x1B[0m'
            draw_enemy_table(board)
            print("You can shoot again!")
            hit(board)
    except:
        print("You missed!")
        board[int(x)][int(y)] = '\x1B[0;30;43m' + "M" + '\x1B[0m'
        draw_enemy_table(board)

def check_win(board):
	for i in range(10):
		for j in range(10):
			if "S" in str(board[i][j]):
				return False
	return True

def main():
    # placement phase
    print("Welcome to Our amazing TORpedo simulator, where you can check your battleship skills.")
    print("""First player
        
        """)
    placement(first_ships,f)
    os.system('clear')
    print("""Second player
        
        """)
    placement(second_ships,s)

    # battle phase
    os.system('clear')
    print("The battle commences NOW!")
    player_one = True
    while check_win(s) == False and check_win(f) == False:
        if player_one == True:
            board = s
            print("First player's turn")
            draw_enemy_table(board)
            hit(board)
            check_win(board)
            if check_win(board) == True:
                print("First player WON!!!")
            player_one = False
            continue
        elif player_one == False:
            board = f
            print("Second player's turn")
            draw_enemy_table(board)
            hit(board)
            check_win(board)
            if check_win(board) == True:
                print("Second player WON!!!")
            player_one = True
            continue
main()