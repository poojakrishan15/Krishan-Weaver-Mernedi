import random
import gym
import time
import numpy as np
from pyparsing import Any

def argmax_action(d: dict[Any,float]) -> Any:
    """return a key of the maximum value in a given dictionary 

    Args:
        d (dict[Any,float]): dictionary

    Returns:
        Any: a key
    """
    curMax = -100000
    curGreedyAction = -1
    for action in d:
        if d[action] > curMax:
            curMax = d[action]
            curGreedyAction = action
    return curGreedyAction

class ValueRLAgent():
    def __init__(self, env: gym.Env, gamma : float = 0.98, eps: float = 0.2, alpha: float = 0.02, total_epi: int = 5_000) -> None:
        """initialize agent parameters
        This class will be a parent class and not be called directly.

        Args:
            env (gym.Env): gym environment
            gamma (float, optional): a discount factor. Defaults to 0.98.
            eps (float, optional): the epsilon value. Defaults to 0.2. Note: this pa uses a simple eps-greedy not decaying eps-greedy.
            alpha (float, optional): a learning rate. Defaults to 0.02.
            total_epi (int, optional): total number of episodes an agent should learn. Defaults to 5_000.
        """
        self.env = env
        self.q = self.init_qtable(136, 5)
        #self.q = self.init_qtable(env.observation_space.n, env.action_space.n)
        self.gamma = gamma
        self.eps = eps
        self.alpha = alpha
        self.total_epi = total_epi
    
    def init_qtable(self, n_states: int, n_actions: int, init_val: float = 0.0) -> dict[int,dict[int,float]]:
        """initialize the q table (dictionary indexed by s, a) with a given init_value

        Args:
            n_states (int, optional): the number of states. Defaults to int.
            n_actions (int, optional): the number of actions. Defaults to int.
            init_val (float, optional): all q(s,a) should be set to this value. Defaults to 0.0.

        Returns:
            dict[int,dict[int,float]]: q table (q[s][a] -> q-value)
        """
        masterTable = list()
        for i in range(4):
            qTable = dict()
            for state in range(n_states):
                curActionDic = dict()
                for action in range(n_actions):
                    curActionDic[action] = init_val
                qTable[state] = curActionDic
            masterTable.append(qTable)
        return masterTable      

class QLAgent(ValueRLAgent):  
    def learn(self):
        """Q-Learning algorithm
        Update the Q table (self.q) for self.total_epi number of episodes.

        The results should be reflected to its q table.
        """  
        stepList = list() 
        print(self.total_epi)
        for itor in range(self.total_epi):        
            #generate an episode
            #initialize s
            s = self.env.reset()
            actionList = list()
            a0 = self.choose_action(0, 9 * s[0][-1] + s[0][-2])
            a1 = self.choose_action(1, 9 * s[1][-1] + s[1][-2])
            a2 = self.choose_action(2, 9 * s[2][-1] + s[2][-2])
            a3 = self.choose_action(3, 9 * s[3][-1] + s[3][-2])
            actionList.append(a0)
            actionList.append(a1)
            actionList.append(a2)
            actionList.append(a3)
            done = False
            # repeate until done
            counter = 0
            while not done:
                self.env.render()
                counter += 1
                time.sleep(0.01)
                #get r s' done?
                #print(actionList)
                ss, r, done, _= self.env.step(actionList)
                if done[3] == False:
                    done = False
                else:
                    done = True
                #take action a
                nextActionList = list()
                a0 = self.choose_action(0,  9 * ss[0][-1] + ss[0][-2])
                a1 = self.choose_action(1, 9 * ss[1][-1] + ss[1][-2])
                a2 = self.choose_action(2, 9 * ss[2][-1] + ss[2][-2])
                a3 = self.choose_action(3, 9 * ss[3][-1] + ss[3][-2])
                nextActionList.append(a0)
                nextActionList.append(a1)
                nextActionList.append(a2)
                nextActionList.append(a3)
                #aa = self.choose_action(ss)
                #update q table
                for i in range(4):
                    self.q[i][9 * s[i][-1] + s[i][-2]][actionList[i]] = self.q[i][9 * s[i][-1] + s[i][-2]][actionList[i]] + (self.alpha * (r[i] + (self.gamma * self.q[i][9 * ss[i][-1] + ss[i][-2]][nextActionList[i]]) - self.q[i][ 9 * s[i][-1] + s[i][-2]][actionList[i]]))

                s = ss
                actionList = nextActionList
            stepList.append(counter)
        with open('./greedyData.txt', 'w') as fp:
            for item in stepList:
                fp.write("%s\n" % item)

    def choose_action(self, agent: int, ss: int) -> int:
        """
        [optional] You may want to override this method.
        """ 
        return(argmax_action(self.q[agent][ss]))