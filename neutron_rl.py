from NeutronRL.q_learning import QLearning

qlearning = QLearning(max_episodes=1000, starting_epsilon=0.5)

qlearning.train()
qlearning.print_qtable()