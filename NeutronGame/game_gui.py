import pygame
import pathlib
from pygame import Surface
from pygame.locals import *
from NeutronGame.gui_utils import *
from NeutronGame.neutron_util import BoardTypes, Player, Turn, RenderMode
from NeutronGame.gui_state import *
from NeutronGame.neutron_util import Tile

class GameGui:
    def __init__(self, game, type, render_mode=RenderMode.Pygame):
        # Neutron class instance
        self.game = game
        self.board = game.state
        self.render_mode = render_mode
        if self.render_mode == RenderMode.Pygame:
            # Stores board gui related constants
            self.constants = BoardConstants(type)
            # Initializes pygame and game screen
            self.init_window()
            # Loads all the game resources
            self.load_resources()
            # Creates a black background to be, later applied to the screen
            self.load_background()
            # Stores the gui states; Handles events based on the current state
            self.state = GuiState(self)

    # Initializes pygame and game screen
    def init_window(self):
        # Initializes pygame
        pygame.init()
        # Initializes a 1250x800, not resizable window
        self.screen = pygame.display.set_mode((1250, 800), HWSURFACE | DOUBLEBUF)
        # Set window title
        pygame.display.set_caption("Neutron")
        self.animation_piece = None

    def load_resources(self):
        # Side Panel title font
        self.side_panel_font = pygame.font.SysFont(None, 50, False)
        # Side Panel sub-title font
        self.side_panel_font_smaller = pygame.font.SysFont(None, 40, False)

        # Load Pieces and Board
        self.red_piece_image = pygame.image.load(str(pathlib.Path(__file__).parent.absolute()) + '/resources/piece_red.png')
        self.blue_piece_image = pygame.image.load(str(pathlib.Path(__file__).parent.absolute()) + '/resources/piece_blue.png')
        self.neutron_piece_image = pygame.image.load(str(pathlib.Path(__file__).parent.absolute()) + '/resources/piece_neutron.png')
        self.game_board_tile = pygame.image.load(str(pathlib.Path(__file__).parent.absolute()) + '/resources/board_tile.png')

        # If the board is 7x7, down-scales resources to fit in the same space
        if (self.constants.BOARD_TYPE == BoardTypes.Board_7X7):
            self.scale_resources_for_7x7()

        # Calculates and registers board/piece/tiles dimensions and offsets
        self.register_constants()

    # Down-scales resources to fit in the same space as they would in a 5x5 board
    def scale_resources_for_7x7(self):
        piece_current_side = self.red_piece_image.get_width()
        piece_new_side = int(piece_current_side * 5 / 7)

        tile_side = self.game_board_tile.get_width()
        tile_new_side = int(tile_side * 5 / 7)

        self.red_piece_image = pygame.transform.scale(self.red_piece_image, (piece_new_side, piece_new_side))
        self.blue_piece_image = pygame.transform.scale(self.blue_piece_image, (piece_new_side, piece_new_side))
        self.neutron_piece_image = pygame.transform.scale(self.neutron_piece_image, (piece_new_side, piece_new_side))
        self.game_board_tile = pygame.transform.scale(self.game_board_tile, (tile_new_side, tile_new_side))

    # Calculates and registers board/piece/tiles dimensions and offsets
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

    # Creates a black background to be, later applied to the screen
    def load_background(self):
        # Create The Backgound
        self.background = pygame.Surface(self.screen.get_size())  # Creates a Surface with Size = Screen
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

    # Displays the helper menu / side panel on the screen
    def display_side_panel(self):
        # Creates side panel surface
        side_panel = Surface((425, 750))

        # Game mode indicator section
        # Writes "Game Mode" horizontally centered on the surface
        draw_text("Game Mode", self.side_panel_font, (255, 255, 255), side_panel, 0, 25, True, False)

        # Writes the game mode chosen, horizontally centered on the surface
        game_mode_text = self.game.player_type['White'].value + " vs " + self.game.player_type['Black'].value
        draw_text(game_mode_text, self.side_panel_font_smaller, (255, 255, 255), side_panel, 0, 75, True, False)

        # Turn indicator section
        draw_text("Turn", self.side_panel_font, (255, 255, 255), side_panel, 0, 175, True, False)
        if self.game.curr_player == Player.White:
            player_color = (209, 27, 94)  # Pink piece color
        else:
            player_color = (27, 209, 142)  # Green piece color
        # Writes the current player, with his color, and centers the text on the surface
        draw_text(self.game.player_type[self.game.curr_player.value].value, self.side_panel_font_smaller, player_color, side_panel, 0, 225, True, False)

        # To move section
        draw_text("To move", self.side_panel_font, (255, 255, 255), side_panel, 0, 325, True, False)
        if self.game.turn == Turn.Pawn:
            move_text = "Pawn"
        else:
            move_text = "Neutron"
        # Writes the piece to move, and centers the text on the surface
        draw_text(move_text, self.side_panel_font_smaller, (255, 255, 255), side_panel, 0, 375, True, False)

        # Calculates the coords where the side panel should be displayed on the screen
        side_panel_draw_x = 2*self.constants.BORDER_SIZE + self.constants.BOARD_SIZE
        side_panel_draw_y = self.constants.BORDER_SIZE
        self.screen.blit(side_panel, (side_panel_draw_x, side_panel_draw_y))

    # After the game ends, displays who won
    def display_winner(self, winner_type, winner):
        # Creates a surface of the same size as the screen, with transparency
        message_sur = Surface((1250, 800), pygame.SRCALPHA)
        # Makes the surface all black with 200 on alpha, to give the ilusion of a blur
        message_sur.fill((0, 0, 0, 200))
        # Displays the surface
        self.screen.blit(message_sur, (0, 0))
        draw_text("Winner", self.side_panel_font, (255, 255, 255), self.screen, 0, 300, True, False)
        if winner == Player.White:
            player_color = (209, 27, 94)  # Pink piece color
        else:
            player_color = (27, 209, 142)  # Green piece color
        # Draws the winner on the screen
        draw_text(winner_type.value, self.side_panel_font, player_color,
                  self.screen, 0, 350, True, False)

        # Draws help text on the bottom-corner of the screen
        draw_text("Press ESC to return to main menu", self.side_panel_font_smaller, (255, 255, 255),
                  self.screen, 760, 760, False, False)
        pygame.display.flip()

    # Returns the resource, based on the tile type
    def get_resource(self, tile):
        if tile == Tile.White:
            return self.red_piece_image
        elif tile == Tile.Black:
            return self.blue_piece_image
        elif tile == Tile.Neutron:
            return self.neutron_piece_image
        else:
            return None

    # Draws Everything
    def display(self):
        if self.render_mode == RenderMode.Ascii:
            self.game.draw_board()
            return

        # Puts the screen black
        self.screen.blit(self.background, (0, 0))
        # Displays side-panel
        self.display_side_panel()

        # Prints board
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

                curr_piece_image = self.get_resource(tile)
                if curr_piece_image != None:
                    self.screen.blit(curr_piece_image, current_piece_coords)

                curr_col_number += 1

            curr_col_number = 0
            curr_line_number += 1

        # Displays animation
        if self.animation_piece != None:
            self.screen.blit(self.animation_piece, self.animation_piece_coords)
            self.animation_piece = None

        # Display everything that was "placed" on the screen
        pygame.display.flip()

    def call_move(self, piece, direction):
        self.game.move_piece(piece[1], piece[0], direction)
