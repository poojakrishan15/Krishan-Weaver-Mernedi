import websockets
import gym
import asyncio
from typing import List, Dict, Tuple
import enum
import numpy as np
import os
import json
import threading
import logging
from gym_derk.enums import TeamStatsKeys, ObservationKeys

logger = logging.getLogger(__name__)

class ConnectionLostError(Exception):
  def __init__(self, session):
    self.session = session

class DerkSession:
  """A single training/evaluation session, consisting of multiple episodes

  Attributes:
    n_teams: Number of teams controlled by this environment
    n_agents_per_team: Number of agents in a team (3)
    action_space: Gym space for actions
    observation_space: Gym space for observations
    total_reward: Accumulated rewards over an episode. Numpy array of shape (n_agents)
    team_stats: Stats for each team for the last episode. Numpy array of shape (n_teams, len(:class:`gym_derk.TeamStatsKeys`)). See :ref:`reading-stats`
    episode_stats: Stats for the last episode. See :ref:`reading-stats`

  """
  def __init__(self, websocket, init_msg):
    self.websocket = websocket
    self.n_teams = init_msg['nTeams']
    self.remote_messages = asyncio.Queue()

    self.logger = logger.getChild('DerkSession({})'.format(websocket.port))

    self.n_agents_per_team = 3
    self.done = False
    self.total_reward = np.zeros((self.n_agents))
    self.episode_stats = { 'wins': 0, 'losses': 0, 'ties': 0 }
    self.team_stats = np.zeros((self.n_teams, int(len(TeamStatsKeys))))

    self.observation_space = gym.spaces.Box(low=-1, high=1, shape=[len(ObservationKeys)])
    self.action_space = gym.spaces.Tuple((
      gym.spaces.Box(low=-1, high=1, shape=[]), # MoveX
      gym.spaces.Box(low=-1, high=1, shape=[]), # Rotate
      gym.spaces.Box(low=0, high=1, shape=[]), # ChaseFocus
      gym.spaces.Discrete(4), # CastingSlot
      gym.spaces.Discrete(8), # ChangeFocus
    ))

  @property
  def n_agents(self):
    """Number of agents controlled by this environment

    I.e. ``env.n_teams * env.n_agents_per_team``
    """
    return self.n_teams * self.n_agents_per_team

  async def close(self):
    """Close session"""
    await self.websocket.close()

  async def reset(self) -> np.ndarray:
    """See :meth:`gym_derk.envs.DerkEnv.reset`"""
    self.total_reward = np.zeros((self.n_agents))
    self.done = False
    self.logger.info('[reset] Waiting for observations')
    observations = self._decode_observations(await self._get_msg())
    self.logger.info('[reset] Got observations')
    return observations

  async def step(self, action_n: np.ndarray = None) -> Tuple[np.ndarray, np.ndarray, List[bool], List[Dict]]:
    """See :meth:`gym_derk.envs.DerkEnv.step`"""
    actions_arr = np.asarray(action_n, dtype='float32').reshape((-1)).tobytes()
    try:
      await self.websocket.send(actions_arr)
    except websockets.exceptions.ConnectionClosedError:
      raise ConnectionLostError(self)

    observations = self._decode_observations(await self._get_msg())
    reward = self._decode_reward(await self._get_msg())
    res = json.loads(await self._get_msg())

    self.total_reward = np.add(self.total_reward, reward)

    self.done = all(res['done'])

    if self.done:
      self.team_stats = self._decode_team_stats(await self._get_msg())
      points = self.team_stats[:, TeamStatsKeys.Reward.value]
      opponent_points = self.team_stats[:, TeamStatsKeys.OpponentReward.value]
      self.episode_stats['wins'] = np.sum(points > opponent_points)
      self.episode_stats['losses'] = np.sum(points < opponent_points)
      self.episode_stats['ties'] = np.sum(points == opponent_points)

    return observations, reward, res['done'], res['info']

  async def _get_msg(self):
    msg = await self.remote_messages.get()
    if msg == "connection_ended":
      raise ConnectionLostError(self)
    return msg

  def _decode_observations(self, observations):
    obs = np.frombuffer(observations, dtype='float32')
    # Images/textures in WebGL are layed out in layer for z, and 4 components per channel
    return obs.reshape((int(len(ObservationKeys) / 4), -1, 4)).swapaxes(0, 1).reshape((-1, len(ObservationKeys)))

  def _decode_team_stats(self, data):
    arr = np.frombuffer(data, dtype='float32')
    # Images/textures in WebGL are layed out in layer for z
    return arr.reshape(int(len(TeamStatsKeys)), -1).transpose()

  def _decode_reward(self, reward):
    return np.frombuffer(reward, dtype='float32')

class DerkAgentServer:
  """Agent server

  This creates a websocket agent server, listening on ``host:port``

  Args:
    handle_session: A coroutine accepting the session and optionally a list org argument
    port: Port to listen to. Defaults to 8789
    host: Host to listen to. Defaults to 127.0.0.1
    args: Dictonary of args passed to handle_session

  """
  def __init__(self, handle_session, port: int=None, host: str=None, args: Dict={}):
    self.handle_session = handle_session
    self.host = host if host is not None else os.environ.get('DERK_SERVER_HOST', '127.0.0.1')
    self.port = port if port is not None else os.environ.get('DERK_SERVER_PORT', 8789)
    self.uri = 'ws://' + self.host + ':' + str(self.port)
    self.args = args

    self.logger = logger.getChild('DerkAgentServer({})'.format(self.port))

  def close(self):
    """Shutdown"""
    self.websocket_server.close()

  async def start(self):
    """Start the server"""
    start_server = websockets.serve(self._handle_websocket, self.host, self.port, max_size=None)
    self.websocket_server = await start_server
    self.logger.info('Serving on ws://' + self.host + ':' + str(self.port))

  async def _handle_websocket(self, websocket, path):
    self.logger.info('[_handle_websocket] Got websocket connection')

    init_msg = json.loads(await websocket.recv())
    session = DerkSession(websocket, init_msg)
    await asyncio.gather(self._run_session(session), self._run_websocket(session))

    self.logger.info('[_handle_websocket] Websocket disconnected')

  async def _run_session(self, session):
    await self.handle_session(session, **self.args)
    await session.close()

  async def _run_websocket(self, session):
    try:
      async for message in session.websocket:
        await session.remote_messages.put(message)
    except websockets.exceptions.ConnectionClosedError:
      self.logger.info('[_handle_websocket] Connection lost')
    self.logger.info('[_handle_websocket] End of messages')
    await session.remote_messages.put('connection_ended')

def agent_server_background(handle_session, **kwargs):
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  server = DerkAgentServer(handle_session, **kwargs)
  loop.run_until_complete(server.start())
  loop.run_forever()

def run_derk_agent_server_in_background(handle_session, **kwargs):
  """Launch a DerkAgentServer a background thread

  Accepts the same arguments as :class:`gym_derk.DerkAgentServer`
  """
  thread = threading.Thread(target=agent_server_background, args=(handle_session,), kwargs=kwargs, daemon=True)
  thread.start()
  return thread
