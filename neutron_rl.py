from NeutronRL.q_learning import QLearning
from NeutronRL.sarsa import SARSA

qlearning = QLearning(max_episodes=100, starting_epsilon=0.5, max_steps=2000, render=False, env='Neutron-5x5-White-Easy-v0')

# qlearning.train()
# qlearning.print_qtable()

sarsa = SARSA(max_episodes=500, starting_epsilon=0.9, decay_rate=0, max_steps=2000, render=False, env='Neutron-5x5-White-Easy-v0')
sarsa.train()
sarsa.print_qtable()