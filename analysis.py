from neutron import Neutron
from neutron_util import BoardTypes, Player, get_next_move, get_time_miliseconds, PlayerTypes, Turn
import pygame


def play_game(board_type, depth, heuristic, depth_op, heuristic_op):
    game = Neutron(board_type=board_type)

    game.player_type['White'] = PlayerTypes.Player
    game.player_type['Black'] = PlayerTypes.Player

    game.start()

    n_white_plays = 0
    white_times = []
    n_black_plays = 0
    black_times = []
    game_ended = game.has_finished()[0]
    while not game_ended:
        if game.curr_player == Player.White:
            calculation_start_time = get_time_miliseconds()
            neutron_move, pawn_coords, pawn_move = get_next_move(game, heuristic, depth)
            calculation_end_time = get_time_miliseconds()

            white_times.append((calculation_end_time - calculation_start_time) / 1000)
            # print("White bot took ", (calculation_end_time - calculation_start_time) / 1000, "s to calculate his move")

            if game.turn == Turn.Neutron:
                game.move_piece(game.neutron_position[0], game.neutron_position[1], neutron_move)
                n_white_plays += 1
                if game.has_finished()[0]:
                    break

            game.move_piece(pawn_coords[0], pawn_coords[1], pawn_move)
            n_white_plays += 1

        else:
            calculation_start_time = get_time_miliseconds()
            neutron_move, pawn_coords, pawn_move = get_next_move(game, heuristic_op, depth_op)
            calculation_end_time = get_time_miliseconds()

            black_times.append((calculation_end_time - calculation_start_time)/1000)
            # print("Black bot took ", (calculation_end_time - calculation_start_time)/1000, "s to calculate his move")

            if game.turn == Turn.Neutron:
                game.move_piece(game.neutron_position[0], game.neutron_position[1], neutron_move)
                n_black_plays += 1
                if game.has_finished()[0]:
                    break

            game.move_piece(pawn_coords[0], pawn_coords[1], pawn_move)
            n_black_plays += 1

        game_ended = game.has_finished()[0]

    print("Game ended")
    # print("Black bot played:", n_black_plays, "times.")
    # print("White bot played:", n_white_plays, "times.")
    return n_white_plays, (sum(white_times) / len(white_times)), n_black_plays, (sum(black_times) / len(black_times))


def get_heuristic_depth(player_type):
    if player_type == PlayerTypes.CpuGreedy:
        return 1, 1
    elif player_type == PlayerTypes.CpuL0:
        return 1, 2
    elif player_type == PlayerTypes.CpuL1:
        return 1, 3
    elif player_type == PlayerTypes.CpuL2:
        return 2, 3
    elif player_type == PlayerTypes.CpuL3:
        return 3, 3

def print_results(results):
    total_white_plays = 0
    total_black_plays = 0
    total_white_average_time = 0
    total_black_average_time = 0
    for result in results:
        total_white_plays += result[0]
        total_white_average_time += result[1]
        total_black_plays += result[2]
        total_black_average_time += result[3]

    print("White player made, in average, {:.6f}".format(total_white_plays / len(results)), " in about {:.6f}".format(total_white_average_time / len(results)), "s each!")
    print("Black player made, in average, {:.6f}".format(total_black_plays / len(results)), " in about {:.6f}".format(total_black_average_time / len(results)), "s each!")

def benchmark(player1_type, player2_type, n_games, board_type):
    p1_heur, p1_dept = get_heuristic_depth(player1_type)
    p2_heur, p2_dept = get_heuristic_depth(player2_type)
    count = 0
    results = []
    while count < n_games:
        result = play_game(board_type, p1_dept, p1_heur, p2_dept, p2_heur)
        results.append(result)
        count += 1

    pygame.quit()
    print_results(results)

if __name__ == '__main__':
    benchmark(PlayerTypes.CpuL3, PlayerTypes.CpuL2, 10, BoardTypes.Board_5X5)
 