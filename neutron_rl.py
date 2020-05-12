from NeutronRL.q_learning import QLearning

qlearning = QLearning(max_episodes=2, starting_epsilon=0.5)

qlearning.train()