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
        self.game = Neutron(self.board_type, curr_player=player, render_mode=self.render_mode)
        self.observation_space = gym.spaces.Box(low=0, high=3, shape=(self.game.size, self.game.size), dtype=np.int32)
        self.action_space = gym.spaces.Box(low=np.array([0, 0, 0]), high=np.array([7, 4, 7]), dtype=np.int32)
        
        self.game.start()

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

        if self.game.curr_player == self.player:
            if self.game.turn == Turn.Neutron:
                neutron_pos = self.game.neutron_position

                success_play = self.game.move_piece(neutron_pos[0], neutron_pos[1], Direction(action[0]))

            if success_play:
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

        ended, winner = self.game.has_finished()

        if success_play and not ended:
            self.__log__("Opponent play")

            if self.opponent == Opponent.Random:
                self.__random_play__()
            elif self.opponent == Opponent.Easy:
                self.__easy_play__()
            
            self.__log__("Opponent played")

            ended, winner = self.game.has_finished()

        obs = self.__encode_state__()

        if ended:
            if winner == self.player:
                reward = 1
            else:
                reward = -1
        else:
            reward = 0

        done = ended

        return obs, reward, done, {}

    def render(self, mode='human', close=False):
        self.game.render()

    def set_logging(self, log):
        self.log = log

    def __encode_state__(self):
        ind = 0
        weight = 0

        for i in range(len(self.game.state)):
            for j in range(len(self.game.state[i])):
                ind += self.game.state[i][j].value * (4**weight)
                weight += 1

        return ind

    def encode_action(self, action):    
        res = 0
        for i in range(3):
            res = res * self.encoding_factors[i] + action[i]

        return res

    def decode_action(self, action_index):
        res = np.zeros(3)
        for i in range(2, -1, -1):
            res[i] = action_index % self.encoding_factors[i]
            action_index = action_index // self.encoding_factors[i]

        return tuple((res).astype(int))

    def __random_play__(self):
        success_play = False

        self.__log__("Will move neutron")

        if self.game.turn == Turn.Neutron:
            neutron_pos = self.game.neutron_position

            while not success_play:
                success_play = self.game.move_piece(neutron_pos[0], neutron_pos[1], Direction(random.randint(0,7)))

        self.__log__("Neutron moved")

        state = self.game.state
        pawn = Tile.Black if self.player == Player.White else Tile.White

        self.__log__("Will move piece")

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

            success_play = self.game.move_piece(pawn_coor_x, pawn_coor_y, Direction(random.randint(0,7)))
        
        self.__log__("Piece moved")

    def __easy_play__(self):
        success_play = False

        neutronMove, pawnCoord, pawnMove = get_next_move(self.game, 1, 2)

        if pawnCoord == None:
            print("FUCK")

        self.__log__("Will move neutron")

        if self.game.turn == Turn.Neutron:
            neutron_pos = self.game.neutron_position

            while not success_play:
                success_play = self.game.move_piece(neutron_pos[0], neutron_pos[1], neutronMove)

        self.__log__("Neutron moved")

        self.__log__("Will move piece")

        while not success_play:
            success_play = self.game.move_piece(pawnCoord[0], pawnCoord[1], pawnMove)
        
        self.__log__("Piece moved")

    def __log__(self, text, end="\n"):
        if self.log:
            print(text, end=end)