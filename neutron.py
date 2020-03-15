import neutron_util as nutils
from neutron_util import Player, Turn

class Neutron:

    def __init__(self, size, curr_player=Player.White, turn=Turn.Neutron, state=None):
        self.size = size
        self.turn = turn
        self.curr_player = curr_player
        self.state = state

    def start(self, starting_player=Player.White):
        """
        Initializes the game.
        """

        if(self.size < 3 or self.size % 2 == 0):
            return False, "Board length has to be an odd number bigger than 2"

        self.curr_player = starting_player
        self.turn = Turn.Pawn
        self.state = []

        for i in range(0, self.size):
            row = []

            for j in range(0, self.size):
                if i == 0:
                    row.append("B")
                elif i == int(self.size / 2) and j == int(self.size / 2):
                    row.append("N")
                elif i == self.size - 1:
                    row.append("W")
                else:
                    row.append("0")

            self.state.append(row)

        return True, "Successfuly started the game"

    def has_finished(self):

        if nutils.victory(Player.Black, self.state):
            return True, Player.Black

        if nutils.victory(Player.White, self.state):
            return True, Player.White

        if nutils.num_empty_fields_around_neutron(self.state) == 0:
            return True, Player.White if self.curr_player != Player.White else Player.Black
        else:
            return False, None

    def move_piece(self, origin_x, origin_y, destination_x, destination_y):
        if(not can_move(origin_x, origin_y, destination_x, destination_y)):
            return False

        self.state[origin_x][origin_y], self.state[destination_x][destination_y] = self.state[destination_x][destination_y], self.state[origin_x][origin_y]

        if self.turn == Turn.Pawn:
            self.curr_player = Player.White if self.curr_player != Player.White else Player.Black

            self.turn = Turn.Neutron
        else:
            self.turn = Turn.Pawn

        return True

    def can_move(self, origin_x, origin_y, destination_x, destination_y):
        if (origin_x < 0 or origin_x >= self.size
            or origin_y < 0 or origin_y >= self.size
            or destination_x < 0 or destination_x >= self.size
            or destination_y < 0 or destination_y >= self.size):
            return False
        
        if(origin_x == destination_x and origin_y == destination_y):
            return False

        if self.turn == Turn.Neutron and self.state[origin_x][origin_y] != "N":
            return False

        if self.turn == Turn.Pawn and self.curr_player == Player.White and self.state[origin_x][origin_y] != "W":
            return False

        if self.turn == Turn.Pawn and self.curr_player == Player.Black and self.state[origin_x][origin_y] != "B":
            return False

        if self.state[destination_x][destination_y] != "0":
            return False

        diff_x = abs(destination_x - origin_x)
        diff_y = abs(destination_y - origin_y)

        if(not (diff_x == diff_y and diff_x != 0
                or diff_x == 0
                or diff_y == 0)):
            return False

        forwards_x = True
        forwards_y = True

        if destination_x < origin_x:
            forwards_x = False

        if destination_y < origin_y:
            forwards_y = False

        aux_x = origin_x
        next_x = origin_x
        aux_y = origin_y
        next_y = origin_y

        hit = False

        while(not hit):
            aux_x = next_x
            aux_y = next_y

            if(diff_x != 0):
                if(forwards_x):
                    next_x = aux_x + 1
                else:
                    next_x = aux_x - 1

            if(diff_y != 0):
                if(forwards_y):
                    next_y = aux_y + 1
                else:
                    next_y = aux_y - 1

            if(next_x < 0 or next_x >= self.size
                or next_y < 0 or next_y >= self.size):
                hit = True
            elif(self.state[next_x][next_y] != "0"):
                hit = True

        if(aux_x != destination_x or aux_y != destination_y):
            return False

        return True

    def draw_board(self):

        print(" ", end=" ")

        for i in range(1, self.size + 1):
            print(i, end=" ")

        print("\n", end="")

        for i in range(0, self.size):
            print(chr(65 + i), end=" ")

            for j in range(0, len(self.state[i])):
                print(self.state[i][j], end=" ")

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
