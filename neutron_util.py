import enum

class Player(enum.Enum):
    White = "White"
    Black = "Black"

class Turn(enum.Enum):
    Neutron = "Neutron"
    Pawn = "Pawn"

def get_neutron_position(state):
    x = -1
    y = -1

    # Gets the coordinates for the Neutron
    found = False

    for i in range(0, len(state)):
        for j in range(0, len(state[i])):
            if state[i][j] == "N":
                x = i
                y = j

                found = True
                break

        if found:
            break

    return x, y

def get_score(game):
    return 1000 + 10 * num_empty_tiles_player(game) - 10 * num_empty_tiles_opponent(game) +\
           200 * neutron_to_player(game) - 200 * neutron_to_opponent(game) + 10 * odd(game) *\
           (8 - num_empty_fields_around_neutron(game.state)) + 500 * victory_player(game.curr_player, game.state) - 500 * victory_opponent(game.curr_player, game.state)


def num_empty_tiles_player(game):
    return __num_empty_tiles(game.curr_player, game)


def num_empty_tiles_opponent(game):
    if game.curr_player == "Black":
        return __num_empty_tiles("White", game)
    elif game.curr_player == "White":
        return __num_empty_tiles("Black", game)


def neutron_to_player(game):
    return __neutron_to(game.curr_player, game)


def neutron_to_opponent(game):
    if game.curr_player == "Black":
        return __neutron_to("White", game)
    elif game.curr_player == "White":
        return __neutron_to("Black", game)


def num_empty_fields_around_neutron(state):
    counter = 0

    x, y = get_neutron_position(state)
    
    left = True
    right = True
    up = True
    down = True

    if(x == len(state) - 1):
        down = False
    if(x == 0):
        up = False
    if(y == len(state) - 1):
        right = False
    if(y == 0):
        left = False

    if left and up and state[x - 1][y - 1] == '0':
        counter += 1
    if up and state[x - 1][y] == '0':
        counter += 1
    if up and right and state[x - 1][y + 1] == '0':
        counter += 1
    if left and state[x][y - 1] == '0':
        counter += 1
    if right and state[x][y + 1] == '0':
        counter += 1
    if down and left and state[x + 1][y - 1] == '0':
        counter += 1
    if down and state[x + 1][y] == '0':
        counter += 1
    if down and right and state[x + 1][y + 1] == '0':
        counter += 1

    return counter


def odd(game):
    if(num_empty_fields_around_neutron(game) % 2 == 0):
        return -1
    else:
        return 1


def victory_player(curr_player, state):
    return victory(curr_player, state)


def victory_opponent(curr_player, state):
    if curr_player == Player.Black:
        return victory(Player.White, state)
    else:
        return victory(Player.Black, state)


def __num_empty_tiles(player, game):
    counter = 0
    if player == "Black":
        for tile in game.state[0]:
            if tile == '0':
                counter += 1
    elif player == "White":
        for tile in game.state[game.size - 1]:
            if tile == '0':
                counter += 1

    return counter

## TODO: have to fix this
def __neutron_to(player, game):
    if player == "Black":
        for tile in game.state[1]:
            if tile == 'N':
                return 1
    elif player == "White":
        for tile in game.state[game.size - 2]:
            if tile == 'N':
                return 1
    return 0


def victory(player, state):
    if player == Player.Black:
        for tile in state[0]:
            if tile == 'N':
                return 1
    elif player == Player.White:
        for tile in state[len(state) - 1]:
            if tile == 'N':
                return 1
    return 0
