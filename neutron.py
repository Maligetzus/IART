import neutron_util as nutils
from neutron_util import Player, Turn, Direction, Tile, BoardTypes
import copy
from game_gui import GameGui


class Neutron:

    def __init__(self, board_type, curr_player=Player.White, turn=Turn.Neutron, state=None, neutron_position=(-1, -1)):
        self.board_type = board_type
        if board_type == BoardTypes.Board_5X5:
            self.size = 5
        else:
            self.size = 7
        self.turn = turn
        self.curr_player = curr_player
        self.state = state #AKA Board
        self.neutron_position = neutron_position

    def start(self, starting_player=Player.White):
        """
        Initializes the game.
        """
        if self.size < 3 or self.size % 2 == 0:
            return False, "Board length has to be an odd number bigger than 2"

        self.curr_player = starting_player
        self.turn = Turn.Pawn
        self.state = []
        self.neutron_position = int(self.size / 2), int(self.size / 2)

        for i in range(0, self.size):
            row = []

            for j in range(0, self.size):
                if i == 0:
                    row.append(Tile.Black)
                elif i == int(self.size / 2) and j == int(self.size / 2):
                    row.append(Tile.Neutron)
                elif i == self.size - 1:
                    row.append(Tile.White)
                else:
                    row.append(Tile.Empty)

            self.state.append(row)
            self.gui = GameGui(self, self.board_type)

        return True, "Successfuly started the game"

    def has_finished(self):

        if nutils.victory(Player.Black, self.state):
            return True, Player.Black

        if nutils.victory(Player.White, self.state):
            return True, Player.White

        if nutils.num_empty_fields_around_neutron(self.state, self.neutron_position) == 0:
            return True, Player.White if self.curr_player != Player.White else Player.Black
        else:
            return False, None

    def move_piece(self, origin_x, origin_y, direction):
        return self.__move_piece(self, origin_x, origin_y, direction)

    def hypothetical_move_piece(self, origin_x, origin_y, direction):
        game = Neutron(self.size, self.curr_player, self.turn, copy.deepcopy(self.state), self.neutron_position)
        
        success = self.__move_piece(game, origin_x, origin_y, direction)

        return success, game

    @staticmethod
    def __move_piece(self, origin_x, origin_y, direction):
        valid, destination_x, destination_y = self.can_move(origin_x, origin_y, direction)
        
        if not valid:
            return False

        if self.state[origin_x][origin_y] == Tile.Neutron:
            self.neutron_position = destination_x, destination_y

        self.state[origin_x][origin_y], self.state[destination_x][destination_y] = \
            self.state[destination_x][destination_y], self.state[origin_x][origin_y]

        if self.turn == Turn.Pawn:
            self.curr_player = Player.White if self.curr_player != Player.White else Player.Black

            self.turn = Turn.Neutron
        else:
            self.turn = Turn.Pawn

        return True

    def can_move(self, origin_x, origin_y, direction):
        if (origin_x < 0 or origin_x >= self.size
                or origin_y < 0 or origin_y >= self.size):
            return False, origin_x, origin_y

        if self.turn == Turn.Neutron and self.state[origin_x][origin_y] != Tile.Neutron:
            return False, origin_x, origin_y

        if self.turn == Turn.Pawn and self.curr_player == Player.White and self.state[origin_x][origin_y] != Tile.White:
            return False, origin_x, origin_y

        if self.turn == Turn.Pawn and self.curr_player == Player.Black and self.state[origin_x][origin_y] != Tile.Black:
            return False, origin_x, origin_y

        move_x = 0
        move_y = 0

        if direction == Direction.Down or direction == Direction.LeftDown or direction == Direction.RightDown:
            move_x = 1
        
        if direction == Direction.Up or direction == Direction.LeftUp or direction == Direction.RightUp:
            move_x = -1

        if direction == Direction.Right or direction == Direction.RightUp or direction == Direction.RightDown:
            move_y = 1
        
        if direction == Direction.Left or direction == Direction.LeftUp or direction == Direction.LeftDown:
            move_y = -1

        aux_x = origin_x
        next_x = origin_x
        aux_y = origin_y
        next_y = origin_y

        hit = False

        while not hit:
            aux_x = next_x
            aux_y = next_y

            next_x = aux_x + move_x
            next_y = aux_y + move_y

            if (next_x < 0 or next_x >= self.size
                    or next_y < 0 or next_y >= self.size):
                hit = True
            elif self.state[next_x][next_y] != Tile.Empty:
                hit = True

        if aux_x == origin_x and aux_y == origin_y:
            return False, origin_x, origin_y

        return True, aux_x, aux_y

    def draw_board(self):

        print(" ", end=" ")

        for i in range(1, self.size + 1):
            print(i, end=" ")

        print("\n", end="")

        for i in range(0, self.size):
            print(chr(65 + i), end=" ")

            for j in range(0, len(self.state[i])):
                print(self.state[i][j].value, end=" ")

            print("\n", end="")

        print("\n", end="")

    @staticmethod
    def square_to_index(square):
        x = -1
        y = -1

        if len(square) != 2:
            return x, y

        x = ord(square[0].upper()) - ord('A')

        y = int(square[1]) - 1

        return x, y
