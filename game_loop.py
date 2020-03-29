import pygame
from neutron import Neutron
from neutron_util import BoardTypes
from pygame.locals import *


def restore_menu_dimensions(game):
    game.gui.screen = pygame.display.set_mode((650, 500), 0, 32)


def game_loop():
    game = Neutron(BoardTypes.Board_5X5)
    game.start()

    finished, winner = game.has_finished()

    # Prepare Game Objects
    clock = pygame.time.Clock()

    quit_pressed = False
    esc_pressed = False
    while not finished:
        current_turn = game.turn
        while game.turn == current_turn and not (quit_pressed or esc_pressed):
            # Max 60 frames per second
            clock.tick(60)

            # Handle Input Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit_pressed = True
                    finished = True
                    break

                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    esc_pressed = True
                    finished = True
                    restore_menu_dimensions(game)
                    break

                elif event.type == MOUSEBUTTONDOWN:
                    game.gui.state.handle_mouse_down()

                elif event.type == MOUSEBUTTONUP:
                    game.gui.state.handle_mouse_up()

                # turn_ended = True
                finished, winner = game.has_finished()

            game.gui.display()

    if quit_pressed:  #Closes window
        pygame.quit()
        print("Game closed by User")
    elif esc_pressed:  #Returns to main menu
        print("Game ended, returning to main menu!")
    else:
        print("Winner: " + winner.value)  #Prints winner; Returns to main menu
        restore_menu_dimensions(game)