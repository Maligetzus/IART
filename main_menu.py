import pygame, sys
from pygame import Surface
from pygame.locals import *
from game_loop import GameLoop
from gui_utils import draw_text
from neutron_util import PlayerTypes, BoardTypes


class MainMenu:
    def __init__(self):
        # Initializes pygame
        pygame.init()
        # Sets window title
        pygame.display.set_caption('Neutron')
        # Sets window icon
        icon = pygame.image.load('resources/logo.png')
        pygame.display.set_icon(icon)
        # Creates a 650x575 window
        self.screen = pygame.display.set_mode((650, 575), 0, 32)
        # Used to limit number of executions per second
        self.mainClock = pygame.time.Clock()
        # Font used for the buttons
        self.font = pygame.font.SysFont(None, 32, False)
        # Store the indexes of the selected types of the players
        self.current_player1_index = 0
        self.current_player2_index = 0
        # Stores the possible types of players
        self.player_types_arr = [PlayerTypes.Player, PlayerTypes.CpuGreedy, PlayerTypes.CpuL0, PlayerTypes.CpuL1,
                                PlayerTypes.CpuL2, PlayerTypes.CpuL3, PlayerTypes.CpuRandom, PlayerTypes.CpuOrdered]
        # Stores the selected board_size index
        self.board_size_index = 0
        # Stores the possible board sizes
        self.board_size_array = [BoardTypes.Board_5X5, BoardTypes.Board_7X7]
        # Main menu image
        self.game_image = pygame.image.load('resources/main_menu.jpg')

    def start(self):
        while True:
            # Clears the screen by painting it white
            self.screen.fill((255, 255, 255))
            # Displays the main menu image
            self.screen.blit(self.game_image, (75, 50))

            # Gets the current mouse coords
            mx, my = pygame.mouse.get_pos()

            # Creates a surface to "place" the menu
            menu = Surface((500, 250))
            # Turns the surface white
            menu.fill((255, 255, 255))

            # Creates a surface for the Player1 vs Player2 section
            vs_section = Surface((500, 45))
            # Turns the surface white
            vs_section.fill((255, 255, 255))

            # VS-Section: Player1
            # Creates a button
            player1_button = pygame.Rect(75, 400, 200, 45)
            if player1_button.collidepoint((mx, my)):
                if click:  # Button click handler
                    self.current_player1_index += 1  # Cycles through all the possible player types for player1
                    self.current_player1_index %= len(self.player_types_arr)

            # Draws the player1 button
            pygame.draw.rect(vs_section, (0, 0, 0), player1_button)
            # Creates a black surface with the same diemnsions as the button
            player1_sur = Surface((200, 45))
            # Writes the player type on the surface, centered horizontally
            draw_text(self.player_types_arr[self.current_player1_index].value, self.font, (255, 255, 255), player1_sur, 0, 0, True, True)
            # "Places" surface on the vs_section
            vs_section.blit(player1_sur, (0, 0))

            # VS-Section: Player2
            # Creates a button
            player2_button = pygame.Rect(375, 400, 200, 45)
            if player2_button.collidepoint((mx, my)):
                if click:  # Button click handler
                    self.current_player2_index += 1  # Cycles through all the possible player types for player2
                    self.current_player2_index %= len(self.player_types_arr)

            # Draws the player2 button
            pygame.draw.rect(vs_section, (0, 0, 0), player2_button)
            # Creates a black surface with the same diemnsions as the button
            player2_sur = Surface((200, 45))
            # Writes the player type on the surface, centered horizontally
            draw_text(self.player_types_arr[self.current_player2_index].value, self.font, (255, 255, 255), player2_sur, 0, 0, True, True)
            # "Places" surface on the vs_section
            vs_section.blit(player2_sur, (300, 0))

            # VS-Section: Vs
            # Draws "vs" on the vs_section surface
            draw_text("vs", self.font, (0, 0, 0), vs_section, 0, 0, True, True)
            # "Places" vs_section on the menu surface
            menu.blit(vs_section, (0, 25))

            # Start_quit_section
            # Creates a surface for start, quit and board_size buttons
            start_quit_section = Surface((500, 45))
            # Turn it white
            start_quit_section.fill((255, 255, 255))

            # Start_quit_section: Board dimensions
            board_button = pygame.Rect(75, 485, 150, 45)
            if board_button.collidepoint((mx, my)):
                if click:  # Cycles through all the possible board sizes
                    self.board_size_index += 1
                    self.board_size_index %= len(self.board_size_array)

            pygame.draw.rect(start_quit_section, (0, 0, 0), board_button)
            board_sur = Surface((150, 45))
            # Drawn currently selected board_size on the button; Centered horizontally
            draw_text(self.board_size_array[self.board_size_index].value, self.font, (255, 255, 255), board_sur, 0, 0, True, True)
            start_quit_section.blit(board_sur, (0, 0))

            # Start_quit_section: Start
            start_button = pygame.Rect(250, 485, 150, 45)
            if start_button.collidepoint((mx, my)):
                if click:  # Starts a new game
                    gl = GameLoop(self.board_size_array[self.board_size_index],
                                  self.player_types_arr[self.current_player1_index],
                                  self.player_types_arr[self.current_player2_index])
                    gl.game_loop()

            pygame.draw.rect(start_quit_section, (0, 0, 0), start_button)
            start_sur = Surface((150, 45))
            draw_text("Start Game", self.font, (255, 255, 255), start_sur, 0, 0, True, True)
            start_quit_section.blit(start_sur, (175, 0))

            # Start_quit_section: Quit
            quit_button = pygame.Rect(425, 485, 150, 45)
            if quit_button.collidepoint((mx, my)):
                if click:  # Quits Main menu
                    pygame.quit()
                    sys.exit()

            pygame.draw.rect(start_quit_section, (0, 0, 0), quit_button)
            quit_sur = Surface((150, 45))
            draw_text("Quit", self.font, (255, 255, 255), quit_sur, 0, 0, True, True)
            start_quit_section.blit(quit_sur, (350, 0))

            # "Places" start_quit_section on menu
            menu.blit(start_quit_section, (0, 110))

            # "Places" menu on screen
            self.screen.blit(menu, (75, 375))

            # Main loop
            click = False
            # Cycles through all events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            # Updates the screen
            pygame.display.update()
            # Limits number of executions to 60 oer second
            self.mainClock.tick(60)


