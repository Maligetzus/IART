from enum import Enum

class GuiStates(Enum):
    Waiting = 1
    Piece_Selected = 2
    Doing_Play = 3

class GuiState:
    def __init__(self, board_gui):
        self.current_state = GuiState.Waiting

