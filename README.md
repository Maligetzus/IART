# IART Project - Neutron board game in Python (using Minimax algorithm)

## How to Run
To be able to run the game, you need the *pygame* package:

```
pip install pygame
```

Once *pygame* is installed, just execute the [neutron_game.py file](neutron_game.py):

```python
python neutron_game.py
```

## How to Play

On the main menu, you can select the players and the size of the board. 

![Main menu](NeutronGame/resources/screenshot1.JPG "Main Menu")

During the game (if there is a human player) you can control the pieces, during your turn, by clicking and holding on the piece you want to move and sliding it in the desired direction.

![Game screenshot](NeutronGame/resources/screenshot2.JPG "Game screenshot")

## Bots

The bot moves are calculated using minimax with alpha-beta pruning, with differing depths and heuristics in each different level:
* Greedy:
    * Heuristic #1
    * Depth: 1
    * Minimax with α–β pruning

* Level 0:
    * Heuristic #1
    * Depth: 2
    * Minimax with α–β pruning

* Level 1:
    * Heuristic #1
    * Depth: 3
    * Minimax with α–β pruning

* Level 2:
    * Heuristic #2
    * Depth: 3
    * Minimax with α–β pruning

* Level 3:
    * Heuristic #3
    * Depth: 3
    * Minimax with α–β pruning

* Random Minimax:
    * Heuristic #3
    * Depth: 3
    * Minimax with α–β pruning that chooses one of best moves randomly

* Ordered Minimax:
    * Heuristic #3
    * Depth: 3
    * Minimax with α–β pruning that checks the most likely to be better Neutron directions first

**Note**: the levels indicate different search parameters, they do not imply better skill or efficiency.

### Heuristics

#### Heuristic #1

*NeutronNumPathsToPlayer* - *NeutronNumPathsToOpponent*

#### Heuristic #2

10 * *NumEmptyTilesPlayer* - 10 * *NumEmptyTilesOpponent* + 10 * *Odd* * (8 - *NumEmptyTilesAroundNeutron*)

#### Heuristic #3

10 * *NumEmptyTilesPlayer* - 10 * *NumEmptyTilesOpponent* + 200 * *NeutronNumPathsToPlayer* - 200 * *NeutronNumPathsToOpponent* + 10 * *Odd* * (8 - *NumEmptyTilesAroundNeutron*)

#### In all heuristics
*VictoryPlayer* -> 999 - *depth*
*VictoryOpponent* -> -999 + *depth*

* *NumEmptyTilesPlayer* - Number of empty tiles in the current player's base
* *NumEmptyTilesOpponent* - Number of empty tiles in the opponent's base
* *NeutronNumPathsToPlayer* - Number of paths the Neutron can take directly to the current player's base
* *NeutronNumPathsToOpponent* - Number of paths the Neutron can take directly to the opponents's base
* *NumEmptyTilesAroundNeutron* - Number of empty tiles around Neutron
* *Odd* - **1** *if* *NumEmptyTilesAroundNeutron* is odd *else* **-1**
* *VictoryPlayer* - *if* Neutron is in current player's base
* *VictoryOpponent* - *if* Neutron is in opponent's base
* *depth* - minimax tree depth

# Reinforcement Learning in Neutron

## How to Run
To be able to run the reinforcement learning unit, you need the following packages:
* *gym*
* *matplotlib*
* *numpy*
* *pygame*

```
pip install gym matplotlib numpy pygame
```

To try the RL demo, just execute the [neutron_rl.py file](neutron_rl.py):

```python
python neutron_rl.py
```

The demo runs the Q-Learning algorithm with the **Random Bot** as the opponent, with 1000 episodes and 2000 steps (the rest of the parameters are the default values). It shows the average score after training and a graph plot with the win rate and the epsilon value as the episode number increases. After that, it runs a testing phase with 100 games, showing the amount of won, lost and unfinished games.

This demo should serve as a good starting point to learn how to use the algorithms.

To delve deeper into how our algorithms were implemented, see the files themselves in [the RL folder](NeutronRL) and check out [our notebook](NeutronRL_Notebook.ipynb), which also contains experimental results.

## Environment

Since we're using the OpenAI Gym library, we had to implement an environment for the learning bot to interact with. We used the code already implemented for the main game to make the environment (you can see it in the [neutron_env.py file](NeutronRL/envs/neutron_env.py)).

If you want to use this environment with other parameters, you need to register it in [\_\_init\_\_.py](NeutronRL/__init__.py).

## Algorithms

We implemented the following algorithms:
* [Q-Learning](NeutronRL/q_learning.py)
* [SARSA](NeutronRL/sarsa.py)

Both algorithms inherit the base class [EnvAlgorithm](NeutronRL/env_algorithm.py), where the default values for each parameter are defined:
* *Number of Episodes*: 100
* *Maximum Number of Steps*: 99
* *Learning Rate*: 0.8
* *Discounting Rate (Gamma)*: 0.95
* *Starting Epsilon*: 0.9
* *Ending Epsilon*: 0.01
* *Decay Rate*: 0.001
* *Epsilon Decay*: Exponential
* *Opponent*: Random Bot

### Reward

For the reward system, we decided to only give a positive (1) or negative (-1) reward at the end of the episode, for winning or losing the game respectively, with all the other steps returning no reward (0).

For invalid actions (ones that can't be taken in a specific state) we return a special reward (-100). This reward doesn't influence any other state-action pair's value apart from the invalid one, and is uniquely used to indicate that that action should never be taken in that specific state.

### Bot Opponents

To change the opponent, you have to select a different environment, from the ones registered [in this file](NeutronRL/__init__.py).

There are two different opponents:
* *Random Bot*: makes its plays randomly.
* *Easy Bot*: uses Minimax with depth 2 and the heuristic #1 to calculate the best play.

### Epsilon Decay

There are the following epsilon decays, with their specific function.

#### Exponential Decay

`epsilon = ending_epsilon + (starting_epsilon - ending_epsilon) * e^(-decay_rate * current_episode)`

#### Linear Decay

`epsilon = starting_epsilon + (starting_epsilon - ending_epsilon) * (-decay_rate * current_episode)` 

In this case, the decay stops when the *ending_epsilon* value is reached.

#### None

Epsilon doesn't decay, stays constant (always *starting_epsilon*).

## Testing

We implemented a [testing class](NeutronRL/env_play.py) to test the effectiveness of the learning bot after it's training. It can run any amount of games against any bot, and prints out the number of wins, defeats and unfinished games. It also has the option to allow the bot to learn what actions are invalid, just like it's done in training. An example of testing is in the [demo file](neutron_rl.py).