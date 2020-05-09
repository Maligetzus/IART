from gym.envs.registration import register
from NeutronGame.neutron_util import Player, BoardTypes

register(
    id='Neutron-5x5-White',
    entry_point='Neutron_gym.envs:NeutronEnv',
    kwargs={'board_type' : BoardTypes.Board_5X5, 'player': Player.White},
    max_episode_steps=2000,
)
