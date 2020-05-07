import neutron_util as nutils
from neutron_util import Player, Turn, Direction, Tile, BoardTypes, RenderMode
import copy
from game_gui import GameGui
from animator import Animator


class Neutron:

    def __init__(self, board_type, curr_player=Player.White, turn=Turn.Neutron, state=None, neutron_position=(-1, -1), render_mode=RenderMode.Pygame):
        self.board_type = board_type
        if board_type == BoardTypes.Board_5X5:
            self.size = 5
        else:
            self.size = 7

        self.turn = turn    # Indicates which piece should be moved: neutron or pawn
        self.curr_player = curr_player
        self.state = state  # AKA Board
        self.neutron_position = neutron_position    # for easier access
        self.player_type = {'White': None, 'Black': None}   # indicates each player type (human, cpu, etc)
        self.animator = None
        self.render_mode = render_mode;

    # Initializes the game
    def start(self, starting_player=Player.White):
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

        if self.render_mode != RenderMode.Disabled:
            self.gui = GameGui(self, self.board_type, self.render_mode)
            if self.render_mode == RenderMode.Pygame:
                self.animator = Animator(self.gui)

        return True, "Successfuly started the game"

    # Checks if game as finished
    def has_finished(self):

        # Has Black won?
        if nutils.victory(Player.Black, self.state):
            return True, Player.Black

        # Has White won?
        if nutils.victory(Player.White, self.state):
            return True, Player.White

        # Is the neutron stuck?
        if nutils.num_empty_fields_around_neutron(self.state, self.neutron_position) == 0:
            return True, Player.White if self.curr_player != Player.White else Player.Black
        else:
            return False, None

    # Moves a piece
    def move_piece(self, origin_x, origin_y, direction):
        return self.__move_piece(self, origin_x, origin_y, direction)

    # Returns the new game state after moving a piece (doesn't change actual game state)
    def hypothetical_move_piece(self, origin_x, origin_y, direction):
        # Makes copy of the game and applies move
        game = Neutron(self.board_type, self.curr_player, self.turn, copy.deepcopy(self.state), self.neutron_position)

        success = self.__move_piece(game, origin_x, origin_y, direction)

        return success, game

    def render(self):
        self.gui.display()

    @staticmethod
    def __move_piece(self, origin_x, origin_y, direction):
        # Checks if the move is valid
        valid, destination_x, destination_y = self.can_move(origin_x, origin_y, direction)

        if not valid:
            return False

        origin_piece = self.state[origin_x][origin_y]

        # Updates the neutron position
        if origin_piece == Tile.Neutron:
            self.neutron_position = destination_x, destination_y


        self.state[origin_x][origin_y] = Tile.Empty

        #Move animation
        if self.animator != None:
            self.animator.animate_move(origin_piece, origin_y, origin_x, destination_y, destination_x, 0.5)

        self.state[destination_x][destination_y] = origin_piece

        # Next player and/or turn
        if self.turn == Turn.Pawn:
            self.curr_player = Player.White if self.curr_player != Player.White else Player.Black

            self.turn = Turn.Neutron
        else:
            self.turn = Turn.Pawn

        return True

    # Checks if a move is valid
    def can_move(self, origin_x, origin_y, direction):
        if (origin_x < 0 or origin_x >= self.size
                or origin_y < 0 or origin_y >= self.size):
            return False, origin_x, origin_y

        # Is the selected piece valid?
        if self.turn == Turn.Neutron and self.state[origin_x][origin_y] != Tile.Neutron:
            return False, origin_x, origin_y

        if self.turn == Turn.Pawn and self.curr_player == Player.White and self.state[origin_x][origin_y] != Tile.White:
            return False, origin_x, origin_y

        if self.turn == Turn.Pawn and self.curr_player == Player.Black and self.state[origin_x][origin_y] != Tile.Black:
            return False, origin_x, origin_y

        # These variables indicate how much the piece will move per increment in each coordinate
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

        # Moves piece until it hits a wall or other piece
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

        # Destination can't be the origin
        if aux_x == origin_x and aux_y == origin_y:
            return False, origin_x, origin_y

        return True, aux_x, aux_y

    # Prints the board in the console window
    def draw_board(self):

        print(" ", end=" ")

        for i in range(1, self.size + 1):
            print(i, end=" ")

        print("\n", end="")

        for i in range(0, self.size):
            print(chr(65 + i), end=" ")

            for j in range(0, len(self.state[i])):
                symbol = ""

                if self.state[i][j] == Tile.Empty:
                    symbol = "E"
                elif self.state[i][j] == Tile.White:
                    symbol = "W"
                elif self.state[i][j] == Tile.Black:
                    symbol = "B"
                else:
                    symbol = "N"

                print(symbol, end=" ")

            print("\n", end="")

        print("\n", end="")

    def hash_state(self):
        result = 0
        current_prime = 1
        for i in range(0, self.size):
            for j in range(0, self.size):
                result += self.state[i][j].value * current_prime
                current_prime = self.__find_next_prime(current_prime)
        return result

    @staticmethod
    def __find_next_prime(n):
        a = n
        b = 2*n
        for p in range(a, b):
            for i in range(2, p):
                if p % i == 0:
                    break
            else:
                return p

    @staticmethod
    def square_to_index(square):
        x = -1
        y = -1

        if len(square) != 2:
            return x, y

        x = ord(square[0].upper()) - ord('A')

        y = int(square[1]) - 1

        return x, y
