import pygame, sys
from pygame.locals import *
from game_loop import game_loop


class MainMenu:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('game base')
        self.screen = pygame.display.set_mode((650, 500), 0, 32)
        self.mainClock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 42, False)

        # Resources
        self.game_image = pygame.image.load('resources/main_menu.jpg')

    @staticmethod
    def draw_text(text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def start(self):
        while True:

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.game_image, (75,50))

            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(75, 400, 200, 45)
            button_2 = pygame.Rect(360, 400, 200, 45)
            if button_1.collidepoint((mx, my)):
                if click:
                    game_loop()
            if button_2.collidepoint((mx, my)):
                if click:
                    pygame.quit()
                    sys.exit()
            pygame.draw.rect(self.screen, (0, 0, 0), button_1)
            self.draw_text("Play", self.font, (255, 255, 255), self.screen, 142, 410)
            pygame.draw.rect(self.screen, (0, 0, 0), button_2)
            self.draw_text("Exit", self.font, (255, 255, 255), self.screen, 432, 410)

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


