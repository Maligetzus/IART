import gym
import random
import numpy as np
from NeutronGame.neutron_util import RenderMode, Turn, Direction, Tile, Player, BoardTypes, get_next_move
from NeutronGame.neutron import Neutron
from enum import Enum

class Opponent(Enum):
    Random = "random"
    Easy = "easy"

class NeutronEnv(gym.Env):
    def __init__(self, board_type=BoardTypes.Board_5X5, player=Player.White, opponent=Opponent.Random):
        self.log = False
        self.player = player
        self.opponent = opponent
        self.board_type = board_type
        self.render_mode = RenderMode.Ascii
        self.game = Neutron(self.board_type, render_mode=self.render_mode)

        # 0 = Blank Tile
        # 1 = White Pawn
        # 2 = Black Pawn
        # 3 = Neutron
        self.observation_space = gym.spaces.Box(low=0, high=3, shape=(self.game.size, self.game.size), dtype=np.int32)
        
        # [NeutronDirection, PawnNumber, PawnDirection]
        self.action_space = gym.spaces.Box(low=np.array([0, 0, 0]), high=np.array([7, 4, 7]), dtype=np.int32)
        
        self.game.start()

        # To encode the actions into integer
        self.encoding_factors = [len(Direction), self.game.size, len(Direction)]

    def reset(self):
        self.game = Neutron(self.board_type, render_mode=self.render_mode)
        self.game.start()

        if self.game.curr_player != self.player:
            if self.opponent == Opponent.Random:
                self.__random_play__()

        return self.__encode_state__()

    def step(self, action):
        success_play = True
        ended = False

        if self.game.curr_player == self.player:
            # Moves Neutron
            if self.game.turn == Turn.Neutron:
                neutron_pos = self.game.neutron_position

                success_play = self.game.move_piece(neutron_pos[0], neutron_pos[1], Direction(action[0]))

                if success_play:
                    # Check if neutron move has finished the game before proceeding
                    ended, winner = self.game.has_finished()

            # Moves Pawn
            if success_play and not ended:
                state = self.game.state

                pawn_coor_x = -1
                pawn_coor_y = -1
                pawn_num = action[1]
                pawn = Tile.White if self.player == Player.White else Tile.Black

                counter = -1

                for i in range(len(state)):
                    for j in range(len(state[i])):
                        if state[i][j] == pawn:
                            counter += 1

                            if counter == pawn_num:
                                pawn_coor_x = i
                                pawn_coor_y = j

                success_play = self.game.move_piece(pawn_coor_x, pawn_coor_y, Direction(action[2]))

        if success_play:
            self.__log__(f"Player play successful: neutron {Direction(action[0]).name} and pawn num {action[1]} {Direction(action[2]).name}")
        else:
            self.__log__(f"Player play failed: neutron {Direction(action[0]).name} and pawn num {action[1]} {Direction(action[2]).name}")

        # Check if player move has finished the game before proceeding
        ended, winner = self.game.has_finished()

        # Bot play
        if success_play and not ended:
            self.__log__("Opponent will play")

            if self.opponent == Opponent.Random:
                self.__random_play__()
            elif self.opponent == Opponent.Easy:
                self.__easy_play__()
            
            self.__log__("Opponent played")

            # Check if bot move has finished the game
            ended, winner = self.game.has_finished()

        # Encode state to int value, so it can be stored in the q-table
        obs = self.__encode_state__()

        if ended:
            if winner == self.player:
                reward = 1
            else:
                reward = -1
        else:
            if success_play:
                reward = 0
            else:
                # Returns -100 reward for invalid moves
                reward = -100

        done = ended

        return obs, reward, done, {}

    def render(self, mode='human', close=False):
        self.game.render()

    def set_logging(self, log):
        self.log = log

    # Encode state to int value, so it can be stored in the q-table
    def __encode_state__(self):
        ind = 0
        weight = 0

        for i in range(len(self.game.state)):
            for j in range(len(self.game.state[i])):
                ind += self.game.state[i][j].value * (4**weight)
                weight += 1

        return ind

    # Encode action to int value, so it can be accessed in the q-table
    def encode_action(self, action):    
        res = 0
        for i in range(3):
            res = res * self.encoding_factors[i] + action[i]

        return res

    # Decode action from int value
    def decode_action(self, action_index):
        res = np.zeros(3)
        for i in range(2, -1, -1):
            res[i] = action_index % self.encoding_factors[i]
            action_index = action_index // self.encoding_factors[i]

        return tuple((res).astype(int))

    # Random bot play
    # Makes a random play
    # If it makes an invalid move, just tries again until it makes a valid move
    def __random_play__(self):
        success_play = True

        # Move Neutron
        if self.game.turn == Turn.Neutron:
            success_play = False
            self.__log__("\tBot will move neutron")
            
            neutron_move = None
            neutron_pos = self.game.neutron_position

            while not success_play:
                neutron_move = Direction(random.randint(0,7))
                success_play = self.game.move_piece(neutron_pos[0], neutron_pos[1], neutron_move)

            self.__log__(f"\tBot moved neutron ({neutron_move.name})")

        state = self.game.state
        pawn = Tile.Black if self.player == Player.White else Tile.White

        # Check if neutron move has finished the game before proceeding
        ended, winner = self.game.has_finished()

        # Move pawn
        if success_play and not ended:

            success_play = False

            pawn_move = None
            pawn_num = None

            self.__log__("\tBot will move piece")

            while not success_play:

                pawn_coor_x = -1
                pawn_coor_y = -1
                pawn_num = random.randint(0,4)

                counter = -1

                for i in range(len(state)):
                    for j in range(len(state[i])):
                        if state[i][j] == pawn:
                            counter += 1

                            if counter == pawn_num:
                                pawn_coor_x = i
                                pawn_coor_y = j

                pawn_move = Direction(random.randint(0,7))
                success_play = self.game.move_piece(pawn_coor_x, pawn_coor_y, pawn_move)
        
            self.__log__(f"\tBot moved piece (num {pawn_num}, {pawn_move.name})")

    # Easy bot play
    # Uses minimax to calculate its next action
    def __easy_play__(self):
        success_play = False

        neutronMove, pawnCoord, pawnMove = get_next_move(self.game, 1, 2)

        self.__log__("Will move neutron")

        # Move Neutron
        if self.game.turn == Turn.Neutron:
            neutron_pos = self.game.neutron_position

            success_play = self.game.move_piece(neutron_pos[0], neutron_pos[1], neutronMove)

        self.__log__("Neutron moved")

        # Check if neutron move has finished the game before proceeding
        ended, winner = self.game.has_finished()

        # Move Pawn
        if not ended:
            self.__log__("Will move piece")

            success_play = self.game.move_piece(pawnCoord[0], pawnCoord[1], pawnMove)
        
            self.__log__("Piece moved")

    def __log__(self, text, end="\n"):
        if self.log:
            print(text, end=end)