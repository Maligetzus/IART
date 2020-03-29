import pygame
from neutron import Neutron
from neutron_util import BoardTypes, PlayerTypes
from pygame.locals import *
from neutron_util import get_next_move


def restore_menu_dimensions(game):
    game.gui.screen = pygame.display.set_mode((650, 500), 0, 32)

# Returns finished, quit_pressed, esc_pressed
def handle_player_input(game):
    # Handle Input Events
    for event in pygame.event.get():
        if event.type == QUIT:
            return True, True, False

        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            restore_menu_dimensions(game)
            return True, False, True

        elif event.type == MOUSEBUTTONDOWN:
            game.gui.state.handle_mouse_down()

        elif event.type == MOUSEBUTTONUP:
            game.gui.state.handle_mouse_up()

    return False, False, False

def handle_bot_play(game):
    if game.player_type[game.curr_player.value] == PlayerTypes.CpuL1:
        return handle_bot_l1_play(game)
    else:
        return handle_bot_l2_play(game)


def handle_bot_l1_play(game):
    print("Bot LVL1 turn")
    finished, winner = game.has_finished()
    return finished, winner


def handle_bot_l2_play(game):
    neutron_move, pawn_coord, pawn_move = get_next_move(game, 1, 3)

    if neutron_move != None:
        game.move_piece(game.neutron_position[0], game.neutron_position[1], neutron_move)

    finished, winner = game.has_finished()

    if not finished:
        game.move_piece(pawn_coord[0], pawn_coord[1], pawn_move)
        finished, winner = game.has_finished()

    return finished, winner


def game_loop(player1_type, player2_type):
    game = Neutron(BoardTypes.Board_5X5)
    game.start()

    game.player_type['White'] = player1_type
    game.player_type['Black'] = player2_type
    print(game.player_type['White'], " // ", game.player_type['Black'])

    finished, winner = game.has_finished()

    clock = pygame.time.Clock()
    quit_pressed = False
    esc_pressed = False
    while not finished:
        # Max 60 frames per second
        clock.tick(60)

        current_turn = game.turn
        if game.player_type[game.curr_player.value] == PlayerTypes.Player:
            finished, quit_pressed, esc_pressed = handle_player_input(game)
        else:
            finished, winner = handle_bot_play(game)

        if not finished and game.turn != current_turn:
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