import gym
import random
import numpy as np
from NeutronGame.neutron_util import RenderMode, Turn, Direction, Tile, Player, BoardTypes
from NeutronGame.neutron import Neutron
from enum import Enum

class Opponent(Enum):
    Random = "random"

class NeutronEnv(gym.Env):
    def __init__(self, board_type=BoardTypes.Board_5X5, player=Player.White, opponent=Opponent.Random):
        self.player = player
        self.opponent = opponent
        self.board_type = board_type
        self.game = Neutron(board_type, curr_player=player, render_mode=RenderMode.Ascii)
        self.observation_space = gym.spaces.Box(low=0, high=3, shape=(self.game.size, self.game.size), dtype=np.int32)
        self.action_space = gym.spaces.Box(low=np.array([0, 1, 0]), high=np.array([7, 5, 7]), dtype=np.int32)

    def reset(self):
        self.game = Neutron(board_type)

        if self.game.curr_player != self.player:
            if self.opponent == Opponent.Random:
                self.__random_play__()

        return self.__encode_state__()

    def step(self, action):
        success_play = False

        if self.game.curr_player == self.player:
            success_play = True

            if self.game.turn == Turn.Neutron:
                neutron_pos = self.game.neutron_position

                success_play = self.game.move_piece(neutron_pos[0], neutron_pos[1], Direction(action[0]))

            if success_play:
                state = self.game.state

                pawn_coor_x = -1
                pawn_coor_y = -1
                pawn_num = action[1]
                pawn = Tile.White if self.player == Player.White else Tile.Black

                counter = 0

                for i in range(len(state)):
                    for j in range(len(state[i])):
                        if state[i][j] == pawn:
                            counter += 1

                            if counter == pawn_num:
                                pawn_coor_x = i
                                pawn_coor_y = j

                success_play = self.game.move_piece(pawn_coor_x, pawn_coor_y, Direction(action[2]))

        if self.opponent == Opponent.Random:
            self.__random_play__()
        
        obs = self.__encode_state__()

        ended, winner = self.game.has_finished

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

    def __encode_state__(self):
        ind = 0
        weight = 0

        for i in range(len(self.game.state)):
            for j in range(len(self.game.state[i])):
                ind += self.game.state[i][j] * (4**weight)
                weight += 1

        return ind

    def __random_play__(self):
        success_play = False

        if self.game.turn == Turn.Neutron:
            neutron_pos = self.game.neutron_position

            while not success_play:
                success_play = self.game.move_piece(neutron_pos[0], neutron_pos[1], Direction(random.randint(0,7)))

        state = self.game.state
        pawn = Tile.Black if self.player == Player.White else Tile.White

        while not success_play:
            pawn_coor_x = -1
            pawn_coor_y = -1
            pawn_num = random.randint(1,5)

            counter = 0

            for i in range(len(state)):
                for j in range(len(state[i])):
                    if state[i][j] == pawn:
                        counter += 1

                        if counter == pawn_num:
                            pawn_coor_x = i
                            pawn_coor_y = j

            success_play = self.game.move_piece(pawn_coor_x, pawn_coor_y, Direction(random.randint(0,7)))