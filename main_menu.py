import pygame, sys
from pygame import Surface
from pygame.locals import *
from game_loop import GameLoop
from gui_utils import draw_text
from neutron_util import PlayerTypes, BoardTypes


class MainMenu:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Neutron')
        self.screen = pygame.display.set_mode((650, 575), 0, 32)
        self.mainClock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 32, False)
        self.current_player1_index = 0
        self.current_player2_index = 0
        self.player_types_arr = [PlayerTypes.Player, PlayerTypes.CpuGreedy, PlayerTypes.CpuL0, PlayerTypes.CpuL1, PlayerTypes.CpuL2, PlayerTypes.CpuL3]
        self.board_size_index = 0
        self.board_size_array = [BoardTypes.Board_5X5, BoardTypes.Board_7X7]
        # Resources
        self.game_image = pygame.image.load('resources/main_menu.jpg')

    def start(self):
        while True:
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.game_image, (75, 50))

            mx, my = pygame.mouse.get_pos()

            menu = Surface((500, 250))
            menu.fill((255, 255, 255))

            vs_section = Surface((500, 45))
            vs_section.fill((255, 255, 255))

            # VS-Section: Player1
            player1_button = pygame.Rect(75, 400, 200, 45)
            if player1_button.collidepoint((mx, my)):
                if click:
                    self.current_player1_index += 1
                    self.current_player1_index %= len(self.player_types_arr)

            pygame.draw.rect(vs_section, (0, 0, 0), player1_button)
            player1_sur = Surface((200, 45))
            draw_text(self.player_types_arr[self.current_player1_index].value, self.font, (255, 255, 255), player1_sur, 0, 0, True, True)
            vs_section.blit(player1_sur, (0, 0))

            # VS-Section: Player2
            player2_button = pygame.Rect(375, 400, 200, 45)
            if player2_button.collidepoint((mx, my)):
                if click:
                    self.current_player2_index += 1
                    self.current_player2_index %= len(self.player_types_arr)

            pygame.draw.rect(vs_section, (0, 0, 0), player2_button)
            player2_sur = Surface((200, 45))
            draw_text(self.player_types_arr[self.current_player2_index].value, self.font, (255, 255, 255), player2_sur, 0, 0, True, True)
            vs_section.blit(player2_sur, (300, 0))

            # VS-Section: Vs
            draw_text("vs", self.font, (0, 0, 0), vs_section, 0, 0, True, True)
            menu.blit(vs_section, (0, 25))

            # Start_quit_section
            start_quit_section = Surface((500, 45))
            start_quit_section.fill((255, 255, 255))

            # Start_quit_section: Board dimensions
            board_button = pygame.Rect(75, 485, 150, 45)
            if board_button.collidepoint((mx, my)):
                if click:
                    self.board_size_index += 1
                    self.board_size_index %= len(self.board_size_array)

            pygame.draw.rect(start_quit_section, (0, 0, 0), board_button)
            board_sur = Surface((150, 45))
            draw_text(self.board_size_array[self.board_size_index].value, self.font, (255, 255, 255), board_sur, 0, 0, True, True)
            start_quit_section.blit(board_sur, (0, 0))

            # Start_quit_section: Start
            start_button = pygame.Rect(250, 485, 150, 45)
            if start_button.collidepoint((mx, my)):
                if click:
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
                if click:
                    pygame.quit()
                    sys.exit()

            pygame.draw.rect(start_quit_section, (0, 0, 0), quit_button)
            quit_sur = Surface((150, 45))
            draw_text("Quit", self.font, (255, 255, 255), quit_sur, 0, 0, True, True)
            start_quit_section.blit(quit_sur, (350, 0))

            menu.blit(start_quit_section, (0, 110))

            self.screen.blit(menu, (75, 375))

            click = False
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

            pygame.display.update()
            self.mainClock.tick(60)


