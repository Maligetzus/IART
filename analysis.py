from neutron import Neutron
from neutron_util import BoardTypes, Player

def play_game(board_type, depth, heuristic, depth_op, heuristic_op):
    game = Neutron(board_type=board_type)

    game.start()

    while not game.has_finished():
        if game.curr_player == Player.White:
            

for board_type in BoardTypes:
    for depth in range(1, 3):
        for heuristic in range(1, 3):

            for depth_op in range(1, 3):
                for heuristic_op in range(1, 3):
 