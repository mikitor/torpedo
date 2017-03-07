# drawing the boards
z = [[0 for row in range(0,10)] for col in range(0,10)]
second_player = [[0 for row in range(0,10)] for col in range(0,10)]

i = 1
for i in range(10):
    z[i][0] = i
    i += 1

i = 1
for i in range(10):
    z[0][i] = i
    i += 1

# function creating the board for the user
#still needs option to hide for the enemy table's ship position
def draw_table():
    print("_"*20)
    for row in z:
        for col in row:
            print("{}".format(col), end="|")
        print(end="\n")
    print("_"*20)

z[1][2] = "X"

#storing the coordinates of the ships
first_carrier = [z[1][0],z[1][1],z[1][2]]

#lenght of different ship types
carrier_len = 4
battleship = 3
submarine = 2
destroyer = 1

print(first_carrier)

draw_table()

print(z[0][2])

possible_ships = ["carrier","battleship","submarine","destroyer"]
possible_direction = ["v","h"]

#storing coordinates of the ships
first_carrier = []
first_battleship = []
first_submarine = []
first_destroyer = []

first_ships = [first_carrier,first_battleship,first_submarine,first_destroyer]

print("First players turn")
i = 0
while i < len(first_ships):
    ship = input("Give the starting coordinates, direction and type of your ship:")
    first_ships[i].append(ship)
    i += 1
