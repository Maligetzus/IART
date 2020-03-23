from enum import Enum
from neutron_util import BoardTypes

class BoardConstants:
    def __init__(self, board_type):
        self.BOARD_TYPE = board_type
        self.TYLE_SIZE = 0
        self.PIECE_SIZE = 0
        self.BOARD_SIZE = 0
        self.BORDER_SIZE = 0
        self.PIECE_OFFSET = 0
        self.BEETWEEN_TYLE_SIZE = 0

class GestureDirection(Enum):
    MovXPos = 1
    MovXNeg = 2
    MovYPos = 3
    MovYNeg = 4
    MovXPosYPos = 5
    MovXPosYNeg = 6
    MovXNegYPos = 7
    MovXNegYNeg = 8
    PieceSelect = 9

class GuiStates(Enum):
    Waiting4Play = 1
    RegisteringPlay = 2
    ApplyingPlay = 3


def get_direction(mouse_movement, tyle_size):
    deltaX = mouse_movement[0]
    deltaY = mouse_movement[1]

    if abs(deltaX) > tyle_size/2 and abs(deltaY) > tyle_size/2: #Diagonal
        if deltaX > 0 and deltaY < 0:
            return GestureDirection.MovXPosYPos
        elif deltaX > 0 and deltaY > 0:
            return GestureDirection.MovXPosYNeg
        elif deltaX < 0 and deltaY > 0:
            return GestureDirection.MovXNegYNeg
        elif deltaX < 0 and deltaY < 0:
            return GestureDirection.MovXNegYPos
    elif abs(deltaX) > tyle_size/2: #Horizontal
        if deltaX > 0:
            return GestureDirection.MovXPos
        else:
            return GestureDirection.MovXNeg
    elif abs(deltaY) > tyle_size/2: #Vertical
        if deltaY > 0:
            return GestureDirection.MovYNeg
        else:
            return GestureDirection.MovYPos
    else:
        return GestureDirection.PieceSelect #Not enough movement to count as a direction


def is_between(coords, top_left_point, bot_right_point):
    if top_left_point[0] <= coords[0] <= bot_right_point[0] and top_left_point[1] <= coords[1] <= bot_right_point[1]:
        return True
    else:
        return False


def get_board_coords_from_screen_coords(board_constants, mouse_coords):
    if board_constants.BOARD_TYPE == BoardTypes.Board_5X5:
        board_side = 5
    else:
        board_side = 7

    if mouse_coords[0] <= board_constants.BORDER_SIZE or mouse_coords[1] <= board_constants.BORDER_SIZE:
        return (-1, -1)
    elif mouse_coords[0] >= board_constants.BOARD_SIZE+board_constants.BORDER_SIZE or mouse_coords[1] >= board_constants.BOARD_SIZE+board_constants.BORDER_SIZE:
        return (-1, -1)
    else:
        current_coords = (board_constants.BORDER_SIZE+board_constants.PIECE_OFFSET, board_constants.BORDER_SIZE+board_constants.PIECE_OFFSET)
        for line in range(0, board_side):  # Lines

            for column in range(0, board_side):  # Columns
                opposite_side = (current_coords[0] + board_constants.PIECE_SIZE, current_coords[1] + board_constants.PIECE_SIZE)
                if is_between(mouse_coords, current_coords, opposite_side):
                    return (column, line)

                current_coords = (current_coords[0] + board_constants.PIECE_SIZE + 2 * board_constants.PIECE_OFFSET + board_constants.BEETWEEN_TYLE_SIZE,
                                    current_coords[1])

            current_coords = (board_constants.BORDER_SIZE+board_constants.PIECE_OFFSET,
                              current_coords[1]+board_constants.PIECE_SIZE+2*board_constants.PIECE_OFFSET+board_constants.BEETWEEN_TYLE_SIZE)

        return (-1, -1)


def tile_has_a_piece(board, board_coords):
    if board[board_coords[1]][board_coords[0]] != 'E':
        return True
    else:
        return False