import asyncio
import os
from typing import List, Dict, Tuple, Union
import sys
import http.server
import socketserver
import urllib
import posixpath
import threading
import itertools
import numpy as np
import base64
import enum
from gym_derk.utils import print_table
from gym_derk.enums import TeamStatsKeys

# This is a copy of the pyppeteer function in pyppeteer/chromium_downloader,
# but since we're trying to update the environment variables which are read in that file
# we can't import it
def pyppeteer_current_platform() -> str:
    if sys.platform.startswith('linux'):
        return 'linux'
    elif sys.platform.startswith('darwin'):
        return 'mac'
    elif (sys.platform.startswith('win') or
          sys.platform.startswith('msys') or
          sys.platform.startswith('cyg')):
        if sys.maxsize > 2 ** 31 - 1:
            return 'win64'
        return 'win32'
    raise OSError('Unsupported platform: ' + sys.platform)

if not ('PYPPETEER_CHROMIUM_REVISION' in os.environ):
  plt = pyppeteer_current_platform()
  if plt == 'win32':
    os.environ['PYPPETEER_CHROMIUM_REVISION'] = '798057'
  elif plt == 'win64':
    os.environ['PYPPETEER_CHROMIUM_REVISION'] = '803555'
  elif plt == 'linux':
    os.environ['PYPPETEER_CHROMIUM_REVISION'] = '798580'
  elif plt == 'mac':
    os.environ['PYPPETEER_CHROMIUM_REVISION'] = '798027'
if not ('PYPPETEER_DOWNLOAD_HOST' in os.environ):
  os.environ['PYPPETEER_DOWNLOAD_HOST'] = 'http://storage.googleapis.com'
import pyppeteer
import logging

logger = logging.getLogger(__name__)

app_build_path = os.path.abspath(os.path.expanduser(__file__ + '/../app_build'))
app_build_index_html = os.path.join(app_build_path, 'index.html')

class AppBuildRequestHandler(http.server.SimpleHTTPRequestHandler):
  def translate_path(self, path):
      path = path.split('?',1)[0]
      path = path.split('#',1)[0]
      if path == '/':
        path = '/index.html'
      return app_build_path + '/' + path

class DerkAppInstance:
  """Application instance of "Dr. Derk's Mutant Battlegrounds"

  Args:
    app_host: Configure an alternative app bundle host. (Environment variable: DERK_APP_HOST)
    chrome_executable: Path to chrome or chromium. (Environment variable: DERK_CHROME_EXECUTABLE)
    chrome_args: List of command line switches passed to chrome
    chrome_devtools: Launch devtools when chrome starts
    window_size: Tuple with the size of the window
    browser: A pyppeteer browser instance
    browser_logs: Show log output from browser
    web_socket_worker: Run websockets in a web worker

  """
  def __init__(self,
      app_host: str=None,
      chrome_executable: str=None,
      chrome_args: List[str]=[],
      chrome_devtools: bool=False,
      window_size: Tuple[int, int]=[1000, 750],
      browser: pyppeteer.browser.Browser=None,
      browser_logs: bool=False,
      internal_http_server: bool = False):

    self.app_host = app_host if app_host is not None else os.environ.get('DERK_APP_HOST', ('file://' + app_build_index_html))
    self.chrome_executable = chrome_executable if chrome_executable is not None else os.environ.get('DERK_CHROME_EXECUTABLE', None)
    self.chrome_args = chrome_args
    self.chrome_devtools = chrome_devtools
    self.window_size = window_size
    self.browser = browser
    self.browser_logs = browser_logs
    self.internal_http_server = internal_http_server

    self.logger = logger.getChild('DerkAppInstance')

    if self.internal_http_server:
      self.bundle_server = socketserver.TCPServer(('', 0), AppBuildRequestHandler)
      threading.Thread(target=self.bundle_server.serve_forever, daemon=True).start()
      self.app_host = 'http://localhost:' + str(self.bundle_server.server_address[1])

    self.page = None
    self.browser = None

  async def close(self):
    """Shut down app instance
    """
    self.logger.info('[close] Closing instance')
    if self.browser:
      await self.browser.close()
    if self.internal_http_server:
      self.bundle_server.shutdown()
    self.logger.info('[close] Done')

  async def start(self):
    """Start the application"""
    self.logger.info('[init] Using bundle host: ' + self.app_host)
    if not self.browser:
      self.logger.info('[init] Creating browser')
      chromium_args = [
        '--app=' + self.app_host,
        '--allow-file-access-from-files',
        '--disable-web-security',
        '--no-sandbox',
        '--ignore-gpu-blacklist',
        '--user-data-dir=' + os.environ.get('DERK_CHROMEDATA', './chromedata'),
        '--window-size={},{}'.format(self.window_size[0], self.window_size[1]),
      ] + self.chrome_args
      self.browser = await pyppeteer.launch(
        ignoreHTTPSErrors=True,
        headless=False,
        executablePath=self.chrome_executable,
        args=chromium_args,
        defaultViewport=None,
        devtools=self.chrome_devtools,
        handleSIGHUP=False,
        handleSIGTERM=False,
        handleSIGINT=False,
      )
      self.logger.info('[init] Creating browser ok')
    self.logger.info('[init] Getting page')
    self.page = [page for page in (await self.browser.pages()) if (not page.url.startswith('devtools'))][0]
    backend = os.environ.get('DERK_BACKEND', 'production')
    if backend is not None:
      self.logger.info('[init] Setting backend')
      await self.page.evaluateOnNewDocument('''(backend) => window.localStorage.setItem('backend', backend)''', backend)
    if self.browser_logs:
      self.logger.info('[init] Setting up logs')
      self.page.on('console', self._handle_console)
      self.page.on('error', lambda m: self.logger.error('[error] %s', m))
      self.page.on('pageerror', lambda m: self.logger.error('[pageerror] %s', m))
      self.page.on('requestfailed', lambda m: self.logger.error('[requestfailed] %s', m))
    self.logger.info('[init] Navigating to bundle host')
    await self.page.goto(self.app_host, timeout=None)
    self.logger.info('[init] Waiting for GymLoaded')
    await self.page.waitForSelector('.GymLoaded', timeout=0)
    self.logger.info('[init] Gym loaded ok')
    self.logger.info('[init] Done!')

  async def run_session(self, **kwargs):
    """Creates a session, connect hosts and runs episodes loop.

    See :meth:`create_session` for args.

    This is just a shorthand for:

    ```python
    await self.create_session(args)
    await self.connect_to_agent_hosts()
    await self.run_episodes_loop()
    ```
    """
    await self.create_session(**kwargs)
    await self.connect_to_agent_hosts()
    await self.run_episodes_loop()

  async def create_session(self,
      n_arenas: int=1,
      reward_function: Dict=None,
      turbo_mode: bool=False,
      home_team: List[Dict]=None,
      away_team: List[Dict]=None,
      substeps: int=8,
      interleaved: bool=True,
      agent_hosts: Union[List[Dict], str]=None,
      debug_no_observations: bool=False,
      web_socket_worker: bool=None,
      ai_crowd_logo: bool=False,
      read_game_state: bool=False):
    """Create a session

    All arguments are optional.

    Args:
      n_arenas: Number of parallel arenas to run
      reward_function: Reward function. See :ref:`reward-function` for available options
      turbo_mode: Skip rendering to the screen to run as fast as possible
      home_team: Home team creatures. See :ref:`creature-config`.
      away_team: Away team creatures. See :ref:`creature-config`.
      substeps: Number of game steps to run for each call to step
      interleaved: Run each step in the background, returning the previous steps observations
      agent_hosts: List of DerkAgentServer's to connect to, or ``"single_local"``, or ``"dual_local"``. See below for details.
      read_game_state: Read the entire internal game state each step, and provide it as a JSON in the info object returned from the step function.

    With the interleaved mode on, there's a delay between observation and action of size substeps.
    E.g. if substeps=8 there's an 8*16ms = 128ms "reaction time" from observation to action. This means
    that the game and the python code can in effect run in parallel.

    The ``agent_hosts`` argument takes list of dicts with the following format:
    ``{ uri: str, regions: [{ side: str, start_arena: int, n_arenas: int }] }``, where
    ``uri`` specifies a running DerkAgentServer to connect to, and regions define which arenas and sides
    that agent will control.
    ``side`` can be ``'home'``, ``'away'`` or ``'both'``. ``start_arena`` and ``n_arenas`` can be ommitted
    to run the agent on all arenas. You can also pass a string value of ``"single_local"``, in which case
    the ``agent_hosts`` defaults to ``[{ 'uri': 'ws://127.0.0.1:8788', 'regions': [{ 'sides': 'both' }] }]``,
    or if you specify ``"dual_local"`` it defaults to

    .. code-block:: python

      [
        { 'uri': 'ws://127.0.0.1:8788', 'regions': [{ 'sides': 'home' }] },
        { 'uri': 'ws://127.0.0.1:8789', 'regions': [{ 'sides': 'away' }] }
      ]

    """
    if agent_hosts == 'single_local' or agent_hosts is None:
      agent_hosts = [{ 'uri': 'ws://127.0.0.1:8788', 'regions': [{ 'sides': 'both' }] }]
    elif agent_hosts == 'dual_local':
      agent_hosts = [
        { 'uri': 'ws://127.0.0.1:8788', 'regions': [{ 'sides': 'home' }] },
        { 'uri': 'ws://127.0.0.1:8789', 'regions': [{ 'sides': 'away' }] }
      ]
    config = {
      'agentHosts': agent_hosts,
      'home': home_team,
      'away': away_team,
      'rewardFunction': reward_function,
      'nArenas': n_arenas,
      'substeps': substeps,
      'turboMode': turbo_mode,
      'interleaved': interleaved,
      'debugNoObservations': debug_no_observations,
      'webSocketWorkers': web_socket_worker,
      'aiCrowdLogo': ai_crowd_logo,
      'gameState': read_game_state
    }
    self.logger.info('[run_session] Creting session')
    await self.page.evaluate('''(config) => window.derk.createSession(config)''', config)
    self.logger.info('[run_session] Session created')

  async def update_home_team_config(self, config):
    """Update the home teams configuration.

    The session needs to be created first.

    Args:
      config: See :ref:`creature-config`
    """
    await self.page.evaluate('''(config) => window.derk.session.config.home = config''', config)

  async def update_away_team_config(self, config):
    """Update the away teams configuration.

    The session needs to be created first.

    Args:
      config: See :ref:`creature-config`
    """
    await self.page.evaluate('''(config) => window.derk.session.config.away = config''', config)

  async def update_reward_function(self, reward_function):
    """Update the reward function.

    The session needs to be created first.

    Args:
      reward_function: See :ref:`reward-function`
    """
    await self.page.evaluate('''(config) => window.derk.session.setRewardFunction(config)''', reward_function)


  async def connect_to_agent_hosts(self):
    """Connect to agent hosts specified when the session was created

    Returns:
      True if all hosts are connected, False otherwise

    This method can be called in a loop to wait for all hosts to come online.
    """
    return await self.page.evaluate('''() => window.derk.session.connectToAgentHosts()''')

  async def run_episodes_loop(self):
    """Runs episodes in a loop until agents disconnect"""
    self.logger.info('[run_episodes_loop] Starting loop')
    while True:
      await self.run_episode()
    self.logger.info('[run_episodes_loop] Done')

  async def run_episode(self):
    """Run a single episode

    Shorthand for:

    .. code-block:: python

      try:
        await app.episode_reset()
        while not (await app.episode_step()):
          pass
      except Exception as e:
        app.disconnect_all_remotes()

    """
    self.logger.info('[run_episode] Running')
    try:
      await self.episode_reset()
      while not (await self.episode_step()):
        pass
    except Exception as e:
      self.logger.info('[run_episode] Current session threw an error', e)
      await self.disconnect_all_remotes()
      return False
    self.logger.info('[run_episode] Done')
    return True

  async def episode_reset(self):
    """Reset for an episode"""
    self.logger.info('[episode_reset] Running')
    await self.page.evaluate('''() => window.derk.session.reset()''')
    self.logger.info('[episode_reset] Done')

  async def episode_step(self):
    """Step for an episode"""
    self.logger.info('[episode_step] Running')
    res = await self.page.evaluate('''() => window.derk.session.step()''')
    self.logger.info('[episode_step] Done')
    return res

  async def disconnect_all_remotes(self):
    """Disconnect all remotes"""
    self.logger.info('[disconnect_all_remotes] Running')
    await self.page.evaluate('''() => window.derk.session.disconnectAllRemotes()''')
    self.logger.info('[disconnect_all_remotes] Done')

  async def get_team_stats(self) -> np.ndarray:
    """Read all team stats from the last episode

    Returns:
      Team stats for all teams; a numpy array of shape (2, n_arenas, len(:class:`gym_derk.TeamStatsKeys`)).
      The first dimension is the side (0=home, 1=away).
    """
    team_stats_string = await self.page.evaluate('''() => window.derk.session.readTeamStatsBase64()''')
    team_stats = self._decode_team_stats(team_stats_string)
    self.logger.info('[get_team_stats] Done')
    return team_stats

  async def print_team_stats(self, team_stats: np.ndarray=None):
    """Reads and prints the team stats from the last episode"""
    if team_stats is None:
      team_stats = await self.get_team_stats()
    columns = ["side", "arena"] + [x.name for x in TeamStatsKeys]
    print_table(columns, team_stats)

  async def get_episode_stats(self):
    """Gets a summary of stats for the last episode, based on team_stats"""
    team_stats = await self.get_team_stats()
    team_stats = team_stats[0:1, :, :]
    points = team_stats[:, :, TeamStatsKeys.Reward.value]
    opponent_points = team_stats[:, :, TeamStatsKeys.OpponentReward.value]
    episode_stats = { 'home_reward': 0, 'away_reward': 0, 'home_wins': 0, 'away_wins': 0, 'ties': 0 }
    episode_stats['home_reward'] = np.sum(points)
    episode_stats['away_reward'] = np.sum(opponent_points)
    episode_stats['home_wins'] = np.sum(points > opponent_points)
    episode_stats['away_wins'] = np.sum(points < opponent_points)
    episode_stats['ties'] = np.sum(points == opponent_points)
    return episode_stats

  def _decode_team_stats(self, data):
    arr = np.frombuffer(base64.b64decode(data), dtype='float32')
    # Images/textures in WebGL are layed out in layer for z
    return arr.reshape(int(len(TeamStatsKeys)), -1).transpose().reshape(2, -1, int(len(TeamStatsKeys)))

  async def reload(self):
    """Reload the game"""
    await self.page.reload()
    self.logger.info('[run_session] Waiting for GymLoaded')
    await self.page.waitForSelector('.GymLoaded')
    self.logger.info('[run_session] Gym loaded ok')

  @property
  def running(self):
    """Returns true if the app is still running"""
    return self.browser.process.poll() is None

  def _handle_console(self, m):
    if m.type == 'error':
      self.logger.error('[console] %s', m.text)
    elif m.type == 'warning':
      self.logger.warning('[console] %s', m.text)
    else:
      self.logger.info('[console] %s', m.text)

  def get_webgl_renderer(self) -> str:
    """Return which webgl renderer is being used by the game"""
    return asyncio.get_event_loop().run_until_complete(self.async_get_webgl_renderer())

  async def async_get_webgl_renderer(self):
    """Async version of :meth:`get_webgl_renderer`"""
    return await self.page.evaluate('''() => window.derk.getWebGLRenderer()''')
