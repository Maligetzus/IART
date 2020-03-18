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
        self.init_window()
        self.load_resources()
        self.load_background()

    def init_window(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800), HWSURFACE|DOUBLEBUF|RESIZABLE)
        pygame.display.set_caption("Neutron")

    def load_resources(self):
        # Load Pieces and Board
        self.red_piece_image = pygame.image.load('resources/piece_red.png')
        self.blue_piece_image = pygame.image.load('resources/piece_blue.png')
        self.game_board_tile = pygame.image.load('resources/board_tile.png')

        if (self.board_type == BoardType.Board_7X7):
            self.scale_resources_for_7x7()

        self.register_resources_dimensions()
        self.register_spacing()


    def register_resources_dimensions(self):
        # Sizes
        self.TYLE_SIZE = self.game_board_tile.get_width()
        self.PIECE_SIZE = self.red_piece_image.get_width()


    def scale_resources_for_7x7(self):
        piece_current_side = self.red_piece_image.get_width()
        piece_new_side = int(piece_current_side*5/7)

        tile_side = self.game_board_tile.get_width()
        tile_new_side = int(tile_side*5/7)

        self.red_piece_image = pygame.transform.scale(self.red_piece_image, (piece_new_side, piece_new_side))
        self.blue_piece_image = pygame.transform.scale(self.blue_piece_image, (piece_new_side, piece_new_side))
        self.game_board_tile = pygame.transform.scale(self.game_board_tile, ( tile_new_side, tile_new_side))


    def register_spacing(self):
        self.BOARD_SIZE = 750
        self.BORDER_SIZE = 25
        self.PIECE_OFFSET = (self.TYLE_SIZE - self.PIECE_SIZE)/2

        if self.board_type == BoardType.Board_5X5:
            self.BEETWEEN_TYLE_SIZE = (self.BOARD_SIZE - 5*self.TYLE_SIZE)/4
        elif self.board_type == BoardType.Board_7X7:
            self.BEETWEEN_TYLE_SIZE = (self.BOARD_SIZE - 7*self.TYLE_SIZE)/6


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


        pygame.display.flip()

    def is_between(self, coords, top_left_point, bot_right_point):
        if top_left_point[0] <= coords[0] <= bot_right_point[0] and top_left_point[1] <= coords[1] <= bot_right_point[1]:
            return True
        else:
            return False


    def handle_mouse_key_press(self, mouse_coords):
        print("Mouse button Pressed at: ", mouse_coords)
        if self.board_type == BoardType.Board_5X5:
            board_side = 5
        else:
            board_side = 7

        if mouse_coords[0] <= self.BORDER_SIZE or mouse_coords[1] <= self.BORDER_SIZE:
            print("B4 Board")
        elif mouse_coords[0] >= self.BOARD_SIZE+self.BORDER_SIZE or mouse_coords[1] >= self.BOARD_SIZE+self.BORDER_SIZE:
            print("After Board")
        else:
            current_coords = (self.BORDER_SIZE+self.PIECE_OFFSET, self.BORDER_SIZE+self.PIECE_OFFSET)
            for line in range(0, board_side): # Lines
                for column in range(0, board_side):  # Columns
                    opposite_side = (current_coords[0] + self.PIECE_SIZE, current_coords[1] + self.PIECE_SIZE)
                    if self.is_between(mouse_coords, current_coords, opposite_side):
                        print("Coords: (", column, ",", line,")")

                    current_coords = (current_coords[0] + self.PIECE_SIZE + 2 * self.PIECE_OFFSET + self.BEETWEEN_TYLE_SIZE,
                                        current_coords[1])

                current_coords = (self.BORDER_SIZE+self.PIECE_OFFSET,
                                  current_coords[1]+self.PIECE_SIZE+2*self.PIECE_OFFSET+self.BEETWEEN_TYLE_SIZE)


            print("Tile / Between tiles")

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
                    self.handle_mouse_key_press(pygame.mouse.get_pos())
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    print("ESPACOOOOOOOOOOOOOO")
                # elif event.type == MOUSEMOTION:
                # print("Mouse Movement")
            self.display()

        pygame.quit()