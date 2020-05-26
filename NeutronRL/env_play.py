import random
import gym
import numpy as np
import NeutronRL.envs.neutron_env
from NeutronRL.env_algorithm import EnvAlgorithm, EpsilonDecay

# Used to test a trained learning bot
class EnvPlay():

    def __init__(self, qtable=None):
        self.qtable = qtable

    # Plays multiple games in a row
    # Returns the number of victories, defeats and unfinished games
    def play_multiple(self, env="Neutron-5x5-White-Random-v0", num_games=10, max_plays=2000, learn=False, log=False, log_results=True, log_games=False):
        unfinished = 0
        victories = 0
        defeats = 0

        for game in range(num_games):
            if log:
                print(f"Game {game + 1}")

            finished, victory = self.play(env, max_plays, learn, log_games, log_results)

            if finished:
                if victory:
                    victories += 1
                else:
                    defeats += 1
            else:
                unfinished += 1

        return victories, defeats, unfinished

    # Plays a game
    def play(self, env="Neutron-5x5-White-Random-v0", max_plays=2000, learn=False, log=False, log_result=True):
        if self.qtable == None:
            return False, False

        finished = False
        victory = False

        env = gym.make(env)

        action_size_aux = tuple((env.action_space.high - env.action_space.low + np.ones(env.action_space.shape)).astype(int))

        action_size = 1

        # Calculates action size
        for num in action_size_aux:
            action_size *= num

        # Gets initial state
        state = env.reset()

        for step in range(max_plays):
            # If a bot is learning, then it adds never found states to the q-table
            # It will then register the action's it take as invalid, if it ends up being invalid
            if learn:
                if state not in self.qtable:
                    self.qtable[state] = np.zeros(action_size)
                
                action_ind = np.argmax(self.qtable[state])
            # If learning is not on, it doesn't know its action was invalid, and will keep trying to take it
            else:
                if state not in self.qtable:
                    action_ind = 0
                else:
                    action_ind = np.argmax(self.qtable[state])

            # Gets action from the enconded action id
            action = env.decode_action(action_ind)
            
            # Takes the action
            new_state, reward, done, info = env.step(action)

            # This is here because when an AI Gym environment reaches its max step, it always returns done as true
            # In this case we only want to receive done as true when the game actually reached its end
            # By checking this flag in info, we can tell if the game did or not actually finish
            if "TimeLimit.truncated" in info:
                done = not info["TimeLimit.truncated"]

            # If the bot is learning, adds the invalid action reward to the state-action pair
            if learn and reward == -100:
                self.qtable[state][action_ind] = reward

            if log:
                env.render()
            
            if done:
                finished = True
                
                if reward == 1:
                    victory = True
                    if log_result:
                        print("Victory! ", end="")
                else:
                    victory = False
                    if log_result:
                        print("Defeat! ", end="")

                if log_result:
                    print("Number of steps: ", step)
                break

            state = new_state

        if not finished and log_result:
            print("Didn't finish the game")

        return finished, victory

    def import_qtable(self, qtable):
        self.qtable = qtable

    def export_qtable(self):
        return self.qtable