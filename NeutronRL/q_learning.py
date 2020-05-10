import random
import gym
import numpy as np
import NeutronRL.envs.neutron_env


def simulate():
    rewards = []
    for current_episode in range(max_episodes):
        state = env.reset()
        step = 0
        done = False
        total_rewards = 0
        for step in range(max_steps):
            exp_exp_tradeoff = random.uniform(0, 1)

            if exp_exp_tradeoff > epsilon:
                action = np.argmax(qtable[state, :])
            else:
                action = env.action_space.sample()

            new_state, reward, done, info = env.step(action)

            qtable[state, action] = qtable[state, action] + learning_rate * (
                        reward + gamma * np.max(qtable[new_state, :]) - qtable[state, action])

            total_rewards += reward
            state = new_state

            if done:
                break

        # Reduce epsilon (because we need less and less exploration)
        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * current_episode)
        rewards.append(total_rewards)

    print ("Score over time: " + str(sum(rewards)/max_episodes))
    print(qtable)


if __name__ == "__main__":
    env = gym.make("Neutron-White-v0")

    # action_size = env.action_space.n # Doesnt work on boxes
    action_size = tuple((env.action_space.high + np.ones(env.action_space.shape)).astype(int))
    print(action_size)
    # state_size = env.observation_space.n # Doesnt work on boxes
    state_size = tuple((env.observation_space.high + np.ones(env.observation_space.shape)).astype(int))
    print(state_size)
    state = env.observation_space
    qtable = np.zeros((state_size, action_size))

    max_episodes = 2 # Total episodes
    learning_rate = 0.8  # Learning rate
    max_steps = 99  # Max steps per episode
    gamma = 0.95  # Discounting rate

    # Exploration
    epsilon = 0.1
    max_epsilon = 1.0
    min_epsilon = 0.01
    decay_rate = 0.001

    # simulate()

