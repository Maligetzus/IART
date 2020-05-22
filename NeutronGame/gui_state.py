from NeutronGame.gui_utils import *
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame.mouse


class GuiState:
    def __init__(self, board_gui):
        self.board_gui = board_gui
        # Current Gui state
        self.current_state = GuiStates.Waiting4Play
        # After the 1st state - Waiting4Play - is passed, it stores the piece where the gesture started here
        self.selected_piece = (-1, -1)

    # Handles Mouse up event
    def handle_mouse_up(self):
        if self.current_state == GuiStates.RegisteringPlay:
            gesture = pygame.mouse.get_rel()
            direction = get_direction(gesture, self.board_gui.constants.TYLE_SIZE)

            if direction != None:  # Invalidate gesture
                self.board_gui.call_move(self.selected_piece, direction) # Calls Neutron's class move_piece method

            self.current_state = GuiStates.Waiting4Play # Resets current state
            self.selected_piece = (-1, -1) # Resets selected piece

    # Handles Mouse down event
    def handle_mouse_down(self):
        if self.current_state == GuiStates.Waiting4Play:
            click_board_coords = get_board_coords_from_screen_coords(self.board_gui.constants, pygame.mouse.get_pos())
            if click_board_coords != (-1, -1) and tile_has_a_piece(self.board_gui.board, click_board_coords):
                pygame.mouse.get_rel()  # Starts registering gesture
                self.selected_piece = click_board_coords # Saves "selected" piece
                self.current_state = GuiStates.RegisteringPlay # Updates State
