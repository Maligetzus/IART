import pygame
from pygame.locals import *
from enum import Enum

class BoardType(Enum):
    Board_5X5 = 1
    Board_7X7 = 2

class BoardGUI:

    def __init__(self, board, type):
        self.board = board
        self.board_type = type
        self.calculate_sizes()
        self.init_window()
        self.load_resources()
        self.load_background()

    def calculate_sizes(self):
        self.BOARD_SIZE = 750
        self.BORDER_SIZE = 25
        if self.board_type == BoardType.Board_5X5:
            self.BEETWEEN_TYLE_SIZE = 15
            self.TYLE_SIZE = (self.BOARD_SIZE - 4*self.BEETWEEN_TYLE_SIZE) / 5
            self.PIECE_SIZE = self.TYLE_SIZE - 38

        self.PIECE_OFFSET = (self.TYLE_SIZE - self.PIECE_SIZE)/2




    def init_window(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800), HWSURFACE|DOUBLEBUF|RESIZABLE)
        pygame.display.set_caption("Neutron")

    def load_resources(self):
        # Load Pieces and Board
        self.red_piece_image = pygame.image.load('resources/piece_red.png')
        self.blue_piece_image = pygame.image.load('resources/piece_blue.png')
        self.game_board_tile = pygame.image.load('resources/board_tile.png')

    def load_background(self):
        # Create The Backgound
        self.background = pygame.Surface(self.screen.get_size())  # Creates a Surface with Size = Screen
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))


    # Draws Everything
    def display(self):

        #Background
        self.screen.blit(self.background, (0, 0))

        #Board
        curr_line_number = 0
        curr_col_number = 0

        for line in self.board:
            for tile in line:
                current_tile_coords = (self.BORDER_SIZE + curr_col_number*self.TYLE_SIZE
                                       + self.BEETWEEN_TYLE_SIZE * curr_col_number,
                                       self.BORDER_SIZE + curr_line_number*self.TYLE_SIZE
                                       + self.BEETWEEN_TYLE_SIZE * curr_line_number)

                self.screen.blit(self.game_board_tile, current_tile_coords)

                current_piece_coords = (self.BORDER_SIZE + curr_col_number * self.TYLE_SIZE
                                        + self.BEETWEEN_TYLE_SIZE * curr_col_number + self.PIECE_OFFSET,
                                        self.BORDER_SIZE + curr_line_number * self.TYLE_SIZE
                                        + self.BEETWEEN_TYLE_SIZE * curr_line_number + self.PIECE_OFFSET)
                if tile == 'R':
                    self.screen.blit(self.red_piece_image, current_piece_coords)
                elif tile == 'B':
                    self.screen.blit(self.blue_piece_image, current_piece_coords)

                curr_col_number += 1

            curr_col_number = 0
            curr_line_number += 1



        self.screen.blit(self.game_board_tile, (25, 25))

        pygame.display.flip()


    def game_loop(self):
        ## Display The Background
        #self.screen.blit(self.background, (0, 0))
        #pygame.display.flip()

        # Prepare Game Objects
        clock = pygame.time.Clock()

        # Main Loop
        going = True
        while going:
            clock.tick(60)

            # Handle Input Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    going = False
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    going = False
                elif event.type == MOUSEBUTTONDOWN:
                    print("Mouse button Pressed at: ", pygame.mouse.get_pos())
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    print("ESPACOOOOOOOOOOOOOO")
                # elif event.type == MOUSEMOTION:
                # print("Mouse Movement")
            self.display()


        pygame.quit()