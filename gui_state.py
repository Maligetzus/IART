from gui_utils import *
import pygame.mouse

class GuiState:
    def __init__(self, board_gui):
        self.board_gui = board_gui
        self.current_state = GuiStates.Waiting4Play
        self.selected_piece = (-1, -1) #To be used by the handlers

    def handle_mouse_up(self):
        if self.current_state == GuiStates.RegisteringPlay:
            gesture = pygame.mouse.get_rel()
            direction = get_direction(gesture, self.board_gui.constants.TYLE_SIZE)
            if direction == Direction.NotReallyADirection: #invalidate
                self.current_state = GuiStates.Waiting4Play
                self.selected_piece = (-1, -1)
            else:
                print(direction)
                self.board_gui.call_move(self.selected_piece, direction)
                self.current_state = GuiStates.Waiting4Play  # For testing purposes only
                self.selected_piece = (-1, -1)  # For testing purposes only

    def handle_mouse_down(self):
        if self.current_state == GuiStates.Waiting4Play:
            click_board_coords = get_board_coords_from_screen_coords(self.board_gui.constants, pygame.mouse.get_pos())
            if click_board_coords != (-1, -1) and tile_has_a_piece(self.board_gui.board, click_board_coords):
                pygame.mouse.get_rel()  #Starts registering gesture
                self.selected_piece = click_board_coords #Save "selected" piece
                print("Registered coords:", click_board_coords)
                self.current_state = GuiStates.RegisteringPlay #Update State
