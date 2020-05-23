import random
import gym
import numpy as np
import NeutronRL.envs.neutron_env
from NeutronRL.env_algorithm import EnvAlgorithm, EpsilonDecay


class EnvPlay():

    def __init__(self, qtable=None):
        self.qtable = qtable

    def play_multiple(self, env="Neutron-5x5-White-Random-v0", num_games=10, max_plays=2000, learn=False, log=False, log_games=False):
        unfinished = 0
        victories = 0
        defeats = 0

        for game in range(num_games):
            if log:
                print(f"Game {game + 1}")

            finished, victory = self.play(env, max_plays, learn, log_games)

            if finished:
                if victory:
                    victories += 1
                else:
                    defeats += 1
            else:
                unfinished += 1

        return victories, defeats, unfinished

    def play(self, env="Neutron-5x5-White-Random-v0", max_plays=2000, learn=False, log=False):
        if self.qtable == None:
            return False, False

        finished = False
        victory = False

        env = gym.make(env)

        action_size_aux = tuple((env.action_space.high - env.action_space.low + np.ones(env.action_space.shape)).astype(int))

        action_size = 1

        for num in action_size_aux:
            action_size *= num

        state = env.reset()

        for step in range(max_plays):
            if learn:
                if state not in self.qtable:
                    self.qtable[state] = np.zeros(action_size)
                
                action_ind = np.argmax(self.qtable[state])
            else:
                if state not in self.qtable:
                    action_ind = 0
                else:
                    action_ind = np.argmax(self.qtable[state])

            action = env.decode_action(action_ind)
            
            new_state, reward, done, info = env.step(action)

            if done:
                print("IT'S TRUE")

            if learn and reward == -100:
                self.qtable[state][action_ind] = reward

            if log:
                env.render()
            
            if done:
                finished = True
                
                if reward == 1:
                    victory = True
                    print("Victory! ", end="")
                else:
                    victory = False
                    print("Defeat! ", end="")

                print("Number of steps: ", step)
                break

            state = new_state

        if not finished:
            print("Didn't finish the game")

        return finished, victory

    def import_qtable(self, qtable):
        self.qtable = qtable

    def export_qtable(self):
        return self.qtable