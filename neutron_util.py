from enum import Enum

seenStates = set()


class BoardTypes(Enum):
    Board_5X5 = 1
    Board_7X7 = 2


class Player(Enum):
    White = "White"
    Black = "Black"


class Turn(Enum):
    Neutron = "Neutron"
    Pawn = "Pawn"


class Direction(Enum):
    Up = 0  #MovYPos
    Down = 1  #MovYNeg
    Left = 2  #MovXNeg
    Right = 3  #MovXPos
    LeftUp = 4  #MovXNegYPos
    RightUp = 5  #MovXPosYPos
    LeftDown = 6  #MovXNegYNeg
    RightDown = 7  #MovXPosYNeg


class Tile(Enum):
    Empty = 0
    Black = 1
    White = 2
    Neutron = 3


class Node:

    def __init__(self, game=None, neutronMove=None, pawnCoord=None, pawnMove=None, children=None, value=None):
        self.game = game
        self.neutronMove = neutronMove
        self.pawnCoord = pawnCoord
        self.pawnMove = pawnMove

        if children is not None:
            self.children = children
        else:
            self.children = []

        self.value = value

    def add_child(self, newNode):
        self.children.append(newNode)


def get_next_move(game, level, max_depth):
    head = Node(game=game)

    value = minimax(head, game.curr_player, level, max_depth)

    for child in head.children:
        if child.value == value:
            return child.neutronMove, child.pawnCoord, child.pawnMove


def minimax(node, player, level, max_depth, depth=0, maximum=True, alpha=-1000, beta=1000):
    player_tile = Tile.White if node.game.curr_player == Player.White else Tile.Black
    
    if victory_player(player, node.game.state):
        return 999 - depth
    elif victory_opponent(player, node.game.state) or num_empty_fields_around_neutron(node.game.state, node.game.neutron_position) == 0:
        return -999 + depth        
    elif depth == max_depth:
        return get_score(player, node.game.state, node.game.neutron_position)

    value = -1000 if maximum else 1000

    for direction_neutron in Direction:

        if node.game.turn != Turn.Neutron:
            direction_neutron = None
            newGame_neutron = node.game
            success = True
        else:
            success, newGame_neutron = node.game.hypothetical_move_piece(node.game.neutron_position[0], node.game.neutron_position[1], direction_neutron)

        # TODO: check if neutron move causes victory

        if success:
            # Check if neutron move is enough for victory
            # If so, the pawn move will be ignored
            finished, aux = newGame_neutron.has_finished()

            pawn_count = 0

            for i in range(newGame_neutron.size):
                for j in range(newGame_neutron.size):
                    if newGame_neutron.state[i][j] == player_tile or finished:
                        pawn_count += 1

                        for direction_pawn in Direction:
                            if finished:
                                direction_pawn = None
                                newGame_pawn = newGame_neutron
                                success = True
                            else:
                                success, newGame_pawn = newGame_neutron.hypothetical_move_piece(i, j, direction_pawn)

                            if(success):

                                # hash_state = newGame_pawn.hash_state()

                                # if not seenStates.__contains__(hash_state):
                                #     seenStates.add(hash_state)
                                
                                newNode = Node(game=newGame_pawn, neutronMove=direction_neutron, pawnCoord=(i, j), pawnMove=direction_pawn)

                                newValueMinimax = minimax(newNode, player, level, max_depth, depth + 1, not maximum, alpha, beta)

                                if maximum:
                                    newValue = max(value, newValueMinimax)
                                    alpha = max(alpha, newValue)
                                else:
                                    newValue = min(value, newValueMinimax)
                                    beta = min(beta, newValue)

                                newNode.value = newValue
                                node.add_child(newNode)

                                value = newValue

                                if alpha >= beta:
                                    break

                                if finished:
                                    break

                        if alpha >= beta:
                            break

                        if pawn_count == node.game.size:
                            break

                        if finished:
                            break

                if alpha >= beta:
                    break

                if pawn_count == node.game.size:
                    break

                if finished:
                    break

        if node.game.turn != Turn.Neutron:
            break

        if alpha >= beta:
            break

    return value


def get_score(curr_player, state, neutron_position):
    return 10 * num_empty_tiles_player(curr_player, state) - 10 * num_empty_tiles_opponent(curr_player, state) +\
           200 * neutron_to_player(curr_player, state, neutron_position) - 200 * neutron_to_opponent(curr_player, state, neutron_position) +\
           10 * odd(state, neutron_position) * (8 - num_empty_fields_around_neutron(state, neutron_position))


def num_empty_tiles_player(curr_player, state):
    return __num_empty_tiles(curr_player, state)


def num_empty_tiles_opponent(curr_player, state):
    return __num_empty_tiles(Player.White if curr_player == Player.Black else Player.Black, state)


def neutron_to_player(curr_player, state, neutron_position):
    return __neutron_to(curr_player, state, neutron_position)


def neutron_to_opponent(curr_player, state, neutron_position):
    return __neutron_to(Player.White if curr_player == Player.Black else Player.Black, state, neutron_position)


def num_empty_fields_around_neutron(state, neutron_position):
    counter = 0

    x, y = neutron_position
    
    left = True
    right = True
    up = True
    down = True

    if x == len(state) - 1:
        down = False
    if x == 0:
        up = False
    if y == len(state) - 1:
        right = False
    if y == 0:
        left = False

    if left and up and state[x - 1][y - 1] == Tile.Empty:
        counter += 1
    if up and state[x - 1][y] == Tile.Empty:
        counter += 1
    if up and right and state[x - 1][y + 1] == Tile.Empty:
        counter += 1
    if left and state[x][y - 1] == Tile.Empty:
        counter += 1
    if right and state[x][y + 1] == Tile.Empty:
        counter += 1
    if down and left and state[x + 1][y - 1] == Tile.Empty:
        counter += 1
    if down and state[x + 1][y] == Tile.Empty:
        counter += 1
    if down and right and state[x + 1][y + 1] == Tile.Empty:
        counter += 1

    return counter


def odd(state, neutron_position):
    if num_empty_fields_around_neutron(state, neutron_position) % 2 == 0:
        return -1
    else:
        return 1


def victory_player(curr_player, state):
    return victory(curr_player, state)


def victory_opponent(curr_player, state):
    return victory(Player.White if curr_player == Player.Black else Player.Black, state)


def __num_empty_tiles(player, state):
    counter = 0
    if player == Player.Black:
        for tile in state[0]:
            if tile == Tile.Empty:
                counter += 1
    else:
        for tile in state[len(state) - 1]:
            if tile == Tile.Empty:
                counter += 1

    return counter


def __neutron_to(player, state, neutron_position):
    counter = 0

    neutron_x, neutron_y = neutron_position

    diff_x = -1
    diff_y = -1

    if player == Player.Black:
        diff_x = neutron_x
    else:
        diff_x = abs(len(state) - 1 - neutron_x)
    
    up = True
    diag_left = True if neutron_y >= diff_x else False
    diag_right = True if len(state[0]) - 1 - neutron_y >= diff_x else False

    for i in range(1, diff_x + 1):
        if up:
            if state[neutron_x - i if player == Player.Black else neutron_x + i][neutron_y] != Tile.Empty:
                up = False
        
        if diag_left:
            if state[neutron_x - i if player == Player.Black else neutron_x + i][neutron_y - i] != Tile.Empty:
                diag_left = False

        if diag_right:
            if state[neutron_x - i if player == Player.Black else neutron_x + i][neutron_y + i] != Tile.Empty:
                diag_right = False
            
        if not up and not diag_left and not diag_right:
            break

    if up:
        counter += 1

    if diag_left:
        counter += 1

    if diag_right:
        counter += 1

    return counter


def victory(player, state):
    if player == Player.Black:
        for tile in state[0]:
            if tile == Tile.Neutron:
                return 1
    elif player == Player.White:
        for tile in state[len(state) - 1]:
            if tile == Tile.Neutron:
                return 1
    return 0
