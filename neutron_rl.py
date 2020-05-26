import matplotlib.pyplot as plt
from NeutronRL.q_learning import QLearning
from NeutronRL.env_algorithm import EpsilonDecay
from NeutronRL.env_play import EnvPlay

# Bot will learn
qlearning = QLearning(env='Neutron-5x5-White-Random-v0', max_episodes=1000, max_steps=2000)
score, rewards, epsilons = qlearning.train()

# Creates the win rate array
winrate = []
num_wins = 0

for i in range(len(rewards)):
    if rewards[i] == 1:
        num_wins += 1

    winrate.append(num_wins / (i + 1))

# Plots the data
plt.plot(winrate, label="Win Rate")
plt.plot(epsilons, label="Epsilon values")
plt.axhline(color="black", ls="--", alpha=0.4)
plt.ylim(-0.1, 1.1)
plt.xlabel("Episodes")
plt.legend()
plt.show()

# Plays 100 games to test the new bot
play = EnvPlay(qlearning.export_qtable())
victories, defeats, unfinished = play.play_multiple(num_games=100, learn=True, log_games=False, log_results=False)

print(f"Victories: {victories}")
print(f"Defeats: {defeats}")
print(f"Unfinished: {unfinished}")