from neutron import Neutron
from neutron_util import BoardTypes, Player, get_next_move, get_time_miliseconds


def play_game(board_type, depth, heuristic, depth_op, heuristic_op):
    game = Neutron(board_type=board_type)


    game.start()

    n_white_plays = 0
    n_black_plays = 0
    while not game.has_finished():
        if game.curr_player == Player.White:
            calculation_start_time = get_time_miliseconds()
            neutron_move, pawn_coords, pawn_move = get_next_move(game, heuristic, depth)
            calculation_end_time = get_time_miliseconds()
            print("White bot took ", (calculation_end_time - calculation_start_time)/1000, "s to calculate his move")
            if game.turn == Neutron:  # 1st play doesnt move the neutron
                game.move_piece(game.neutron_position[0], game.neutron_position[1], neutron_move)
                n_white_plays += 1
                if game.has_finished():
                    break

            game.move_piece(pawn_coords[0], pawn_coords[1], pawn_move)
            n_white_plays += 1

        else:
            calculation_start_time = get_time_miliseconds()
            neutron_move, pawn_coords, pawn_move = get_next_move(game, heuristic_op, depth_op)
            calculation_end_time = get_time_miliseconds()
            print("Black bot took ", (calculation_end_time - calculation_start_time)/1000, "s to calculate his move")
            game.move_piece(game.neutron_position[0], game.neutron_position[1], neutron_move)
            n_black_plays += 1
            if game.has_finished():
                break
            game.move_piece(pawn_coords[0], pawn_coords[1], pawn_move)
            n_black_plays
    print("Game ended")


# for board_type in BoardTypes:
#     for depth in range(1, 3):
#         for heuristic in range(1, 3):
#
#             for depth_op in range(1, 3):
#                 for heuristic_op in range(1, 3):

if __name__ == '__main__':
    play_game(BoardTypes.Board_5X5, 1, 1, 3, 3)
 