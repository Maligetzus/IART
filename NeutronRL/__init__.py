from gym.envs.registration import register
from NeutronGame.neutron_util import Player, BoardTypes

register(
    id='Neutron-White-v0',
    entry_point='NeutronRL.envs:NeutronEnv',
    kwargs={'board_type': BoardTypes.Board_5X5, 'player': Player.White},
    max_episode_steps=2000
)
