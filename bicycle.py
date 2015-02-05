#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the bicycle domain.  

'''
bicycle STATESPACE 
'''
#   You may add only standard python imports---i.e., ones that are automatically
#   available on CDF.
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

from search import *
from random import randint
from math import sqrt

class bicycle(StateSpace):
	_MAX_WEIGHT = 10000

	def __init__(self, action, gval, state, loc_map, job_list, parent=None):
#IMPLEMENT
	'''Initialize a bicycle search state object.'''
	if action == 'START':   #NOTE action = 'START' is treated as starting the search space
		StateSpace.n = 0
				
	StateSpace.__init__(self, action, gval, parent)
	#implement the rest of this function.
	self.map = map
	self.job_list = job_list
	self.max_weight = max_weight
		
	def successors(self): 
#IMPLEMENT
		'''Return list of bicycle objects that are the successors of the current object'''
		States = list()
		
		# Location is home, can only perform first_pickup actions
		if get_loc(self) == 'home':
			for job_name in get_unstarted(self):
				job_info = get_job_info(job_list, job_name)
				job_pickup_location = job_info[1]
				job_pickup_time = job_info[2]                
				job_destination_location = job_info[3]
				job_weight = job_info[4]
				
				# Cannot perform a first_pickup action if adding the job to the jobs already carried
				# by the courier causes the total weight carried to exceed the courier's limit.
				if job_weight + get_load(self) <= get_max_weight(self):
					new_state = {"jobs_carried": list(get_carrying(self)).append(job_name),
								"jobs_carried_weight":  job_weight + get_load(self),
								"location": job_pickup_location,
								"time": job_pickup_time,
								"earnings": get_earned(self),
								"jobs_not_started": list(jobs_not_started).remove(job_name)}
					action = "first_pickup(" + job_name + ")"	
					States.append(bicycle(action, self.gval, new_state, map, job_list, self))
					
		# Location is not home, can only perform pickup or deliver actions
		else:
			# Pickup actions
			for job_name in get_unstarted(self):
				job_info = get_job_info(job_list, job_name)
				job_pickup_location = job_info[1]
				job_pickup_time = job_info[2]                
				job_destination_location = job_info[3]
				job_weight = job_info[4]
			
				# Cannot perform a pickup action if adding the job to the jobs already carried
				# by the courier causes the total weight carried to exceed the courier's limit.
				if job_weight + get_load(self) <= get_max_weight(self):
					# The courier is not allowed to perform a pickup(<job name>) action if the pickup 
					# location of <job name> is the same as the delivery location of some package 
					# currently being carried.
					cannot_pickup = False
				
					for carried_job_name in self.state['jobs_carried']:
						carried_job_info = get_job_info(job_list, carried_job_name)
						carried_job_destination_location = carried_job_info[3]
						if job_pickup_location == carried_job_destination_location:
							cannot_pickup == True
							break

					if cannot_pickup = False:
						new_state = {"jobs_carried": list(get_carrying(self)).append(job_name),
									"jobs_carried_weight":  job_weight + get_load(self),
									"location": job_pickup_location,
									"time": job_pickup_time,
									"earnings": get_earned(self),
									"jobs_not_started": list(jobs_not_started).remove(job_name)}
						action = "pickup(" + job_name + ")"
						States.append(bicycle(action, self.gval, new_state, map, job_list, self))

			# Deliver actions
			for job_name in get_carrying(self):
				job_info = get_job_info(job_list, job_name)
				job_pickup_location = job_info[1]
				job_pickup_time = job_info[2]                
				job_destination_location = job_info[3]
				job_weight = job_info[4]

				
	


		return States
	
	def hashable_state(self) :
#IMPLEMENT
		'''Return a data item that can be used as a dictionary key to UNIQUELY represent the state.'''
		return ()
	def print_state(self):
		#DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
		#and in generating sample trace output. 
		#Note that if you implement the "get" routines below properly, 
		#This function should work irrespective of how you represent
		#your state. 

		if self.parent:
			print("Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index))
		else:
			print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))
			
		print("    Carrying: {} (load {} grams)".format(
					  self.get_carrying(), self.get_load()))
		print("    State time = {} loc = {} earned so far = {}".format(
					  self.get_time(), self.get_loc(), self.get_earned()))
		print("    Unstarted Jobs.{}".format(self.get_unstarted()))

	def get_job_info(job_name, job_list):
		''' Given a job name return its corresponding entry in job_list. 
			Assume there always exists a corresponding entry. '''
		for index in range(len(job_list)):
			if job_list[index][0] == job_name:
				return job_list[index]
			
	def get_travel_time(locA, locB, map):
		''' Given two locations return the associated travel time in map.
			Assume there always exists a corresponding entry. '''
		check = False
		
		for index in range(len(map[1])):
			check = all(x in map[1][index] for x in [locA, locB])
			if check == True:
				break
		
		return map[1][index][2]
		
	def get_max_weight(self):
		return self._MAX_WEIGHT

	def get_loc(self):
#IMPLEMENT
		'''Return location of courier in this state'''
		return self.state['location']
	
	def get_carrying(self):
#IMPLEMENT
		'''Return list of NAMES of jobs being carried in this state'''
		return self.state['jobs_carried']
	
	def get_load(self):
#IMPLEMENT
		'''Return total weight being carried in this state'''
		return self.state['jobs_carried_weight']
	
	def get_time(self):
#IMPLEMENT
		'''Return current time in this state'''
		return self.state['time']
	
	def get_earned(self):
#IMPLEMENT
		'''Return amount earned so far in this state'''
		return self.state['earnings']
	
	def get_unstarted(self):
#IMPLEMENT
		'''Return list of NAMES of jobs not yet stated in this state''' 
		return self.state['jobs_not_started']
	
def heur_null(state):
	'''Null Heuristic use to make A* search perform uniform cost search'''
	return 0

def heur_sum_delivery_costs(state):
#IMPLEMENT
	'''Bicycle Heuristic sum of delivery costs.'''
	#Sum over every job J being carried: Lost revenue if we
	#immediately travel to J's dropoff point and deliver J.
	#Plus 
	#Sum over every unstarted job J: Lost revenue if we immediately travel to J's pickup 
	#point then to J's dropoff poing and then deliver J.

def heur_max_delivery_costs(state):
#IMPLEMENT
	'''Bicycle Heuristic sum of delivery costs.'''
	#m1 = Max over every job J being carried: Lost revenue if we immediately travel to J's dropoff
	#point and deliver J.
	#m2 = Max over every unstarted job J: Lost revenue if we immediately travel to J's pickup 
	#point then to J's dropoff poing and then deliver J.
	#heur_max_delivery_costs(state) = max(m1, m2)


def bicycle_goal_fn(state):
#IMPLEMENT
	'''Have we reached the goal (where all jobs have been delivered)?'''

def make_start_state(map, job_list):
#IMPLEMENT
	'''Input a map list and a job_list. Return a bicycle StateSpace object
	with action "START", gval = 0, and initial location "home" that represents the 
	starting configuration for the scheduling problem specified'''
	
	for job in job_list:
		jobs_not_started.append(job[0]);
	
	state = {"jobs_carried": [],
			"jobs_carried_weight": 0,
			"location": "home",
			"time": 420,
			"earnings": 0,
			"jobs_not_started": jobs_not_started}

	start_state = bicycle("START", 0, state, map, job_list)
	return start_state

########################################################
#   Functions provided so that you can more easily     #
#   Test your implementation                           #
########################################################

def make_rand_map(nlocs):
	'''Generate a random collection of locations and distances 
	in input format'''
	lpairs = [(randint(0,50), randint(0,50)) for i in range(nlocs)]
	lpairs = list(set(lpairs))  #remove duplicates
	nlocs = len(lpairs)
	lnames = ["loc{}".format(i) for i in range(nlocs)]
	ldists = list()

	for i in range(nlocs):
		for j in range(i+1, nlocs):
			ldists.append([lnames[i], lnames[j],
						   int(round(euclideandist(lpairs[i], lpairs[j])))])
	return [lnames, ldists]

def dist(l1, l2, map):
	'''Return distance from l1 to l2 in map (as output by make_rand_map)'''
	ldist = map[1]
	if l1 == l2:
		return 0
	for [n1, n2, d] in ldist:
		if (n1 == l1 and n2 == l2) or (n1 == l2 and n2 == l1):
			return d
	return 0
	
def euclideandist(p1, p2):
	return sqrt((p1[0]-p2[0])*(p1[0]-p2[0]) + (p1[1]-p2[1])*(p1[1]-p2[1]))

def make_rand_jobs(map, njobs):
	'''input a map (as output by make_rand_map) object and output n jobs in input format'''
	jobs = list()
	for i in range(njobs):
		name = 'Job{}'.format(i)
		ploc = map[0][randint(0,len(map[0])-1)]
		ptime = randint(7*60, 16*60 + 30) #no pickups after 16:30
		dloci = randint(0, len(map[0])-1)
		if map[0][dloci] == ploc:
			dloci = (dloci + 1) % len(map[0])
		dloc = map[0][dloci]
		weight = randint(10, 5000)
		job = [name, ploc, ptime, dloc, weight]
		payoffs = list()
		amount = 50
		#earliest delivery time
		time = ptime + dist(ploc, dloc, map)
		for j in range(randint(1,5)): #max of 5 payoffs
			time = time + randint(5, 120) #max of 120mins between payoffs
			amount = amount - randint(5, 25)
			if amount <= 0 or time >= 19*60:
				break
			payoffs.append([time, amount])
		job.append(payoffs)
		jobs.append(job)
	return jobs

def test(nloc, njobs):
	map = make_rand_map(nloc)
	jobs = make_rand_jobs(map, njobs)
	print("Map = ", map)
	print("jobs = ", jobs)
	s0 = make_start_state(map, jobs)
	print("heur Sum = ", heur_sum_delivery_costs(s0))
	print("heur max = ", heur_max_delivery_costs(s0))
	se = SearchEngine('astar', 'full')
	#se.trace_on(2)
	final = se.search(s0, bicycle_goal_fn, heur_max_delivery_costs)
	

### TESTING AREA
if __name__ == '__main__':
	job_list = [['Job1', 'locA', 480, 'locC', 5000, [[510, 25], [570, 20], [600, 10], [660, 5]]],
				['Job2', 'locB', 600, 'locC', 5000, [[630, 25], [730, 5]]],
				['Job3', 'locC', 540, 'locD', 10000, [[545, 50], [570, 25], [600, 5]]]]
	
	map = [['loc0', 'loc1', 'loc2', 'loc3', 'loc4', 'loc5', 'loc6', 'loc7', 'loc8'], 
			[['loc0', 'loc1', 33], ['loc0', 'loc2', 6], ['loc0', 'loc3', 28], ['loc0', 'loc4', 7], 
			['loc0', 'loc5', 47], ['loc0', 'loc6', 21], ['loc0', 'loc7', 7], ['loc0', 'loc8', 22], 
			['loc1', 'loc2', 39], ['loc1', 'loc3', 31], ['loc1', 'loc4', 39], ['loc1', 'loc5', 16], 
			['loc1', 'loc6', 39], ['loc1', 'loc7', 26], ['loc1', 'loc8', 18], ['loc2', 'loc3', 32], 
			['loc2', 'loc4', 5], ['loc2', 'loc5', 52], ['loc2', 'loc6', 22], ['loc2', 'loc7', 13], 
			['loc2', 'loc8', 27], ['loc3', 'loc4', 28], ['loc3', 'loc5', 47], ['loc3', 'loc6', 48], 
			['loc3', 'loc7', 25], ['loc3', 'loc8', 14], ['loc4', 'loc5', 53], ['loc4', 'loc6', 26], 
			['loc4', 'loc7', 13], ['loc4', 'loc8', 25], ['loc5', 'loc6', 46], ['loc5', 'loc7', 40], 
			['loc5', 'loc8', 34], ['loc6', 'loc7', 23], ['loc6', 'loc8', 36], ['loc7', 'loc8', 15]]]
	return 0
	