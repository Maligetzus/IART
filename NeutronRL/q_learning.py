import random
import gym
import numpy as np
import NeutronRL.envs.neutron_env
from NeutronRL.env_algorithm import EnvAlgorithm

class QLearning(EnvAlgorithm):

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
                render=False,
                log=True,
                log_detail=False):

        super().__init__(env=env, max_episodes=max_episodes, learning_rate=learning_rate,
                        max_steps=max_steps, gamma=gamma, starting_epsilon=starting_epsilon,
                        max_epsilon=max_epsilon, min_epsilon=min_epsilon, render=render, log=log, log_detail=log_detail)

        self.decay_rate = decay_rate

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

            for step in range(self.max_steps):
                if self.log:
                    print(f"Step {step}")

                exp_exp_tradeoff = random.uniform(0, 1)

                if exp_exp_tradeoff > epsilon:
                    action_ind = np.argmax(self.qtable[state])
                    action = self.env.decode_action(action_ind)
                else:
                    action = self.env.action_space.sample()
                    action_ind = self.env.encode_action(action)

                new_state, reward, done, info = self.env.step(action)

                if new_state not in self.qtable:
                    self.qtable[new_state] = np.zeros(self.action_size)

                self.qtable[state][action_ind] = self.qtable[state][action_ind] + self.learning_rate * (reward + self.gamma * np.max(self.qtable[new_state]) - self.qtable[state][action_ind])

                total_rewards += reward
                state = new_state

                if self.render:
                    self.env.render()

                if done:
                    break

            # Reduce epsilon (because we need less and less exploration)
            epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon) * np.exp(-self.decay_rate * current_episode)
            rewards.append(total_rewards)

        print("Score over time: " + str(sum(rewards)/self.max_episodes))