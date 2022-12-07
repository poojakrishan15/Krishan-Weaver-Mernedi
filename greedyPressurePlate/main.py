from pressureplate import *
from greedyMA import *
import gym

env = gym.make('pressureplate-linear-4p-v0')
qAgent = QLAgent(env, total_epi=1000)
qAgent.learn() 
env.close()
