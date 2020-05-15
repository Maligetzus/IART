import random
import gym
import numpy as np
import NeutronRL.envs.neutron_env

class QLearning():

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
                render=False):

        self.render = render

        self.env = gym.make(env)

        action_size_aux = tuple((self.env.action_space.high - self.env.action_space.low + np.ones(self.env.action_space.shape)).astype(int))

        self.action_size = 1

        for num in action_size_aux:
            self.action_size *= num

        print(f"Action size = {self.action_size}")
    
        self.qtable = { }

        self.max_episodes = max_episodes # Total episodes
        self.learning_rate = learning_rate  # Learning rate
        self.max_steps = max_steps  # Max steps per episode
        self.gamma = gamma  # Discounting rate

        # Exploration
        self.starting_epsilon = starting_epsilon
        self.max_epsilon = max_epsilon
        self.min_epsilon = min_epsilon
        self.decay_rate = decay_rate

    def train(self):
        epsilon = self.starting_epsilon
        rewards = []

        for current_episode in range(self.max_episodes):
            print(f"Episode {current_episode}")

            step = 0
            done = False
            total_rewards = 0

            state = self.env.reset()

            if state not in self.qtable:
                self.qtable[state] = np.zeros(self.action_size)

            for step in range(self.max_steps):
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

    
    def print_qtable(self):
        for key in self.qtable:
            print(f"{key}: [", end="")
            
            for value in self.qtable[key]:
                if value != 0:
                    action = np.where(self.qtable[key] == value)
                    print(f"{action[0][0]}: {value}", end=" ")

            print("]", end="\n")