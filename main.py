import pygame

from minimax import minimax
from neutron import Neutron
import neutron_util
from neutron_util import Direction, BoardTypes
import game_gui
from pygame.locals import *

def main():
    game = Neutron(BoardTypes.Board_5X5)
    game.start()

    finished, winner = game.has_finished()

    # Prepare Game Objects
    clock = pygame.time.Clock()

    quit_pressed = False
    while not finished:

        print(game.curr_player.value + " player, play " + game.turn.value + " (ex.: E1 5)")

        current_turn = game.curr_player
        while game.curr_player == current_turn and not quit_pressed:
            # Max 60 frames per second
            clock.tick(60)

            # Handle Input Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit_pressed = True
                    finished = True
                    break

                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    quit_pressed = True
                    finished = True
                    break

                elif event.type == MOUSEBUTTONDOWN:
                    game.gui.state.handle_mouse_down()

                elif event.type == MOUSEBUTTONUP:
                    game.gui.state.handle_mouse_up()

                elif event.type == KEYDOWN and event.key == K_SPACE:
                    print("ESPACOOOOOOOOOOOOOO")

                # turn_ended = True
                finished, winner = game.has_finished()

            game.gui.display()

    if not quit_pressed:
        print("Winner: " + winner.value)
    else:
        print("Game closed by User")

    pygame.quit()


if __name__ == '__main__':
    main()
