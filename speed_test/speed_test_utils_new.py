import enum


class Player(enum.Enum):
    White = "White"
    Black = "Black"


class Turn(enum.Enum):
    Neutron = "Neutron"
    Pawn = "Pawn"


class Direction(enum.Enum):
    Up = 0
    Down = 1
    Left = 2
    Right = 3
    LeftUp = 4
    RightUp = 5
    LeftDown = 6
    RightDown = 7


class Tile(enum.Enum):
    Empty = 'E'
    Black = 'B'
    White = 'W'
    Neutron = 'N'


def get_score(curr_player, state, size):
    return 1000 + 10 * num_empty_tiles_player(curr_player, state, size) - 10 * num_empty_tiles_opponent(curr_player, state, size) +\
           200 * neutron_to_player(curr_player, state, size) - 200 * neutron_to_opponent(curr_player, state, size) + 10 * odd(state) *\
           (8 - num_empty_fields_around_neutron(state)) + 500 * victory_player(curr_player, state, size) - 500\
           * victory_opponent(curr_player, state, size)


def num_empty_tiles_player(curr_player, state, size):
    return __num_empty_tiles(curr_player, state, size)


def num_empty_tiles_opponent(curr_player, state, size):
    return __num_empty_tiles(Player.White if curr_player == Player.Black else Player.Black, state, size)


def neutron_to_player(curr_player, state, size):
    return __neutron_to(curr_player, state, size)


def neutron_to_opponent(curr_player, state, size):
    return __neutron_to(Player.White if curr_player == Player.Black else Player.Black, state, size)


def num_empty_fields_around_neutron(state):
    counter = 0

    x, y = state[20], state[21]
    
    for i in range(0, 20, 2):
        if state[i] >= x - 1 and state[i] <= x + 1 and state[i + 1] >= y - 1 and state[i + 1] <= y + 1:
            counter += 1

    return counter


def odd(state):
    if num_empty_fields_around_neutron(state) % 2 == 0:
        return -1
    else:
        return 1


def victory_player(curr_player, state, size):
    return victory(curr_player, state, size)


def victory_opponent(curr_player, state, size):
    return victory(Player.White if curr_player == Player.Black else Player.Black, state, size)


def __num_empty_tiles(player, state, size):
    counter = 0
    if player == Player.Black:
        for i in range(0, 22, 2):
            if i == 0:
                counter += 1
    else:
        for i in range(0, 22, 2):
            if i == size - 1:
                counter += 1

    return counter


def __neutron_to(player, state, size):
    counter = 0

    neutron_x, neutron_y = state[20], state[21]

    diff_x = -1
    diff_y = -1

    if player == Player.Black:
        diff_x = neutron_x
    else:
        diff_x = abs(size - 1 - neutron_x)
    
    up = True
    diag_left = True if neutron_y >= diff_x else False
    diag_right = True if size - 1 - neutron_y >= diff_x else False

    for i in range(1, 20, 2):
        if up:
            if state[i + 1] == neutron_y and (not player == Player.Black or state[i] < neutron_x) and (not player == Player.White or state[i] > neutron_x):
                up = False
        
        if diag_left:
            if state[i + 1] < neutron_y and (not player == Player.Black or (state[i] == neutron_x - abs(neutron_y - state[i + 1]))) \
                and (not player == Player.White or (state[i] == neutron_x + abs(neutron_y - state[i + 1]))):
                diag_left = False

        if diag_right:
            if state[i + 1] > neutron_y and (not player == Player.Black or (state[i] == neutron_x - abs(neutron_y - state[i + 1]))) \
                and (not player == Player.White or (state[i] == neutron_x + abs(neutron_y - state[i + 1]))):
                diag_right = False
            
        if not up and not diag_left and not diag_right:
            break

    if up:
        counter += 1

    if diag_left:
        counter += 1

    if diag_right:
        counter += 1

    return counter


def victory(player, state, size):
    if player == Player.Black and state[21] == 0:
        return 1
    elif player == Player.White and state[21] == size - 1:
        return 1

    return 0
