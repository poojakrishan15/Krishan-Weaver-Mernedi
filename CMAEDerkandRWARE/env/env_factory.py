"""Implements a model factory."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import functools
from env.rooms import Rooms
from env.secret_rooms import SecretRooms
from env.push_box import PushBox
from env.rwh import Warehouse
from gym_derk.envs import DerkEnv
from env.lbforaging import ForagingEnv


ENV_MAP = {
    'room30': functools.partial(Rooms, H=300, grid_size=30, n_actions=4, n_agents=2),
    'room30_ckpt': functools.partial(Rooms, H=300, grid_size=30, n_actions=4, n_agents=2, checkpoint=True),
    'secret_room': functools.partial(SecretRooms, H=300, grid_size=25, n_actions=4, n_agents=2),
    'secret_room_ckpt': functools.partial(SecretRooms, H=300, grid_size=25, n_actions=4, n_agents=2, checkpoint=True),
    'push_box': functools.partial(PushBox, H=300, grid_size=10, n_actions=4, n_agents=2),
    'push_box_ckpt': functools.partial(PushBox, H=300, grid_size=15, n_actions=4, n_agents=2, checkpoint=True),
    'rwh': functools.partial(Warehouse, 9, 8, 3, 10, 3, 1, 5, None, None, 0),
    'derk': functools.partial(DerkEnv),
    'lbf':functools.partial(ForagingEnv,grid_size = 5,field_size=(5,5),players=2, max_player_level=3,max_food=3, sight=1,max_episode_steps=50,force_coop=True)
}


def get_env(name):
  assert name in ENV_MAP
  return ENV_MAP[name]
