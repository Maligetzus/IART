import enum

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
    index = x * size + y

def get_list_of_lists_string_state():
    return [[TileString.Empty, TileString.Black, TileString.Empty, TileString.Empty, TileString.Black],
            [TileString.Empty, TileString.Empty, TileString.Empty, TileString.Empty, TileString.Empty],
            [TileString.Empty, TileString.Empty, TileString.Black, TileString.Black, TileString.White],
            [TileString.Empty, TileString.Empty, TileString.Black, TileString.Empty, TileString.Neutron],
            [TileString.Empty, TileString.White, TileString.White, TileString.White, TileString.White]]

def get_list_of_lists_int_state():
    return [[TileInt.Empty, TileInt.Black, TileInt.Empty, TileInt.Empty, TileInt.Black],
            [TileInt.Empty, TileInt.Empty, TileInt.Empty, TileInt.Empty, TileInt.Empty],
            [TileInt.Empty, TileInt.Empty, TileInt.Black, TileInt.Black, TileInt.White],
            [TileInt.Empty, TileInt.Empty, TileInt.Black, TileInt.Empty, TileInt.Neutron],
            [TileInt.Empty, TileInt.White, TileInt.White, TileInt.White, TileInt.White]]

def get_list_string_state():
    return [TileString.Empty, TileString.Black, TileString.Empty, TileString.Empty, TileString.Black,
            TileString.Empty, TileString.Empty, TileString.Empty, TileString.Empty, TileString.Empty,
            TileString.Empty, TileString.Empty, TileString.Black, TileString.Black, TileString.White,
            TileString.Empty, TileString.Empty, TileString.Black, TileString.Empty, TileString.Neutron,
            TileString.Empty, TileString.White, TileString.White, TileString.White, TileString.White]

def get_list_int_state():
    return [TileInt.Empty, TileInt.Black, TileInt.Empty, TileInt.Empty, TileInt.Black,
            TileInt.Empty, TileInt.Empty, TileInt.Empty, TileInt.Empty, TileInt.Empty,
            TileInt.Empty, TileInt.Empty, TileInt.Black, TileInt.Black, TileInt.White,
            TileInt.Empty, TileInt.Empty, TileInt.Black, TileInt.Empty, TileInt.Neutron,
            TileInt.Empty, TileInt.White, TileInt.White, TileInt.White, TileInt.White]