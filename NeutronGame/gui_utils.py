from enum import Enum
from NeutronGame.neutron_util import BoardTypes, Tile, Direction

# Used in game_gui to store board display constants
class BoardConstants:
    def __init__(self, board_type):
        self.BOARD_TYPE = board_type
        self.TYLE_SIZE = 0
        self.PIECE_SIZE = 0
        self.BOARD_SIZE = 0
        self.BORDER_SIZE = 0
        self.PIECE_OFFSET = 0
        self.BEETWEEN_TYLE_SIZE = 0


# Player move gesture states
class GuiStates(Enum):
    Waiting4Play = 1
    RegisteringPlay = 2
    ApplyingPlay = 3


# Calculates, based on a delta on mouse movement and the tile_size, the gesture direction the player made and returns it
def get_direction(mouse_movement, tile_size):
    deltaX = mouse_movement[0]
    deltaY = mouse_movement[1]

    if abs(deltaX) > tile_size/2 and abs(deltaY) > tile_size/2: #Diagonal
        if deltaX > 0 and deltaY < 0:
            return Direction.RightUp
        elif deltaX > 0 and deltaY > 0:
            return Direction.RightDown
        elif deltaX < 0 and deltaY > 0:
            return Direction.LeftDown
        elif deltaX < 0 and deltaY < 0:
            return Direction.LeftUp
    elif abs(deltaX) > tile_size/2: #Horizontal
        if deltaX > 0:
            return Direction.Right
        else:
            return Direction.Left
    elif abs(deltaY) > tile_size/2: #Vertical
        if deltaY > 0:
            return Direction.Down
        else:
            return Direction.Up
    else:
        return None #Not enough movement to count as a direction


# Aux funtion used to check if a click happened inside a rectangle
def is_between(coords, top_left_point, bot_right_point):
    if top_left_point[0] <= coords[0] <= bot_right_point[0] and top_left_point[1] <= coords[1] <= bot_right_point[1]:
        return True
    else:
        return False


# Converts screen coords into board coordinates
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


# Returns piece top-left corner coordinate, given board coordinates
def get_piece_coords_from_board_coords(board_constants, piece_coords):
    return (board_constants.BORDER_SIZE + board_constants.PIECE_OFFSET + piece_coords[0]*(board_constants.TYLE_SIZE + board_constants.BEETWEEN_TYLE_SIZE),
            board_constants.BORDER_SIZE + board_constants.PIECE_OFFSET +  piece_coords[1]*(board_constants.TYLE_SIZE + board_constants.BEETWEEN_TYLE_SIZE))


# Returns true if the given board tile has a piece on top
def tile_has_a_piece(board, board_coords):
    if board[board_coords[1]][board_coords[0]] != Tile.Empty:
        return True
    else:
        return False

# Draws text, using given font and color, onto a surface
def draw_text(text, font, color, surface, x, y, center_text_x=False, center_text_y=False):
    textobj = font.render(text, 1, color)

    if center_text_x and center_text_y:
        textrect = textobj.get_rect(center=(surface.get_width() / 2, surface.get_height() / 2))
    elif center_text_x:
        textrect = textobj.get_rect(center=(surface.get_width() / 2, y))
    elif center_text_y:
        textrect = textobj.get_rect(center=(x, surface.get_height() / 2))
    else:
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)

    surface.blit(textobj, textrect)