from enum import Enum
import pygame.mouse

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

class GuiState:
    def __init__(self, board_gui):
        self.board_gui = board_gui
        self.current_state = GuiStates.Waiting4Play

    def get_direction(self, mouse_movement):
        deltaX = mouse_movement[0]
        deltaY = mouse_movement[1]

        if abs(deltaX) > self.board_gui.TYLE_SIZE and abs(deltaY) > self.board_gui.TYLE_SIZE: #Diagonal
            if deltaX > 0 and deltaY < 0:
                return GestureDirection.MovXPosYPos
            elif deltaX > 0 and deltaY > 0:
                return GestureDirection.MovXPosYNeg
            elif deltaX < 0 and deltaY > 0:
                return GestureDirection.MovXNegYNeg
            elif deltaX < 0 and deltaY < 0:
                return GestureDirection.MovXNegYPos
        elif abs(deltaX) > self.board_gui.TYLE_SIZE: #Horizontal
            if deltaX > 0:
                return GestureDirection.MovXPos
            else:
                return GestureDirection.MovXNeg
        elif abs(deltaY) > self.board_gui.TYLE_SIZE: #Vertical
            if deltaY > 0:
                return GestureDirection.MovYNeg
            else:
                return GestureDirection.MovYPos
        else:
            return GestureDirection.PieceSelect #Not enough movement to count as a direction



    def handle_mouse_up(self):
        print("[Mouse button up]")

        if self.current_state == GuiStates.RegisteringPlay:
            gesture = pygame.mouse.get_rel()
            print(gesture)
            direction = self.get_direction(gesture)
            print(direction)
            self.current_state = GuiStates.Waiting4Play

        # pygame.mouse.get_rel()
        # click_board_coords = self.get_board_coords_from_screen_coords(pygame.mouse.get_pos())
        # if click_board_coords != (-1, -1) and self.tile_has_a_piece(click_board_coords):
        #     self.handle_piece_click(click_board_coords)

    def handle_mouse_down(self):
        print("[Mouse button down]")

        if self.current_state == GuiStates.Waiting4Play:
            pygame.mouse.get_rel() #Starts registering gesture
            self.current_state = GuiStates.RegisteringPlay