import gym
import asyncio
import os
from typing import List, Dict, Tuple
import numpy as np
from gym_derk.derk_app_instance import DerkAppInstance
from gym_derk.derk_server import DerkAgentServer, DerkSession
import logging

logger = logging.getLogger(__name__)

class DerkEnv(gym.Env):
  """Reinforcement Learning environment for "Dr. Derk's Mutant Battlegrounds"

  There are two modes for the environment:

  * ``mode="normal"``: You control both the home and away teams.
  * ``mode="connected"``: Connects this environment to another agent. See :ref:`connected_mode`.

  Args:
    mode: ``"normal"`` (default), ``"connected"``. See above for details. (Environment variable: DERK_MODE)
    n_arenas: Number of parallel arenas to run
    reward_function: Reward function. See :ref:`reward-function` for available options
    turbo_mode: Skip rendering to the screen to run as fast as possible
    home_team: Home team creatures. See :ref:`creature-config`.
    away_team: Away team creatures. See :ref:`creature-config`.
    session_args: See arguments to :meth:`gym_derk.DerkAppInstance.create_session`
    app_args: See arguments to :class:`gym_derk.DerkAppInstance`
    agent_server_args: See arguments to :class:`gym_derk.DerkAgentServer`

  This is a convenience wrapper of the more low level api of :class:`gym_derk.DerkAppInstance`,
  :class:`gym_derk.DerkAgentServer` and :class:`gym_derk.DerkSession`.

  """
  def __init__(self,
      mode: str=False,
      n_arenas: int=None,
      reward_function: Dict=None,
      turbo_mode: bool=False,
      home_team: List[Dict]=None,
      away_team: List[Dict]=None,
      session_args: Dict={},
      app_args: Dict={},
      agent_server_args: Dict={}
    ):

    self.mode = mode if mode is not None else os.environ.get('DERK_MODE', 'normal')
    self.session_args = session_args
    if n_arenas is not None:
      self.session_args['n_arenas'] = n_arenas
    if reward_function is not None:
      self.session_args['reward_function'] = reward_function
    if turbo_mode is not None:
      self.session_args['turbo_mode'] = turbo_mode
    if home_team is not None:
      self.session_args['home_team'] = home_team
    if away_team is not None:
      self.session_args['away_team'] = away_team
    self.app_args = app_args

    self.session = asyncio.Future()
    if 'port' not in agent_server_args:
      agent_server_args['port'] = 8788
    self.logger = logger.getChild('DerkEnv({})'.format(agent_server_args['port']))
    self.server = DerkAgentServer(self._handle_session, **agent_server_args)
    asyncio.get_event_loop().run_until_complete(self.server.start())

    if 'agent_hosts' not in self.session_args:
      if self.mode == 'connected':
        self.session_args['agent_hosts'] = [{ 'uri': self.server.uri, 'regions': [{ 'sides': 'home' }] }, { 'uri': 'ws://127.0.0.1:8789', 'regions': [{ 'sides': 'away' }] }]
      else:
        self.session_args['agent_hosts'] = [{ 'uri': self.server.uri, 'regions': [{ 'sides': 'both' }] }]

    self.app = DerkAppInstance(**app_args)
    asyncio.get_event_loop().run_until_complete(self.app.start())

    asyncio.get_event_loop().run_until_complete(self.app.create_session(**self.session_args))
    asyncio.get_event_loop().run_until_complete(self.app.connect_to_agent_hosts())
    self.can_reset = True

    asyncio.get_event_loop().run_until_complete(self.session)

  @property
  def n_agents(self) -> int:
    """Number of agents controlled by this environment

    I.e. ``env.n_teams * env.n_agents_per_team``
    """
    return self.session.result().n_agents

  @property
  def n_teams(self) -> int:
    """Number of teams controlled by this environment"""
    return self.session.result().n_teams

  @property
  def n_agents_per_team(self) -> int:
    """Number of agents in a team (3)"""
    return self.session.result().n_agents_per_team

  @property
  def action_space(self):
    """Gym space for actions"""
    return self.session.result().action_space

  @property
  def observation_space(self):
    """Gym space for observations"""
    return self.session.result().observation_space

  @property
  def total_reward(self) -> np.ndarray:
    """Accumulated rewards over an episode

    Numpy array of shape (n_agents)
    """
    return self.session.result().total_reward

  @property
  def episode_stats(self) -> Dict:
    """Stats for the last episode"""
    return self.session.result().episode_stats

  @property
  def team_stats(self) -> np.ndarray:
    """Stats for each team for the last episode

    Numpy array of shape (env.n_teams, len(:class:`gym_derk.TeamStatsKeys`))

    See :ref:`reading-stats`
    """
    return self.session.result().team_stats

  def reset(self) -> np.ndarray:
    """Resets the state of the environment and returns an initial observation.

    Returns:
      The initial observation for each agent, with shape (n_agents, len(:class:`gym_derk.ObservationKeys`)).

    Raises:
      ConnectionLostError: If there was a connection error in connected mode
    """
    return asyncio.get_event_loop().run_until_complete(self.async_reset())

  def step(self, action_n: np.ndarray = None) -> Tuple[np.ndarray, np.ndarray, List[bool], List[Dict]]:
    """Run one timestep.

    Accepts a list of actions, one for each agent, and returns the current state.

    Actions can have one of the following formats/shapes:

    * Numpy array of shape (:attr:`n_teams`, :attr:`n_agents_per_team`, len(:class:`gym_derk.ActionKeys`))
    * Numpy array of shape (:attr:`n_agents`, len(:class:`gym_derk.ActionKeys`))
    * List of actions (i.e. ``[[1, 0, 0, 2, 0], [0, 1, 0, 0, 3], ...]``), one inner array per agent. This is just cast to a numpy array of shape (:attr:`n_agents`, len(:class:`gym_derk.ActionKeys`)).

    The returned observations are laid out in the same way as the actions, and can therefore
    be reshape like the above. For instance: ``observations.reshape((env.n_teams, env.n_agents_per_team, -1))``

    Args:
      action_n: Numpy array or list of actions. See :class:`gym_derk.ActionKeys`

    Returns:
      A tuple of (observation_n, reward_n, done_n, info).
      observation_n has shape (n_agents, len(:class:`gym_derk.ObservationKeys`))

    Raises:
      ConnectionLostError: If there was a connection error in connected mode
    """
    return asyncio.get_event_loop().run_until_complete(self.async_step(action_n))

  def close(self):
    """Shut down environment
    """
    return asyncio.get_event_loop().run_until_complete(self.async_close())

  async def _handle_session(self, session):
    self.logger.info('[_handle_session] Got session')
    self.session.set_result(session)
    await session.websocket.wait_closed()

  async def async_close(self):
    """Async version of :meth:`close`"""
    self.logger.info('[async_close] Closing environment')
    self.server.close()
    await self.app.close()
    self.logger.info('[async_close] Done')

  async def async_reset(self):
    """Async version of :meth:`reset`"""
    if not self.can_reset or not self.app.running:
      self.logger.info('[async_reset] Bad state detected, running full reset')
      self.logger.info('[async_reset] Closing current session')
      await self.session.result().close()
      self.logger.info('[async_reset] Waiting for current session to finnish')
      self.session = asyncio.Future()
      if not self.app.running:
        self.logger.info('[async_reset] App is not running, restarting')
        self.app = DerkAppInstance(**self.app_args)
        await self.app.start()
        self.logger.info('[async_reset] App restarted')
      self.logger.info('[async_reset] Creating new session')
      await self.app.create_session(**self.session_args)
      await self.app.connect_to_agent_hosts()
      self.logger.info('[async_reset] Resetting')
      self.logger.info('[async_reset] Full reset done')
    session = await self.session
    try:
        res = await asyncio.gather(self.app.episode_reset(), session.reset())
        return res[1]
    except Exception as e:
      self.logger.info('[async_reset] Reset threw an error', e)
      self.app.disconnect_all_remotes()

  async def async_step(self, action_n: np.ndarray = None) -> Tuple[np.ndarray, np.ndarray, List[bool], List[Dict]]:
    """Async version of :meth:`step`"""
    session = await self.session
    res = await asyncio.gather(session.step(action_n), self.app.episode_step())
    self.can_reset = all(res[0][2])
    return res[0]
