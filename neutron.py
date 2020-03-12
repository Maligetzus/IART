def square_to_index(square):
    x = -1
    y = -1

    if(len(square) != 2):
        return x, y

    if square[0] == 'A' or square[0] == 'a':
        x = 0
    elif square[0] == 'B' or square[0] == 'b':
        x = 1
    elif square[0] == 'C' or square[0] == 'c':
        x = 2
    elif square[0] == 'D' or square[0] == 'd':
        x = 3
    elif square[0] == 'E' or square[0] == 'e':
        x = 4
    elif square[0] == 'F' or square[0] == 'f':
        x = 5
    elif square[0] == 'G' or square[0] == 'g':
        x = 6

    if square[1] == '1':
        y = 0
    elif square[1] == '2':
        y = 1
    elif square[1] == '3':
        y = 2
    elif square[1] == '4':
        y = 3
    elif square[1] == '5':
        y = 4
    elif square[1] == '6':
        y = 5
    elif square[1] == '7':
        y = 6

    return x, y

def play(state, player, step, move):
    squares = move.split(" ")

    if(len(squares) != 2):
        return False, state
        
    piece_x, piece_y = square_to_index(squares[0])
    square_x, square_y = square_to_index(squares[1])

    if(piece_x == -1 or piece_y == -1 or square_x == -1 or square_y == -1):
        return False, state
    
    if(step == 1 and state[piece_x][piece_y] != "N"):
        return False, state
    
    if(step == 2 and player == "White" and state[piece_x][piece_y] != "W"):
        return False, state

    if(step == 2 and player == "Black" and state[piece_x][piece_y] != "B"):
        return False, state

    if(state[square_x][square_y] != "0"):
        return False, state

    return move_piece(state, piece_x, piece_y, square_x, square_y)

    
def move_piece(state, piece_x, piece_y, square_x, square_y):
    diff_x = abs(square_x - piece_x)
    diff_y = abs(square_y - piece_y)

    aux_x = piece_x
    aux_y = piece_y

    if(diff_x == diff_y and diff_x != 0):
        forwards_x = True
        forwards_y = True

        if(square_x < piece_x):
            forwards_x = False

        if(square_y < piece_y):
            forwards_y = False

        if(forwards_x):
            if(forwards_y):
                if(square_x + 1 < len(state) and square_y + 1 < len(state) and state[square_x + 1][square_y + 1] == "0"):
                    return False, state
            else:
                if(square_x + 1 < len(state) and square_y - 1 >= 0 and state[square_x + 1][square_y - 1] == "0"):
                    return False, state
        else:
            if(forwards_y):
                if(square_x - 1 >= 0 and square_y + 1 < len(state) and state[square_x - 1][square_y + 1] == "0"):
                    return False, state
            else:
                if(square_x - 1 >= 0 and square_y - 1 >= 0 and state[square_x - 1][square_y - 1] == "0"):
                    return False, state

        while(aux_x != square_x and aux_y != square_y):
            if(forwards_x):
                aux_x += 1
            else:
                aux_x -= 1

            if(forwards_y):
                aux_y += 1
            else:
                aux_y -= 1

            if(state[aux_x][aux_y] != "0"):
                return False, state
    elif(diff_x == 0):
        forwards_y = True

        if(square_y < piece_y):
            forwards_y = False

        if(forwards_y):
            if(square_y + 1 < len(state) and state[square_x][square_y + 1] == "0"):
                return False, state
        else:
            if(square_y - 1 >= 0 and state[square_x][square_y - 1] == "0"):
                return False, state

        while(aux_y != square_y):
            if(forwards_y):
                aux_y += 1
            else:
                aux_y -= 1

            if(state[aux_x][aux_y] != "0"):
                return False, state
    elif(diff_y == 0):
        forwards_x = True

        if(square_x < piece_x):
            forwards_x = False

        if(forwards_x):
            if(square_x + 1 < len(state) and state[square_x + 1][square_y] == "0"):
                return False, state
        else:
            if(square_x - 1 >= 0 and state[square_x - 1][square_y] == "0"):
                return False, state

        while(aux_x != square_x):

            if(forwards_x):
                aux_x += 1
            else:
                aux_x -= 1

            if(state[aux_x][aux_y] != "0"):
                return False, state
    else:
        return False, state

    state[piece_x][piece_y], state[square_x][square_y] = state[square_x][square_y], state[piece_x][piece_y]

    return True, state 

def end_state(state):
    n_x = -1
    n_y = -1

    found = False

    for i in range(0, len(state)):
        for j in range(0, len(state[i])):
            if(state[i][j] == "N"):
                n_x = i
                n_y = j

                found = True
                break

        if(found):
            break

    if(n_x == 0):
        return True, "B"
    
    if(n_x == len(state) - 1):
        return True, "W"

    can_move = False

    for i in range(n_x - 1, n_x + 2):
        if(i >= 0 and i < len(state)):
            for j in range(n_y - 1, n_y + 2):
                if(j >= 0 and j < len(state[i])):
                    if(state[i][j] == "0"):
                        can_move = True
                        break
        
        if(can_move):
            break

    if(can_move):
        return False, None
    else:
        return True, None

def draw_board(state):
    length = len(state)

    print(" ", end=" ")
    
    for i in range(1, length + 1):
        print(i, end=" ")

    print("\n", end="")

    for i in range(0, length):
        print(chr(65 + i), end=" ")

        for j in range(0, len(state[i])):
            print(state[i][j], end=" ")

        print("\n", end="")

    print("\n", end="")

print("Size of board:\n1 - 5x5\n2 - 7x7")

size = 0
state = []

while(size != 1 and size != 2):
    size = int(input())
    print(size)

if(size == 1):
    state = [   ["B", "B", "B", "B", "B"],
                ["0", "0", "0", "0", "0"],
                ["0", "0", "N", "0", "0"],
                ["0", "0", "0", "0", "0"],
                ["W", "W", "W", "W", "W"]]
else:
    state = [   ["B", "B", "B", "B", "B", "B", "B"],
                ["0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "N", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0"],
                ["W", "W", "W", "W", "W", "W", "W"]]

winner = None
end = False
curr_player = "White"
step = 1

while(not end):
    if(step == 2):
        curr_player = "White" if curr_player != "White" else "Black"

        step = 1
    else:
        step = 2

    draw_board(state)
    print(curr_player + " Player,", end="")
    print(" play Neutron" if step == 1 else " play piece", end="")
    print(" (ex.: E1 B1):")
    
    success = False

    while(not success):

        move = input()

        success, new_state = play(state, curr_player, step, move)

        if(not success):
            print("Bad input!\n")
        else:
            state = new_state

    end, winner = end_state(state)

if(winner == None):
    winner = curr_player

print("Winner: " + curr_player)