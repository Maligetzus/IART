from minimax import minimax
from neutron import Neutron
import neutron_util
from neutron_util import Direction

def main():
    # game = Neutron(5, neutron_util.Player.White, neutron_util.Turn.Pawn, [["0", "B", "0", "0", "B"], ["0", "0", "0", "0", "0"], ["0", "0", "B", "B", "W"], ["0", "0", "B", "0", "N"], ["0", "W", "W", "W", "W"]])
    game = Neutron(5)
    game.start()

    finished, winner = game.has_finished()

    while not finished:
        game.draw_board()

        print(game.curr_player.value + " player, play " + game.turn.value + " (ex.: E1 5)")
        print("Directions: 0 - Up, 1 - Down, 2 - Left, 3 - Right, 4 - LeftUp, 5 - RightUp, 6 - LeftDown, 7 - RightDown")
        
        success = False
        
        while not success:
            move = input()

            squares = move.split(" ")

            if len(squares) != 2:
                success = False
            else:
                destination = None

                if(squares[1] == "0"):
                    destination = Direction.Up
                elif(squares[1] == "1"):
                    destination = Direction.Down
                elif(squares[1] == "2"):
                    destination = Direction.Left
                elif(squares[1] == "3"):
                    destination = Direction.Right
                elif(squares[1] == "4"):
                    destination = Direction.LeftUp
                elif(squares[1] == "5"):
                    destination = Direction.RightUp
                elif(squares[1] == "6"):
                    destination = Direction.LeftDown
                elif(squares[1] == "7"):
                    destination = Direction.RightDown

                if(destination != None):
                    origin_x, origin_y = Neutron.square_to_index(squares[0])

                    success = game.move_piece(origin_x, origin_y, destination)
                else:
                    success = False

            if not success:
                print("Bad input!\n")

        finished, winner = game.has_finished()

    print("Winner: " + winner.value)

    # minimax(game)


if __name__ == '__main__':
    main()
