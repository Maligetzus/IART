import pygame, sys
from pygame.locals import *
from game_loop import game_loop


class MainMenu:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('game base')
        self.screen = pygame.display.set_mode((650, 650), 0, 32)
        self.mainClock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 20)

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def start(self):
        while True:

            self.screen.fill((0, 0, 0))
            self.draw_text('main menu', self.font, (255, 255, 255), self.screen, 20, 20)

            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(50, 100, 200, 50)
            button_2 = pygame.Rect(50, 200, 200, 50)
            if button_1.collidepoint((mx, my)):
                if click:
                    game_loop()
            if button_2.collidepoint((mx, my)):
                if click:
                    pygame.quit()
                    sys.exit()
            pygame.draw.rect(self.screen, (255, 0, 0), button_1)
            self.draw_text("Gamee", self.font, (255, 255, 0), self.screen, 50, 100)
            pygame.draw.rect(self.screen, (255, 0, 0), button_2)
            self.draw_text("Quit", self.font, (255, 255, 0), self.screen, 50, 200)

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

    def game(self):
        self.screen = pygame.display.set_mode((800, 800), 0, 32)
        running = True
        while running:
            self.screen.fill((0, 0, 0))

            self.draw_text('game', self.font, (255, 255, 255), self.screen, 20, 20)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.screen = pygame.display.set_mode((650, 650), 0, 32)
                        running = False

            pygame.display.update()
            self.mainClock.tick(60)

    def options(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))

            self.draw_text('options', self.font, (255, 255, 255), self.screen, 20, 20)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

            pygame.display.update()
            self.mainClock.tick(60)


