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
            # Keep track of the epsilons along the training for interpretation purposes
            epsilons.append(epsilon)

            if self.log:
                print(f"Episode {current_episode}")

            step = 0
            done = False
            total_rewards = 0

            # Gets initial state
            state = self.env.reset()

            # Adds state to Q-Table if it wasn't there yet
            if state not in self.qtable:
                self.qtable[state] = np.zeros(self.action_size)

            for step in range(self.max_steps):
                if self.log:
                    print(f"Step {step}")

                exp_exp_tradeoff = random.uniform(0, 1)
                
                # Picks the new action (randomly or from the q-table)
                if exp_exp_tradeoff > epsilon:
                    action_ind = np.argmax(self.qtable[state])
                    action = self.env.decode_action(action_ind)
                else:
                    action = self.env.action_space.sample()
                    action_ind = self.env.encode_action(action)

                new_state, reward, done, info = self.env.step(action)

                # Adds state to Q-Table if it wasn't there yet
                if new_state not in self.qtable:
                    self.qtable[new_state] = np.zeros(self.action_size)

                if reward != -100:
                    self.qtable[state][action_ind] = self.qtable[state][action_ind] + self.learning_rate * (reward + self.gamma * np.max(self.qtable[new_state]) - self.qtable[state][action_ind])

                    total_rewards += reward
                # Marks the state-action pair as invalid if it's invalid
                # In this case, the normal function is not used, as we do not want to influence the value of other states
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

                # With linear decay, it doesn't lower the epsilon past the ending_epsilon value
                if self.starting_epsilon > self.ending_epsilon:
                    if aux_expsilon > self.ending_epsilon:
                        epsilon = aux_expsilon
                else:
                    if aux_expsilon < self.ending_epsilon:
                        epsilon = aux_expsilon

            # If the episode didn't finish (final value == 0)
            # The invalid_episodes counter is incremented
            # This counter will be used to decrease the number of episodes when calculating the overall score
            # We don't want invalid episodes decreasing/increasing the overall score
            # The 0 rewards will still be included in the rewards array
            if total_rewards == 0:
                invalid_episodes += 1
            rewards.append(total_rewards)

        score = sum(rewards)/(self.max_episodes - invalid_episodes)

        if self.print_final_score:
            print("Score over time: " + str(score))

        return score, rewards, epsilons