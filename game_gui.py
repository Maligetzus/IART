import pygame
from pygame.locals import *
from gui_utils import *
from neutron_util import BoardTypes
import gui_state
from neutron_util import Tile


class GameGui:
    def __init__(self, board, type):
        self.board = board
        self.constants = BoardConstants(type)
        self.init_window()
        self.load_resources()
        self.load_background()
        self.state = gui_state.GuiState(self)

    def init_window(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800), HWSURFACE | DOUBLEBUF | RESIZABLE)
        pygame.display.set_caption("Neutron")

    def load_resources(self):
        # Load Pieces and Board
        self.red_piece_image = pygame.image.load('resources/piece_red.png')
        self.blue_piece_image = pygame.image.load('resources/piece_blue.png')
        self.game_board_tile = pygame.image.load('resources/board_tile.png')

        if (self.constants.BOARD_TYPE == BoardTypes.Board_7X7):
            self.scale_resources_for_7x7()

        self.register_constants()

    def scale_resources_for_7x7(self):
        piece_current_side = self.red_piece_image.get_width()
        piece_new_side = int(piece_current_side * 5 / 7)

        tile_side = self.game_board_tile.get_width()
        tile_new_side = int(tile_side * 5 / 7)

        self.red_piece_image = pygame.transform.scale(self.red_piece_image, (piece_new_side, piece_new_side))
        self.blue_piece_image = pygame.transform.scale(self.blue_piece_image, (piece_new_side, piece_new_side))
        self.game_board_tile = pygame.transform.scale(self.game_board_tile, (tile_new_side, tile_new_side))

    def register_constants(self):
        self.constants.TYLE_SIZE = self.game_board_tile.get_width()
        self.constants.PIECE_SIZE = self.red_piece_image.get_width()
        self.constants.BOARD_SIZE = 750
        self.constants.BORDER_SIZE = 25
        self.constants.PIECE_OFFSET = (self.constants.TYLE_SIZE - self.constants.PIECE_SIZE) / 2

        if self.constants.BOARD_TYPE == BoardTypes.Board_5X5:
            self.constants.BEETWEEN_TYLE_SIZE = (self.constants.BOARD_SIZE - 5 * self.constants.TYLE_SIZE) / 4
        elif self.constants.BOARD_TYPE == BoardTypes.Board_7X7:
            self.constants.BEETWEEN_TYLE_SIZE = (self.constants.BOARD_SIZE - 7 * self.constants.TYLE_SIZE) / 6

    def load_background(self):
        # Create The Backgound
        self.background = pygame.Surface(self.screen.get_size())  # Creates a Surface with Size = Screen
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

    # Draws Everything
    def display(self):
        # Background
        self.screen.blit(self.background, (0, 0))

        # Board
        curr_line_number = 0
        curr_col_number = 0

        for line in self.board:
            for tile in line:
                current_tile_coords = (self.constants.BORDER_SIZE + curr_col_number * self.constants.TYLE_SIZE
                                       + self.constants.BEETWEEN_TYLE_SIZE * curr_col_number,
                                       self.constants.BORDER_SIZE + curr_line_number * self.constants.TYLE_SIZE
                                       + self.constants.BEETWEEN_TYLE_SIZE * curr_line_number)

                self.screen.blit(self.game_board_tile, current_tile_coords)

                current_piece_coords = (self.constants.BORDER_SIZE + curr_col_number * self.constants.TYLE_SIZE
                                        + self.constants.BEETWEEN_TYLE_SIZE * curr_col_number + self.constants.PIECE_OFFSET,
                                        self.constants.BORDER_SIZE + curr_line_number * self.constants.TYLE_SIZE
                                        + self.constants.BEETWEEN_TYLE_SIZE * curr_line_number + self.constants.PIECE_OFFSET)

                if tile == Tile.White:
                    self.screen.blit(self.red_piece_image, current_piece_coords)
                elif tile == Tile.Black:
                    self.screen.blit(self.blue_piece_image, current_piece_coords)

                curr_col_number += 1

            curr_col_number = 0
            curr_line_number += 1

        pygame.display.flip()
