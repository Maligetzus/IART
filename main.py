import pygame
from neutron import Neutron
import neutron_util
from neutron_util import Direction, BoardTypes, Player
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

        current_turn = game.turn
        while game.turn == current_turn and not quit_pressed:
            # Max 60 frames per second
            clock.tick(60)
            
            if game.curr_player == Player.Black:
                neutronMove, pawnCoord, pawnMove = neutron_util.get_next_move(game, 1, 3)

                if neutronMove != None:
                    game.move_piece(game.neutron_position[0], game.neutron_position[1], neutronMove)

                finished, winner = game.has_finished()

                if not finished:
                    game.move_piece(pawnCoord[0], pawnCoord[1], pawnMove)
            else:
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

            if not finished:
                finished, winner = game.has_finished()

            game.gui.display()

    if not quit_pressed:
        print("Winner: " + winner.value)
    else:
        print("Game closed by User")

    pygame.quit()


if __name__ == '__main__':
    main()
