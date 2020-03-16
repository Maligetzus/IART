import pygame
from pygame.locals import *


class BoardGUI:
    def __init__(self, board):
        self.board = board
        self.init_window()
        self.load_resources()
        self.load_background()

    def init_window(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800), DOUBLEBUF)
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
        currLineNumber = 0
        currColNumber = 0

        for line in self.board:
            for tile in line:
                currentTileCoords = (25 + currColNumber*132 + 15 * currColNumber, 25 + currLineNumber*132 + 15 * currLineNumber)
                self.screen.blit(self.game_board_tile, currentTileCoords)

                currentPieceCoords = (25 + currColNumber * 132 + 15 * currColNumber + 3, 25 + currLineNumber * 132 + 15 * currLineNumber + 3)
                if tile == 'R':
                    self.screen.blit(self.red_piece_image, currentPieceCoords)
                elif tile == 'B':
                    self.screen.blit(self.blue_piece_image, currentPieceCoords)

                currColNumber += 1

            currColNumber = 0
            currLineNumber += 1



        self.screen.blit(self.game_board_tile, (25, 25))

        #Pieces
        self.screen.blit(self.blue_piece_image, (28, 28))
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