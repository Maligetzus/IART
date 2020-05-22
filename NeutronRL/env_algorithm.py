import random
import gym
import numpy as np
import NeutronRL.envs.neutron_env
from enum import Enum

class EpsilonDecay(Enum):
    Exponential = "exp"
    Linear = "linear"
    NoDecay = "none"

class EnvAlgorithm():

    def __init__(self,
                env="Neutron-5x5-White-Easy-v0",
                max_episodes=100,
                learning_rate=0.8,
                max_steps=99,
                gamma=0.95,
                starting_epsilon=0.1,
                max_epsilon=1.0,
                min_epsilon=0.01,
                decay_rate=0.001,
                epsilon_decay=EpsilonDecay.Exponential,
                render=False,
                log=True,
                log_detail=False,
                plot_rewards=False):

        self.render = render
        self.plot_rewards = plot_rewards

        self.env = gym.make(env)

        self.env.set_logging(log_detail)
        self.log = log

        action_size_aux = tuple((self.env.action_space.high - self.env.action_space.low + np.ones(self.env.action_space.shape)).astype(int))

        self.action_size = 1

        for num in action_size_aux:
            self.action_size *= num

        if self.log:
            print(f"Action size = {self.action_size}")
    
        self.reset_qtable()

        self.max_episodes = max_episodes # Total episodes
        self.learning_rate = learning_rate  # Learning rate
        self.max_steps = max_steps  # Max steps per episode
        self.gamma = gamma  # Discounting rate

        # Exploration
        self.starting_epsilon = starting_epsilon
        self.max_epsilon = max_epsilon
        self.min_epsilon = min_epsilon
        self.decay_rate = decay_rate
        self.epsilon_decay = epsilon_decay
    
    def print_qtable(self):
        for key in self.qtable:
            print(f"{key}: [", end="")
            
            for value in self.qtable[key]:
                if value != 0:
                    action = np.where(self.qtable[key] == value)
                    print(f"{action[0][0]}: {value}", end=" ")

            print("]", end="\n")

    def reset_qtable(self):
        self.qtable = { }

    def import_qtable(self, qtable):
        self.qtable = qtable

    def export_qtable(self):
        return self.qtable