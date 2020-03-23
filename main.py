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

    while not finished:

        print(game.curr_player.value + " player, play " + game.turn.value + " (ex.: E1 5)")

        #Max 60 frames per second
        clock.tick(60)

        turn_ended = False
        while not turn_ended:
            # Handle Input Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    turn_ended = True
                    finished = True
                    winner = "GameClosed"
                    break

                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    turn_ended = True
                    finished = True
                    winner = "GameClosed"
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

    print("Winner: " + winner)
    pygame.quit()


if __name__ == '__main__':
    main()
