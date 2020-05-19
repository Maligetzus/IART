import random
import gym
import numpy as np
import NeutronRL.envs.neutron_env
from NeutronRL.env_algorithm import EnvAlgorithm

class SARSA(EnvAlgorithm):

    def train(self):
        epsilon = self.starting_epsilon
        rewards = []

        for current_episode in range(self.max_episodes):
            if self.log:
                print(f"Episode {current_episode}")

            step = 0
            done = False
            total_rewards = 0

            state = self.env.reset()

            if state not in self.qtable:
                self.qtable[state] = np.zeros(self.action_size)

            action_ind, action = self.__get_action__(epsilon, state)

            for step in range(self.max_steps):
                if self.log:
                    print(f"Step {step}")

                new_state, reward, done, info = self.env.step(action)

                if new_state not in self.qtable:
                    self.qtable[new_state] = np.zeros(self.action_size)

                new_action_ind, new_action = self.__get_action__(epsilon, state)

                self.qtable[state][action_ind] = self.qtable[state][action_ind] + self.learning_rate * (reward + self.gamma * self.qtable[new_state][new_action_ind] - self.qtable[state][action_ind])

                total_rewards += reward
                state = new_state
                action_ind = new_action_ind
                action = new_action

                if self.render:
                    self.env.render()

                if done:
                    break

            # Reduce epsilon (because we need less and less exploration)
            epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon) * np.exp(-self.decay_rate * current_episode)
            rewards.append(total_rewards)

        print("Score over time: " + str(sum(rewards)/self.max_episodes))

    def __get_action__(self, epsilon, state):
        exp_exp_tradeoff = random.uniform(0, 1)

        if exp_exp_tradeoff > epsilon:
            action_ind = np.argmax(self.qtable[state])
            action = self.env.decode_action(action_ind)
        else:
            action = self.env.action_space.sample()
            action_ind = self.env.encode_action(action)

        return action_ind, action
