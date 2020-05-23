from NeutronRL.q_learning import QLearning
from NeutronRL.sarsa import SARSA
import matplotlib.pyplot as plt
from NeutronRL.env_algorithm import EpsilonDecay

qlearning = QLearning(max_episodes=1000, max_steps=2000, starting_epsilon=1, ending_epsilon=0.1, decay_rate=(1 - 0.1)/500, epsilon_decay=EpsilonDecay.Linear, render=True, env='Neutron-5x5-White-Easy-v0', log=True, log_detail=True)
# score, rewards, epsilons, action_picks = qlearning.train()

sarsa = SARSA(max_episodes=2000, starting_epsilon=1, ending_epsilon=0.1, decay_rate=(1 - 0.1)/1000, max_steps=2000, epsilon_decay=EpsilonDecay.Linear, render=False, env='Neutron-5x5-White-Easy-v0', log=False, log_detail=False)
score, rewards, epsilons, action_picks = sarsa.train()

print(f"Score: {score}")

plt.plot(rewards, label="Rewards")
plt.plot(epsilons, label="Epsilon values")
plt.plot(action_picks, label="Random action picks")
plt.axhline(color="black", ls="--", alpha=0.4)
plt.ylim(-1.1, 1.1)
plt.legend()
plt.show()