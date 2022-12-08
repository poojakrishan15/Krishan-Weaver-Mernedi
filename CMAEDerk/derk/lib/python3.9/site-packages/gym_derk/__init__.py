from gym.envs.registration import register
from gym_derk.derk_server import DerkSession, DerkAgentServer, ConnectionLostError, run_derk_agent_server_in_background
from gym_derk.derk_app_instance import DerkAppInstance
from gym_derk.enums import ObservationKeys, TeamStatsKeys
from gym_derk.action_keys import ActionKeys
from gym_derk.utils import print_table

register(
    id='derk-v0',
    entry_point='gym_derk.envs:DerkEnv',
)