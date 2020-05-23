import random
import gym
import numpy as np
import NeutronRL.envs.neutron_env
from NeutronRL.env_algorithm import EnvAlgorithm, EpsilonDecay


class QLearning(EnvAlgorithm):

    def train(self):
        invalid_episodes = 0
        epsilon = self.starting_epsilon
        aux_expsilon = epsilon
        rewards = []
        epsilons = []

        for current_episode in range(self.max_episodes):
            epsilons.append(epsilon)
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

                if reward != -100:
                    self.qtable[state][action_ind] = self.qtable[state][action_ind] + self.learning_rate * (reward + self.gamma * np.max(self.qtable[new_state]) - self.qtable[state][action_ind])

                    total_rewards += reward
                else:
                    self.qtable[state][action_ind] = reward

                state = new_state

                if self.render:
                    self.env.render()

                if done:
                    break

            # Reduce epsilon (because we need less and less exploration)
            if self.epsilon_decay == EpsilonDecay.Exponential:
                epsilon = self.ending_epsilon + (self.starting_epsilon - self.ending_epsilon) * np.exp(-self.decay_rate * current_episode)
            elif self.epsilon_decay == EpsilonDecay.Linear and aux_expsilon > 0:
                aux_expsilon = self.starting_epsilon + (self.starting_epsilon - self.ending_epsilon) * (-self.decay_rate * current_episode)

                if self.starting_epsilon > self.ending_epsilon:
                    if aux_expsilon > self.ending_epsilon:
                        epsilon = aux_expsilon
                else:
                    if aux_expsilon < self.ending_epsilon:
                        epsilon = aux_expsilon

            if total_rewards == 0:
                invalid_episodes += 1
            rewards.append(total_rewards)

        score = sum(rewards)/(self.max_episodes - invalid_episodes)

        print("Score over time: " + str(score))

        return score, rewards, epsilons