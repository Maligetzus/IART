import Neutron_gym
from gym import spaces
import numpy as np
from Neutron_gym.envs.Game.neutron import Neutron
from Neutron_gym.envs.Game.neutron import *

class NeutronEnv(gym.Env):
    def __init__(self, board_type, player):
        self.player = player
        self.board_type = board_type
        self.game = Neutron(board_type, curr_player=player)
        self.observation_space = spaces.Box(0, 3, (game.size, game.size), np.int32)
        self.action_space = spaces.Discrete(game.size * 8)

    def reset(self):
        self.game = Neutron(board_type)
        return self.__encode_state__()

    def step(self, action):
        # TODO: decode action to move
        # self.game.move_piece(origin_x, origin_y, direction)
        
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