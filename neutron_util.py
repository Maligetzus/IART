import enum


class Player(enum.Enum):
    White = "White"
    Black = "Black"


class Turn(enum.Enum):
    Neutron = "Neutron"
    Pawn = "Pawn"

def get_score(game):
    return 1000 + 10 * num_empty_tiles_player(game) - 10 * num_empty_tiles_opponent(game) +\
           200 * neutron_to_player(game) - 200 * neutron_to_opponent(game) + 10 * odd(game) *\
           (8 - num_empty_fields_around_neutron(game)) + 500 * victory_player(game.curr_player, game.state) - 500\
           * victory_opponent(game)

def num_empty_tiles_player(game):
    return __num_empty_tiles(game.curr_player, game.state)

def num_empty_tiles_opponent(game):
    return __num_empty_tiles(Player.White if game.curr_player == Player.Black else Player.Black, game.state)

def neutron_to_player(game):
    return __neutron_to(game.curr_player, game.state, game.neutron_position)

def neutron_to_opponent(game):
    return __neutron_to(Player.White if game.curr_player == Player.Black else Player.Black, game.state, game.neutron_position)

def num_empty_fields_around_neutron(game):
    counter = 0

    x, y = game.neutron_position
    
    left = True
    right = True
    up = True
    down = True

    if x == game.size - 1:
        down = False
    if x == 0:
        up = False
    if y == game.size - 1:
        right = False
    if y == 0:
        left = False

    state = game.state

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
    if num_empty_fields_around_neutron(game) % 2 == 0:
        return -1
    else:
        return 1


def victory_player(game):
    return victory(game.curr_player, game.state)


def victory_opponent(game):
    return victory(Player.White if game.curr_player == Player.Black else Player.Black, game.state)


def __num_empty_tiles(player, state):
    counter = 0
    if player == Player.Black:
        for tile in state[0]:
            if tile == '0':
                counter += 1
    else:
        for tile in state[len(state) - 1]:
            if tile == '0':
                counter += 1

    return counter


def __neutron_to(player, state, neutron_position):
    counter = 0

    neutron_x, neutron_y = neutron_position

    diff_x = -1
    diff_y = -1

    if player == Player.Black:
        diff_x = neutron_x
    else:
        diff_x = abs(len(state) - 1 - neutron_x)
    
    up = True
    diag_left = True if neutron_y >= diff_x else False
    diag_right = True if len(state[0]) - 1 - neutron_y >= diff_x else False

    for i in range(1, diff_x + 1):
        if up:
            if state[neutron_x - i if player == Player.Black else neutron_x + i][neutron_y] != "0":
                up = False
        
        if diag_left:
            if state[neutron_x - i if player == Player.Black else neutron_x + i][neutron_y - i] != "0":
                diag_left = False

        if diag_right:
            if state[neutron_x - i if player == Player.Black else neutron_x + i][neutron_y + i] != "0":
                diag_right = False
            
        if(not up and not diag_left and not diag_right):
            break

    if(up):
        counter += 1

    if(diag_left):
        counter += 1

    if(diag_right):
        counter += 1

    return counter


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
