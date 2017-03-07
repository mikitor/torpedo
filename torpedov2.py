z = [[0 for row in range(0,11)] for col in range(0,11)]
second_player = [[0 for row in range(0,11)] for col in range(0,11)]

i = 3
for i in range(11):
    z[i][0] = i
    i += 1

i = 1
for i in range(11):
    z[0][i] = i
    i += 1

def draw_table():
    print("_"*30)
    for row in z:
        for col in row:
            print("{}".format(col), end="|")
        print(end="\n")
    print("_"*30)

z[1][2] = "X"

first_carrier = [z[1][0],z[1][1],z[1][2]]
print(first_carrier)


draw_table()

print(z[0][2])

