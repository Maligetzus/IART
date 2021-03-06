import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
import threading
from NeutronGame.neutron import Neutron
from NeutronGame.neutron_util import get_next_move, get_next_move_random, get_next_move_ordered, BoardTypes, PlayerTypes, Turn
from pygame.locals import *

class GameLoop:
    def __init__(self, board_type, player1_type, player2_type):
        self.game = Neutron(board_type)

        self.game.player_type['White'] = player1_type
        self.game.player_type['Black'] = player2_type
        print(self.game.player_type['White'], " // ", self.game.player_type['Black'])

        self.neutron_move = None
        self.pawn_move = None
        self.pawn_coords = None

        if player1_type == PlayerTypes.Player and player2_type != PlayerTypes.Player or\
            player1_type != PlayerTypes.Player and player2_type == PlayerTypes.Player:
            self.analyse_cpu = True
        else:
            self.analyse_cpu = False

        self.cpu_times = []
        self.cpu_plays = 0

        # For threading
        self.waiting = False    # indicates if a background thread is running
        self.done = False       # indicates if the background task is done
        
    def restore_menu_dimensions(self):
        self.game.gui.screen = pygame.display.set_mode((650, 575), 0, 32)

    # Returns finished, quit_pressed, esc_pressed
    def handle_player_input(self, can_move):
        # can_move indicates if the player can do a move input

        # Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return True, True, False

            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.restore_menu_dimensions()
                return True, False, True

            elif can_move and event.type == MOUSEBUTTONDOWN:
                self.game.gui.state.handle_mouse_down()

            elif can_move and event.type == MOUSEBUTTONUP:
                self.game.gui.state.handle_mouse_up()

        return False, False, False

    def handle_bot_play(self):
        # if the background task is done, it won't trigger it again (yet)
        if not self.done and self.pawn_move == None:
            heuristic = 3
            max_depth = 3

            if self.game.player_type[self.game.curr_player.value] == PlayerTypes.CpuGreedy:
                heuristic = 1
                max_depth = 1
            elif self.game.player_type[self.game.curr_player.value] == PlayerTypes.CpuL0:
                heuristic = 1
                max_depth = 2
            elif self.game.player_type[self.game.curr_player.value] == PlayerTypes.CpuL1:
                heuristic = 1
                max_depth = 3
            elif self.game.player_type[self.game.curr_player.value] == PlayerTypes.CpuL2:
                heuristic = 2
                max_depth = 3

            def get_result(instance, heuristic, max_depth):
                start_time = time.time()
                
                if instance.game.player_type[instance.game.curr_player.value] == PlayerTypes.CpuRandom:
                    instance.neutron_move, instance.pawn_coords, instance.pawn_move = get_next_move_random(instance.game, heuristic, max_depth)
                elif instance.game.player_type[instance.game.curr_player.value] == PlayerTypes.CpuOrdered:
                    instance.neutron_move, instance.pawn_coords, instance.pawn_move = get_next_move_ordered(instance.game, heuristic, max_depth)
                else:
                    instance.neutron_move, instance.pawn_coords, instance.pawn_move = get_next_move(instance.game, heuristic, max_depth)
                
                if instance.analyse_cpu:
                    instance.cpu_times.append(time.time() - start_time)
                    instance.cpu_plays += 1

                # task is done
                instance.done = True
                instance.waiting = False

            # triggers background task
            self.waiting = True
            self.done = False
            thread = threading.Thread(target=get_result, args=(self, heuristic, max_depth))
            thread.setDaemon(True)
            thread.start()

        # Only enters if background task is done
        if self.done:
            if self.game.turn == Turn.Neutron:
                self.game.move_piece(self.game.neutron_position[0], self.game.neutron_position[1], self.neutron_move)
                self.neutron_move = None
            elif self.game.turn == Turn.Pawn:
                self.game.move_piece(self.pawn_coords[0], self.pawn_coords[1], self.pawn_move)
                self.pawn_coords = None
                self.pawn_move = None

                # Reset threading done variable
                self.done = False

            finished, winner = self.game.has_finished()
            return finished, winner
        else:
            return False, None


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
            can_move = False

            if self.game.player_type[self.game.curr_player.value] == PlayerTypes.Player:
                can_move = True # if it's the player's turn, he can move
            else:
                # if it's not waiting for the background task, it can handle bot play
                if not self.waiting:
                    finished, winner = self.handle_bot_play()

            finished, quit_pressed, esc_pressed = self.handle_player_input(can_move)

            # only checks if game has finished if it's not waiting for background task
            if not self.waiting and not finished and self.game.turn != current_turn:
                finished, winner = self.game.has_finished()

            self.game.render()

        if self.analyse_cpu:
            print("Number of CPU plays: ", end="")
            print(self.cpu_plays)

            average_time = 0

            for i in range(len(self.cpu_times)):
                average_time += self.cpu_times[i]

            if len(self.cpu_times) != 0:
                average_time /= len(self.cpu_times)

            print("Average time per move: ", end="")
            print(average_time, end="")
            print(" seconds")

        if quit_pressed:  # Closes window
            pygame.quit()
            print("Game closed by User")
        elif esc_pressed:  # Returns to main menu
            print("Game ended, returning to main menu!")
        else:
            print("Winner: " + winner.value)  # Prints winner; Returns to main menu
            self.game.gui.display_winner(self.game.player_type[winner.value], winner)

            esc_pressed = False
            while not esc_pressed:
                # Max 60 frames per second
                clock.tick(60)

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        print("Game closed by User")

                    elif event.type == KEYDOWN and event.key == K_ESCAPE:
                        self.restore_menu_dimensions()
                        esc_pressed = True
                        break
