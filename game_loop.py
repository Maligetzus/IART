import pygame
import time
from neutron import Neutron
from neutron_util import BoardTypes, PlayerTypes
from pygame.locals import *
from neutron_util import get_next_move, Turn


class GameLoop:
    def __init__(self, player1_type, player2_type):
        self.game = Neutron(BoardTypes.Board_5X5)

        self.game.player_type['White'] = player1_type
        self.game.player_type['Black'] = player2_type
        print(self.game.player_type['White'], " // ", self.game.player_type['Black'])

        self.pawn_move = None
        self.pawn_coords = None
        
    def restore_menu_dimensions(self):
        self.game.gui.screen = pygame.display.set_mode((650, 575), 0, 32)

    # Returns finished, quit_pressed, esc_pressed
    def handle_player_input(self):
        # Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return True, True, False

            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.restore_menu_dimensions()
                return True, False, True

            elif event.type == MOUSEBUTTONDOWN:
                self.game.gui.state.handle_mouse_down()

            elif event.type == MOUSEBUTTONUP:
                self.game.gui.state.handle_mouse_up()

        return False, False, False

    def handle_bot_play(self):
        if self.pawn_move == None:
            if self.game.player_type[self.game.curr_player.value] == PlayerTypes.CpuGreedy:
                neutron_move, self.pawn_coords, self.pawn_move = get_next_move(self.game, 1, 1)
            elif self.game.player_type[self.game.curr_player.value] == PlayerTypes.CpuL0:
                neutron_move, self.pawn_coords, self.pawn_move = get_next_move(self.game, 1, 2)
            elif self.game.player_type[self.game.curr_player.value] == PlayerTypes.CpuL1:
                neutron_move, self.pawn_coords, self.pawn_move = get_next_move(self.game, 1, 3)
            elif self.game.player_type[self.game.curr_player.value] == PlayerTypes.CpuL2:
                neutron_move, self.pawn_coords, self.pawn_move = get_next_move(self.game, 2, 3)
            else:
                neutron_move, self.pawn_coords, self.pawn_move = get_next_move(self.game, 3, 3)

        if self.game.turn == Turn.Neutron:
            self.game.move_piece(self.game.neutron_position[0], self.game.neutron_position[1], neutron_move)
        elif self.game.turn == Turn.Pawn:
            self.game.move_piece(self.pawn_coords[0], self.pawn_coords[1], self.pawn_move)
            self.pawn_coords = None
            self.pawn_move = None

        finished, winner = self.game.has_finished()
        return finished, winner


    def game_loop(self):
        self.game.start()
        finished, winner = self.game.has_finished()

        clock = pygame.time.Clock()
        quit_pressed = False
        esc_pressed = False
        while not finished:
            # Max 60 frames per second
            clock.tick(60)

            current_turn = self.game.turn
            if self.game.player_type[self.game.curr_player.value] == PlayerTypes.Player:
                finished, quit_pressed, esc_pressed = self.handle_player_input()
            else:
                finished, winner = self.handle_bot_play()

            if not finished and self.game.turn != current_turn:
                finished, winner = self.game.has_finished()

            self.game.gui.display()

        if quit_pressed:  # Closes window
            pygame.quit()
            print("Game closed by User")
        elif esc_pressed:  # Returns to main menu
            print("Game ended, returning to main menu!")
        else:
            print("Winner: " + winner.value)  # Prints winner; Returns to main menu
            self.restore_menu_dimensions()