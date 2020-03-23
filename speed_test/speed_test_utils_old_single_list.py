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


class TileString(enum.Enum):
    Empty = 'E'
    Black = 'B'
    White = 'W'
    Neutron = 'N'

class TileInt(enum.Enum):
    Empty = 0
    Black = 2
    White = 1
    Neutron = 3

def get_state_list_element(x, y, size):
    return x * size + y

def get_score(curr_player, state, neutron_position, size):
    return 1000 + 10 * num_empty_tiles_player(curr_player, state, size) - 10 * num_empty_tiles_opponent(curr_player, state, size) +\
           200 * neutron_to_player(curr_player, state, neutron_position, size) - 200 * neutron_to_opponent(curr_player, state, neutron_position, size) + 10 * odd(state, neutron_position, size) *\
           (8 - num_empty_fields_around_neutron(state, neutron_position, size)) + 500 * victory_player(curr_player, state, size) - 500\
           * victory_opponent(curr_player, state, size)


def num_empty_tiles_player(curr_player, state, size):
    return __num_empty_tiles(curr_player, state, size)


def num_empty_tiles_opponent(curr_player, state, size):
    return __num_empty_tiles(Player.White if curr_player == Player.Black else Player.Black, state, size)


def neutron_to_player(curr_player, state, neutron_position, size):
    return __neutron_to(curr_player, state, neutron_position, size)


def neutron_to_opponent(curr_player, state, neutron_position, size):
    return __neutron_to(Player.White if curr_player == Player.Black else Player.Black, state, neutron_position, size)


def num_empty_fields_around_neutron(state, neutron_position, size):
    counter = 0

    x, y = neutron_position
    
    left = True
    right = True
    up = True
    down = True

    if x == size - 1:
        down = False
    if x == 0:
        up = False
    if y == size - 1:
        right = False
    if y == 0:
        left = False

    if left and up and (state[get_state_list_element(x - 1, y - 1, size)] == TileString.Empty or state[get_state_list_element(x - 1, y - 1, size)] == TileInt.Empty):
        counter += 1
    if up and (state[get_state_list_element(x - 1, y, size)] == TileString.Empty or state[get_state_list_element(x - 1, y, size)] == TileInt.Empty):
        counter += 1
    if up and right and (state[get_state_list_element(x - 1, y + 1, size)] == TileString.Empty or state[get_state_list_element(x - 1, y + 1, size)] == TileInt.Empty):
        counter += 1
    if left and (state[get_state_list_element(x, y - 1, size)] == TileString.Empty or state[get_state_list_element(x, y - 1, size)] == TileInt.Empty):
        counter += 1
    if right and (state[get_state_list_element(x, y + 1, size)] == TileString.Empty or state[get_state_list_element(x, y + 1, size)] == TileInt.Empty):
        counter += 1
    if down and left and (state[get_state_list_element(x + 1, y - 1, size)] == TileString.Empty or state[get_state_list_element(x + 1, y - 1, size)] == TileInt.Empty):
        counter += 1
    if down and (state[get_state_list_element(x + 1, y, size)] == TileString.Empty or state[get_state_list_element(x + 1, y, size)] == TileInt.Empty):
        counter += 1
    if down and right and (state[get_state_list_element(x + 1, y + 1, size)] == TileString.Empty or state[get_state_list_element(x + 1, y + 1, size)] == TileInt.Empty):
        counter += 1

    return counter


def odd(state, neutron_position, size):
    if num_empty_fields_around_neutron(state, neutron_position, size) % 2 == 0:
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
        for i in range(0, size - 1):
            if state[i] == TileString.Empty or state[i] == TileInt.Empty:
                counter += 1
    else:
        for i in range(get_state_list_element(size - 1, 0, size), get_state_list_element(size - 1, size - 1, size)):
            if state[i] == TileString.Empty or state[i] == TileInt.Empty:
                counter += 1

    return counter


def __neutron_to(player, state, neutron_position, size):
    counter = 0

    neutron_x, neutron_y = neutron_position

    diff_x = -1
    diff_y = -1

    if player == Player.Black:
        diff_x = neutron_x
    else:
        diff_x = abs(size - 1 - neutron_x)
    
    up = True
    diag_left = True if neutron_y >= diff_x else False
    diag_right = True if size - 1 - neutron_y >= diff_x else False

    for i in range(1, diff_x + 1):
        if up:
            if (state[get_state_list_element(neutron_x - i if player == Player.Black else neutron_x + i, neutron_y, size)] != TileString.Empty
                or state[get_state_list_element(neutron_x - i if player == Player.Black else neutron_x + i, neutron_y, size)] != TileInt.Empty):
                up = False
        
        if diag_left:
            if (state[get_state_list_element(neutron_x - i if player == Player.Black else neutron_x + i, neutron_y - i, size)] != TileString.Empty
                or state[get_state_list_element(neutron_x - i if player == Player.Black else neutron_x + i, neutron_y - i, size)] != TileInt.Empty):
                diag_left = False

        if diag_right:
            if (state[get_state_list_element(neutron_x - i if player == Player.Black else neutron_x + i, neutron_y + i, size)] != TileString.Empty
                or state[get_state_list_element(neutron_x - i if player == Player.Black else neutron_x + i, neutron_y + i, size)] != TileInt.Empty):
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
    if player == Player.Black:
        for i in range(0, size - 1):
            if state[i] == TileString.Neutron or state[i] == TileInt.Neutron:
                return 1
    elif player == Player.White:
        for i in range(get_state_list_element(size - 1, 0, size), get_state_list_element(size - 1, size - 1, size)):
            if state[i] == TileString.Neutron or state[i] == TileInt.Neutron:
                return 1
    return 0
