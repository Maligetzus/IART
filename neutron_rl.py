from NeutronRL.q_learning import QLearning
from NeutronRL.sarsa import SARSA
import matplotlib.pyplot as plt
from NeutronRL.env_algorithm import EpsilonDecay
from NeutronRL.env_play import EnvPlay

# qlearning = QLearning(max_episodes=1000, max_steps=2000, starting_epsilon=1, ending_epsilon=0.1, decay_rate=(1 - 0.1)/1000, epsilon_decay=EpsilonDecay.Exponential, render=False, env='Neutron-5x5-White-Random-v0', log=False, log_detail=False)
# qlearning = QLearning(max_episodes=1000000, max_steps=2000, decay_rate=0.00005, render=False, env='Neutron-5x5-White-Random-v0', log=False, log_detail=False)
# score, rewards, epsilons = qlearning.train()

# sarsa = SARSA(max_episodes=4000, starting_epsilon=1, ending_epsilon=0.3, decay_rate=(1 - 0.3)/1000, max_steps=2000, epsilon_decay=EpsilonDecay.Linear, render=False, env='Neutron-5x5-White-Easy-v0', log=False, log_detail=False)
sarsa = SARSA(max_episodes=1000, max_steps=2000, epsilon_decay=EpsilonDecay.Exponential, render=False, env='Neutron-5x5-White-Easy-v0', log=False, log_detail=False)
score, rewards, epsilons = sarsa.train()

print(f"Score: {score}")

# plt.plot(rewards, label="Rewards")
# plt.plot(epsilons, label="Epsilon values")
# plt.axhline(color="black", ls="--", alpha=0.4)
# plt.ylim(-1.1, 1.1)
# plt.legend()
# plt.show()
# plt.close()

winrate = []
num_wins = 0

for i in range(len(rewards)):
    if rewards[i] == 1:
        num_wins += 1

    winrate.append(num_wins / (i + 1))

plt.plot(winrate, label="Win Rate")
plt.plot(epsilons, label="Epsilon values")
plt.axhline(color="black", ls="--", alpha=0.4)
plt.ylim(-0.1, 1.1)
plt.legend()
plt.show()

# play = EnvPlay(qlearning.export_qtable())
play = EnvPlay(sarsa.export_qtable())
# finished, victory = play.play(env='Neutron-5x5-White-Easy-v0', max_plays=2000, log=True)

# if finished:
#     if victory:
#         print("Bot won!")
#     else:
#         print("Bot lost!")
# else:
#     print("Game did not finish.")

victories, defeats, unfinished = play.play_multiple(num_games=100, log_games=False, learn=True)
print(f"Victories: {victories}")
print(f"Defeats: {defeats}")
print(f"Unfinished: {unfinished}")