class Neutron:

    def __init__(self, state, size, curr_player=None):
        self.size = size
        self.state = state
        self.curr_player = curr_player

    @staticmethod
    def get():
        print("Size of board:")

        size = 0

        while size < 3 and size % 2 == 0:
            size = int(input())

        state = []

        for i in range(0, size):
            row = []
            for j in range(0, size):
                if i == 0:
                    row.append("B")
                elif i == size / 2 and j == size / 2:
                    row.append("N")
                elif i == size - 1:
                    row.append("W")
                else:
                    row.append("0")
            state.append(row)

        return Neutron(size, state)

    def run(self):
        winner = None
        end = False
        self.curr_player = "White"
        step = 1

        while not end:
            if step == 2:
                curr_player = "White" if self.curr_player != "White" else "Black"

                step = 1
            else:
                step = 2

            self.draw_board()
            print(self.curr_player + " Player,", end="")
            print(" play Neutron" if step == 1 else " play piece", end="")
            print(" (ex.: E1 B1):")

            success = False

            while not success:

                move = input()

                success, new_state = self.play(self.curr_player, step, move)

                if not success:
                    print("Bad input!\n")
                else:
                    self.state = new_state

            end, winner = self.end_state()

        if winner is None:
            winner = self.curr_player

        print("Winner: " + winner)

    def play(self, player, step, move):
        squares = move.split(" ")

        if len(squares) != 2:
            return False, self.state

        piece_x, piece_y = self.square_to_index(squares[0])
        square_x, square_y = self.square_to_index(squares[1])

        if piece_x == -1 or piece_y == -1 or square_x == -1 or square_y == -1:
            return False, self.state

        if step == 1 and self.state[piece_x][piece_y] != "N":
            return False, self.state

        if step == 2 and player == "White" and self.state[piece_x][piece_y] != "W":
            return False, self.state

        if step == 2 and player == "Black" and self.state[piece_x][piece_y] != "B":
            return False, self.state

        if self.state[square_x][square_y] != "0":
            return False, self.state

        return self.move_piece(piece_x, piece_y, square_x, square_y)

    def move_piece(self, piece_x, piece_y, square_x, square_y):
        diff_x = abs(square_x - piece_x)
        diff_y = abs(square_y - piece_y)

        aux_x = piece_x
        aux_y = piece_y

        if diff_x == diff_y and diff_x != 0:
            forwards_x = True
            forwards_y = True

            if square_x < piece_x:
                forwards_x = False

            if square_y < piece_y:
                forwards_y = False

            if forwards_x:
                if forwards_y:
                    if square_x + 1 < self.size and square_y + 1 < self.size and self.state[square_x + 1][square_y + 1] == "0":
                        return False, self.state
                else:
                    if square_x + 1 < self.size and square_y - 1 >= 0 and self.state[square_x + 1][square_y - 1] == "0":
                        return False, self.state
            else:
                if forwards_y:
                    if square_x - 1 >= 0 and square_y + 1 < self.size and self.state[square_x - 1][square_y + 1] == "0":
                        return False, self.state
                else:
                    if square_x - 1 >= 0 and square_y - 1 >= 0 and self.state[square_x - 1][square_y - 1] == "0":
                        return False, self.state

            while aux_x != square_x and aux_y != square_y:
                if forwards_x:
                    aux_x += 1
                else:
                    aux_x -= 1

                if forwards_y:
                    aux_y += 1
                else:
                    aux_y -= 1

                if self.state[aux_x][aux_y] != "0":
                    return False, self.state
        elif diff_x == 0:
            forwards_y = True

            if square_y < piece_y:
                forwards_y = False

            if forwards_y:
                if square_y + 1 < self.size and self.state[square_x][square_y + 1] == "0":
                    return False, self.state
            else:
                if square_y - 1 >= 0 and self.state[square_x][square_y - 1] == "0":
                    return False, self.state

            while aux_y != square_y:
                if forwards_y:
                    aux_y += 1
                else:
                    aux_y -= 1

                if self.state[aux_x][aux_y] != "0":
                    return False, self.state
        elif diff_y == 0:
            forwards_x = True

            if square_x < piece_x:
                forwards_x = False

            if forwards_x:
                if square_x + 1 < self.size and self.state[square_x + 1][square_y] == "0":
                    return False, self.state
            else:
                if square_x - 1 >= 0 and self.state[square_x - 1][square_y] == "0":
                    return False, self.state

            while aux_x != square_x:

                if forwards_x:
                    aux_x += 1
                else:
                    aux_x -= 1

                if self.state[aux_x][aux_y] != "0":
                    return False, self.state
        else:
            return False, self.state

        self.state[piece_x][piece_y], self.state[square_x][square_y] = self.state[square_x][square_y], self.state[piece_x][piece_y]

        return True, self.state

    def end_state(self):
        n_x = -1
        n_y = -1

        found = False

        for i in range(0, self.size):
            for j in range(0, len(self.state[i])):
                if self.state[i][j] == "N":
                    n_x = i
                    n_y = j

                    found = True
                    break

            if found:
                break

        if n_x == 0:
            return True, "B"

        if n_x == self.size - 1:
            return True, "W"

        can_move = False

        for i in range(n_x - 1, n_x + 2):
            if i >= 0 and i < self.size:
                for j in range(n_y - 1, n_y + 2):
                    if j >= 0 and j < len(self.state[i]):
                        if self.state[i][j] == "0":
                            can_move = True
                            break

            if can_move:
                break

        if can_move:
            return False, None
        else:
            return True, None

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
    def square_to_index(self, square):
        x = -1
        y = -1

        if len(square) != 2:
            return x, y

        x = ord(square[0].upper()) - ord('A')

        y = int(square[1]) - 1

        return x, y
