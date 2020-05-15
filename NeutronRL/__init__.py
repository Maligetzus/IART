from gym.envs.registration import register
from NeutronGame.neutron_util import Player, BoardTypes
from NeutronRL.envs.neutron_env import Opponent

register(
    id='Neutron-5x5-White-Random-v0',
    entry_point='NeutronRL.envs:NeutronEnv',
    kwargs={'board_type': BoardTypes.Board_5X5, 'player': Player.White, 'opponent': Opponent.Random},
    max_episode_steps=2000
)

register(
    id='Neutron-5x5-White-Easy-v0',
    entry_point='NeutronRL.envs:NeutronEnv',
    kwargs={'board_type': BoardTypes.Board_5X5, 'player': Player.White, 'opponent': Opponent.Easy},
    max_episode_steps=2000
)
