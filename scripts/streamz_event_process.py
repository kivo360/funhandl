import asyncio
import random
import sys
import threading
import uuid
from copy import deepcopy
from time import sleep
from abc import ABC
import numpy as np
import pandas as pd
from dask.distributed import Client, Lock
from loguru import logger
from streamz import Stream
from tornado import gen

np.random.seed(2) 

client = Client(processes=False)

logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>")
# logger.add(sys.stderr, format="{time} {message}", filter="my_module", level="INFO")
logger.add("file{time}.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")



source = Stream()
check_emission = Stream()
class SerizableEvent(ABC):
	def __init__(self):
		pass
	
	def __setattr__(self, name, value):
		self.__dict__[name] = value


class LearningEvent(SerizableEvent):
	def __init__(self, state, action, reward, result, done):
		super().__init__()
		self.__dict__ = {
			"state": state,
			"action": action, 
			"reward": reward, 
			"result": result, 
			"done": done
		}
	


# 1. Create sims (random list) with names
# 2. Get list of sims (the name/id of the sim)
# 3. Emit the name of the sim to a function
# 4. Step through the event with the given name

N_STATES = 6   # the length of the 1 dimensional world
ACTIONS = ['LEFT', 'RIGHT']     # available actions
EPSILON = 0.9   # greedy police
ALPHA = 0.1     # learning rate
GAMMA = 0.9    # discount factor
MAX_EPISODES = 13   # maximum episodes
FRESH_TIME = 0.3    # fresh time for one move






class Actor(object):
	def __init__(self):
		"""
			The actor here gets creates a table based on the number of states and available actions
		"""
		self.table = None
		self.actions = ACTIONS
		self.last_action = {}
		# self.lr = learning_rate
		# self.gamma = reward_decay
		# self.epsilon = e_greedy
		self.build_q_table(N_STATES, ACTIONS)
		

	def build_q_table(self, n_states, actions):
		table = pd.DataFrame(
			np.zeros((n_states, len(actions))),     # q_table initial values
			columns=actions,    # actions's name
		)
		self.table = table
	
	def learn(self, **kwargs):
		_id = kwargs.get("_id", None)
		previous = kwargs.get("prev", None)
		current = kwargs.get("current", None)
		reward = kwargs.get("reward", None)
		is_done = kwargs.get("done", False)

		# is_done = kwargs.get("done", None)
		
		try:
			self.last_action[_id]
		except KeyError:
			logger.error("Key {} not found for last action".format(_id))
			return
		q_predict = self.table.loc[previous, self.last_action[_id]]

		if is_done == False:
			q_target = reward + GAMMA * self.table.iloc[current, :].max()
		else:
			q_target = reward

		self.table.loc[current, self.last_action[_id]] += ALPHA * (q_target - q_predict)
		# return is_done



	def decide(self, state, _id):
		# This is how to choose an action
		state_actions = self.table.iloc[state, :]
		if (np.random.uniform() > EPSILON) or ((state_actions == 0).all()):  # act non-greedy or state-action have no value
			action_name = np.random.choice(ACTIONS)
		else:   # act greedy
			action_name = state_actions.idxmax()    # replace argmax to idxmax as argmax means a different function in newer version of pandas
		# logger.info(type(self.last_action))
		# logger.info(type(str(_id)))
		# self.last_action[str(_id)] = 0

		self.last_action[_id] = action_name
		# logger.info()
		return action_name
	
	# def get_env_feedback(self, S, A):
	# 	# This is how agent will interact with the environment
	# 	if A == 'right':    # move right
	# 		if S == N_STATES - 2:   # terminate
	# 			S_ = 'terminal'
	# 			R = 1
	# 		else:
	# 			S_ = S + 1
	# 			R = 0
	# 	else:   # move left
	# 		R = 0
	# 		if S == 0:
	# 			S_ = S  # reach the wall
	# 		else:
	# 			S_ = S - 1
	# 	return S_, R




		# print(table)    # show table

class Simulation(object):
	def __init__(self):
		# The simulation is a lot like an environment. Load the episodes for the enviornment
		self.episodes = list(np.random.uniform(low=0.5, high=13.3, size=70))
		self.S = 0
		self.laststate = 0
		self._id = str(uuid.uuid1())
		self.current = None
		self.total_state = []
		self.step_counter = 0


		self.env_list = ['-']*(N_STATES-1) + ['T']   # '---------T' our environment
		
		# if S == 'terminal':
		# 	interaction = 'Episode %s: total_steps = %s' % (episode+1, step_counter)
		# 	print('\r{}'.format(interaction), end='')
		# 	time.sleep(2)
		# 	print('\r                                ', end='')
		# else:
		# 	env_list[S] = 'o'
		# 	interaction = ''.join(env_list)
		# 	print('\r{}'.format(interaction), end='')
		# 	time.sleep(FRESH_TIME)


	def current_state(self):
		return self.S

	def step(self, action, **kwargs):
		# We'd run through every part of the process here
		# For agent based modeling the components would be here
		# self.current = self.episodes.pop()
		# processed = self.current
		self.laststate = deepcopy(self.S)
		action = str(action).upper()
		done = False
		reward = 0
		# We try sending in a new state
		if action == 'RIGHT':    # move right
			if self.S == N_STATES - 2:   # terminate
				done = True				
				reward = 1
			else:
				self.S += 1
				reward = 0
		if action == "LEFT":   # move left
			if self.S == 0:
				self.S = self.S  # reach the wall
			else:
				self.S -= self.S
		# return S_, R

		# if action == "LEFT":
		# 	# processed = self.current*2
		# 	logger.info("Applying Left", enqueue=True)
		# elif action == "RIGHT":
		# 	# processed = self.current*15
		# 	logger.info("Applying Right", enqueue=True)
		

		# self.total_state.append(processed)
		# # print("Doing processing here: {}".format(self.current))

		# done = False
		# if len(self.episodes) == 0:
		# 	done = True
		
		self.step_counter += 1
		# logger.info(self.step_counter)
		# logger.info(self.total_state)
		return self.laststate, self.S, reward, done
		# Pops through an element and stores the currently observed state as current
		# self.episodes.


class SimulationController(object):
	def __init__(self, **kwargs):
		# print("Create simulations")
		self.simulations = {}
		# self.lock = Lock()
		# We'd run through various sims with ray remote and store internally
		episodes = kwargs.get("episodes", MAX_EPISODES)
		for _ in range(episodes):
			# These would be remotely accessible using ray
			sim = Simulation()
			self.simulations[sim._id] = sim
	
	
	
	def get_list_of_sims(self):
		""" """
		return self.simulations.keys()

	def get_current(self, **kwargs):
		_id = kwargs.get("_id")
		return self.simulations[_id].current_state()

	def get_last(self, **kwargs):
		_id = kwargs.get("_id")
		return self.simulations[_id].laststate
	def info(self, _id):
		counter = self.simulations[_id].step_counter
		return "Simulation-ID: {}, Number Of Iterations: {}".format(_id, counter)

	def step(self, **kwargs):
		
		_id = kwargs.get("_id", None)
		action = kwargs.get("action", None)

		if _id is None:
			raise AttributeError("Id not found")
		
		last, current, reward, done = self.simulations[_id].step(action)
		# Maybe push the learning to another step
		# actor.learn(prev=self.simulations[_id].laststate, current=self.simulations[_id].current_state(), done=done)
		return last, current, reward, done
	

	


simmy = SimulationController(episodes=10)
actor = Actor()



	


def take_next(x):
	# Get the current state of a simulation by ID
	current_state = simmy.get_current(_id=x)
	action = actor.decide(current_state, x)
	# action = actor.decide(current_state)
	last, current, reward, done = simmy.step(_id=x, action=action)
	se = SerizableEvent()
	se.reward = reward
	se.last = last
	se.current = current
	se.done = done
	se._id = x
	se.current = current
	return se

def take_note(event):
	actor.learn(prev=event.last, current=event.current, reward=event.reward, done=event.done, _id=event._id)
	return event

def is_done(s):

	logger.info(simmy.info(s._id))
	if s.done == False:
		return True
	else:
		return False


# @logger.catch
def reemit(s):
	# event = s.result()
	source.emit(s._id)

@logger.catch
def main():
	
	sim_list = simmy.get_list_of_sims()
	for _ in sim_list:
		source.emit(_)



# I can instead package everything into a Session object and single stream everything.
# Dask Distributed scheduler will be used inside of the session object.
# count = 

(source.map(take_next)
		.map(take_note)
		.filter(is_done).sink(reemit))

if __name__ == "__main__":
	main()
	# print("Running the streamz here. Should include dask-distributed and kubernetes here")
