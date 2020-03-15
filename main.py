from minimax import minimax
from neutron import Neutron
import neutron_util

import game_gui

def main():
    # game = Neutron(5, neutron_util.Player.White, neutron_util.Turn.Pawn, [["0", "B", "0", "0", "B"], ["0", "0", "0", "0", "0"], ["0", "0", "B", "B", "W"], ["0", "0", "B", "0", "N"], ["0", "W", "W", "W", "W"]])
    game = Neutron(5)
    game.start()

    finished, winner = game.has_finished()

    while not finished:
        game.draw_board()

        print(game.curr_player.value + " player, play " + game.turn.value + " (ex.: E1 B1):")
        
        success = False
        
        while not success:
            move = input()

            squares = move.split(" ")

            if len(squares) != 2:
                success = False
            else:
                origin_x, origin_y = Neutron.square_to_index(squares[0])
                destination_x, destination_y = Neutron.square_to_index(squares[1])

                success = game.move_piece(origin_x, origin_y, destination_x, destination_y)

            if not success:
                print("Bad input!\n")

        finished, winner = game.has_finished()

    print("Winner: " + winner.value)

    # minimax(game)


if __name__ == '__main__':
    #main()
    game_gui.init_game_window()
