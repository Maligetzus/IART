from enum import Enum
import time
import random

seenStates = set()


# Enum that denotes the size of the board.
class BoardTypes(Enum):
    Board_5X5 = "5x5 Board"
    Board_7X7 = "7x7 Board"


# Enum that denotes types of players in the game.
class PlayerTypes(Enum):
    Player = "Player"
    CpuGreedy = "CPU (Greedy)"
    CpuL0 = "CPU (lvl 0)"
    CpuL1 = "CPU (lvl 1)"
    CpuL2 = "CPU (lvl 2)"
    CpuL3 = "CPU (lvl 3)"
    CpuRandom = "CPU (RandM)"
    CpuOrdered = "CPU (OrdM)"


# Enum the player colour.
class Player(Enum):
    White = "White"
    Black = "Black"


# Enum that denotes the turn kind.
class Turn(Enum):
    Neutron = "Neutron"
    Pawn = "Pawn"


# Enum that denotes the turn directions.
class Direction(Enum):
    Up = 0  #MovYPos
    Down = 1  #MovYNeg
    Left = 2  #MovXNeg
    Right = 3  #MovXPos
    LeftUp = 4  #MovXNegYPos
    RightUp = 5  #MovXPosYPos
    LeftDown = 6  #MovXNegYNeg
    RightDown = 7  #MovXPosYNeg


# Enum that denotes the tile kind.
class Tile(Enum):
    Empty = 0
    Black = 1
    White = 2
    Neutron = 3


# Class that represents the minimax tree node.
class Node:

    # Method
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


# Function that returns the next move to be executed.
def get_next_move(game, heuristic, max_depth):
    head = Node(game=game)

    value = minimax_alpha_beta_pruning(head, game.curr_player, heuristic, max_depth)

    for child in head.children:
        if child.value == value:
            return child.neutronMove, child.pawnCoord, child.pawnMove

# Function that returns the next move to be executed, with the most likely to be best directions checked first
def get_next_move_ordered(game, heuristic, max_depth):
    head = Node(game=game)

    value = minimax_alpha_beta_pruning(head, game.curr_player, heuristic, max_depth, first_directions=True)

    for child in head.children:
        if child.value == value:
            return child.neutronMove, child.pawnCoord, child.pawnMove

# Function that returns the next move to be executed (picks a random one from all the best)
def get_next_move_random(game, heuristic, max_depth):
    head = Node(game=game)

    value = minimax_alpha_beta_pruning(head, game.curr_player, heuristic, max_depth, multiple_moves=True)

    possibleChildren = []

    for i in range(len(head.children)):
        if head.children[i].value == value:
            possibleChildren.append(i)
            print(head.children[i].neutronMove)

    chosenChildIndex = possibleChildren[random.randint(0, len(possibleChildren) - 1)]
    chosenChild = head.children[chosenChildIndex]

    print(chosenChild.neutronMove)
    print(chosenChild.pawnCoord)
    print(chosenChild.pawnMove)

    return chosenChild.neutronMove, chosenChild.pawnCoord, chosenChild.pawnMove


# Function that contains the minimax algorithm with alpha beta pruning.
def minimax_alpha_beta_pruning(node, player, heuristic, max_depth, multiple_moves=False, first_directions=False, depth=0, maximum=True, alpha=-1000, beta=1000):
    player_tile = Tile.White if node.game.curr_player == Player.White else Tile.Black
    
    if victory_player(player, node.game.state):
        return 999 - depth
    elif victory_opponent(player, node.game.state) or num_empty_fields_around_neutron(node.game.state, node.game.neutron_position) == 0:
        return -999 + depth        
    elif depth == max_depth:
        return get_score(heuristic, player, node.game.state, node.game.neutron_position)

    value = -1000 if maximum else 1000

    directions = []

    for direction in Direction:

        if first_directions and\
            (node.game.curr_player == Player.White and (direction == Direction.LeftDown or direction == Direction.RightDown or direction == Direction.Down)) or\
            (node.game.curr_player == Player.Black and (direction == Direction.LeftUp or direction == Direction.RightUp or direction == Direction.Up)):
            directions.insert(0, direction)
        else:
            directions.append(direction)

    for direction_neutron in directions:

        if node.game.turn != Turn.Neutron:
            direction_neutron = None
            newGame_neutron = node.game
            success = True
        else:
            success, newGame_neutron = node.game.hypothetical_move_piece(node.game.neutron_position[0], node.game.neutron_position[1], direction_neutron)

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

                                newValueMinimax = minimax_alpha_beta_pruning(newNode, player, heuristic, max_depth, multiple_moves, first_directions, depth + 1, not maximum, alpha, beta)

                                newNode.value = newValueMinimax
                                node.add_child(newNode)

                                if maximum:
                                    value = max(value, newValueMinimax)
                                    alpha = max(alpha, value)
                                else:
                                    value = min(value, newValueMinimax)
                                    beta = min(beta, value)

                                if alpha == beta and not multiple_moves or alpha > beta:
                                    break

                                if finished:
                                    break

                        if alpha == beta and not multiple_moves or alpha > beta:
                            break

                        if pawn_count == node.game.size:
                            break

                        if finished:
                            break

                if alpha == beta and not multiple_moves or alpha > beta:
                    break

                if pawn_count == node.game.size:
                    break

                if finished:
                    break

        if node.game.turn != Turn.Neutron:
            break

        if alpha == beta and not multiple_moves or alpha > beta:
            break

    return value


# Function that returns the values of a give heuistic.
def get_score(heuristic, curr_player, state, neutron_position):
    if heuristic == 3:
        return 10 * num_empty_tiles_player(curr_player, state) - 10 * num_empty_tiles_opponent(curr_player, state) +\
           200 * neutron_to_player(curr_player, state, neutron_position) - 200 * neutron_to_opponent(curr_player, state, neutron_position) +\
           10 * odd(state, neutron_position) * (8 - num_empty_fields_around_neutron(state, neutron_position))
    elif heuristic == 2:
        return 10 * num_empty_tiles_player(curr_player, state) - 10 * num_empty_tiles_opponent(curr_player, state) +\
           10 * odd(state, neutron_position) * (8 - num_empty_fields_around_neutron(state, neutron_position))
    elif heuristic == 1:
        return neutron_to_player(curr_player, state, neutron_position) - neutron_to_opponent(curr_player, state, neutron_position)
    else:
        return 0


# Function returns the number of empty tiles in the current player's back row.
def num_empty_tiles_player(curr_player, state):
    return __num_empty_tiles(curr_player, state)


# Function returns the number of empty tiles in the opposing player's back row.
def num_empty_tiles_opponent(curr_player, state):
    return __num_empty_tiles(Player.White if curr_player == Player.Black else Player.Black, state)


# Function returns if the neutron has a path to the current player's victory in the next turn.
def neutron_to_player(curr_player, state, neutron_position):
    return __neutron_to(curr_player, state, neutron_position)


# Function returns if the neutron has a path to an opposing player's victory in the next turn.
def neutron_to_opponent(curr_player, state, neutron_position):
    return __neutron_to(Player.White if curr_player == Player.Black else Player.Black, state, neutron_position)


# Function returns the number of empty field around neutron.
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


# Function returns if the method num_empty_fields_around_neutron returns an odd number.
def odd(state, neutron_position):
    if num_empty_fields_around_neutron(state, neutron_position) % 2 == 0:
        return -1
    else:
        return 1


# Function returns if the victory condition was met by the current player.
def victory_player(curr_player, state):
    return victory(curr_player, state)


# Function returns if the victory condition was met by the opposing player.
def victory_opponent(curr_player, state):
    return victory(Player.White if curr_player == Player.Black else Player.Black, state)


# Function returns the number of empty tiles in a player's back row.
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


# Function returns if the neutron has a path to a player's victory in the next turn.
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


# Function returns if the victory condition was met by a given player.
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


# Function that returns current time in miliseconds.
def get_time_miliseconds():
    return int(round(time.time() * 1000))
