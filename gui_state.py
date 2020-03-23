from gui_utils import *
import pygame.mouse

class GuiState:
    def __init__(self, board_gui):
        self.board_gui = board_gui
        self.current_state = GuiStates.Waiting4Play

    def handle_mouse_up(self):
        print("[Mouse button up]")
        if self.current_state == GuiStates.RegisteringPlay:
            gesture = pygame.mouse.get_rel()
            print(gesture)
            direction = get_direction(gesture, self.board_gui.constants.TYLE_SIZE)
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