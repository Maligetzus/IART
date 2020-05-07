from gym.envs.registration import register

register(
    id='Neutron-v0',
    entry_point='Neutron_gym.envs:NeutronEnv',
    max_episode_steps=2000,
)
