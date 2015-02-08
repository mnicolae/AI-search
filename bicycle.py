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

class bicycleStateInfo:
    def __init__ (self, jobs_carried, jobs_carried_weight, location, time, earnings, jobs_not_started):
        ''' Initialize a bicycleStateInfo object. '''
        self.jobs_carried = jobs_carried
        self.jobs_carried_weight = jobs_carried_weight
        self.location = location
        self.time = time
        self.earnings = earnings
        self.jobs_not_started = jobs_not_started

class bicycle(StateSpace):
    _MAX_WEIGHT = 10000
    _MAX_DELIVER = 1140
    
    def __init__(self, action, gval, state, loc_map, job_list, parent=None):
#IMPLEMENT
        '''Initialize a bicycle search state object.'''
        if action == 'START':    #NOTE action = 'START' is treated as starting the search space
            StateSpace.n = 0
                
        StateSpace.__init__(self, action, gval, parent)
        #implement the rest of this function.
        self.state = state
        self.loc_map = loc_map
        self.job_list = job_list

    def successors(self): 
#IMPLEMENT
        '''Return list of bicycle objects that are the successors of the current object'''
        States = list()

        # Location is home, can only perform first_pickup actions
        if self.get_loc() == 'home':
            # first_pickup actions
            for job_name in self.get_unstarted():
                job_info = get_job_info(job_name, self.get_job_list())
                job_pickup_location = job_info[1]
                job_pickup_time = job_info[2]             
                job_destination_location = job_info[3]
                job_weight = job_info[4]
                
                # Cannot perform a first_pickup action if adding the job to the jobs already carried
                # by the courier causes the total weight carried to exceed the courier's limit.
                if self.get_load() + job_weight <= self.get_max_weight():
                    new_jobs_carried = list(self.get_carrying())
                    new_jobs_carried.append(job_name)
                    new_jobs_not_started = list(self.get_unstarted())
                    new_jobs_not_started.remove(job_name)
                    new_state = bicycleStateInfo(new_jobs_carried, \
                                                 self.get_load() + job_weight, \
                                                 job_pickup_location, \
                                                 job_pickup_time, \
                                                 self.get_earned(), \
                                                 new_jobs_not_started)
                    
                    action = "first_pickup(" + job_name + ")"    
                    States.append(bicycle(action, self.gval, new_state, self.get_loc_map(), self.get_job_list(), self))
                
        # Location is not home, can only perform pickup or deliver actions
        else:
            # pickup actions
            for job_name in self.get_unstarted():
                job_info = get_job_info(job_name, self.get_job_list())
                job_pickup_location = job_info[1]
                job_pickup_time = job_info[2]             
                job_destination_location = job_info[3]
                job_weight = job_info[4]
            
                # Cannot perform a pickup action if adding the job to the jobs already carried
                # by the courier causes the total weight carried to exceed the courier's limit.
                if self.get_load() + job_weight <= self.get_max_weight():
                    # The courier is not allowed to perform a pickup action if the pickup 
                    # location is the same as the delivery location of some package 
                    # currently being carried.
                    cannot_pickup = False   
                    for carried_job_name in self.get_carrying():
                        carried_job_info = get_job_info(carried_job_name, self.get_job_list())
                        carried_job_destination_location = carried_job_info[3]
                        if job_pickup_location == carried_job_destination_location:
                            cannot_pickup = True

                    if cannot_pickup == False:
                        travel_time = get_travel_time(self.get_loc(), job_pickup_location, self.get_loc_map())
                        new_state_time = self.get_time() + travel_time
                        
                        new_jobs_carried = list(self.get_carrying())
                        new_jobs_carried.append(job_name)
                        new_jobs_not_started = list(self.get_unstarted())
                        new_jobs_not_started.remove(job_name)
                        new_state = bicycleStateInfo(new_jobs_carried, \
                                                    self.get_load() + job_weight, \
                                                    job_pickup_location, \
                                                    max(new_state_time, job_pickup_time), \
                                                    self.get_earned(), \
                                                    new_jobs_not_started)
                        
                        action = "pickup(" + job_name + ")"
                        States.append(bicycle(action, self.gval, new_state, self.get_loc_map(), self.get_job_list(), self))

            # Deliver actions
            for job_name in self.get_carrying():
                job_info = get_job_info(job_name, self.get_job_list())
                job_pickup_location = job_info[1]
                job_pickup_time = job_info[2]             
                job_destination_location = job_info[3]
                job_weight = job_info[4]
                                        
                travel_time = get_travel_time(self.get_loc(), job_destination_location, self.get_loc_map())
                new_state_time = self.get_time() + travel_time
                job_earning = get_job_earning(new_state_time, job_name, self.get_job_list())
                
                # Cannot perform a deliver action if the job is delivered 
                # past the end of the day time.
                if new_state_time <= self.get_max_deliver():
                    new_jobs_carried = list(self.get_carrying())
                    new_jobs_carried.remove(job_name)
                    new_jobs_not_started = list(self.get_unstarted())
                    new_state = bicycleStateInfo(new_jobs_carried, \
                                                self.get_load() - job_weight, \
                                                job_destination_location, \
                                                new_state_time, \
                                                self.get_earned() + job_earning, \
                                                new_jobs_not_started)
                    
                    action = "deliver(" + job_name + ")"
                    new_gval = self.gval + get_job_loss(new_state_time, job_name, self.get_job_list())
                    States.append(bicycle(action, new_gval, new_state, self.get_loc_map(), self.get_job_list(), self))

        return States
    
    def hashable_state(self) :
#IMPLEMENT
        '''Return a data item that can be used as a dictionary key to UNIQUELY represent the state.'''
        # TODO
    
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

    #
    # Custom methods start here
    #
    def get_loc_map(self):
        return self.loc_map

    def get_job_list(self):
        return self.job_list

    def get_max_weight(self):
        return self._MAX_WEIGHT

    def get_max_deliver(self):
        return self._MAX_DELIVER
    #
    # Custom methods end here
    #

    def get_loc(self):
#IMPLEMENT
        '''Return location of courier in this state'''
        return self.state.location
    
    def get_carrying(self):
#IMPLEMENT
        '''Return list of NAMES of jobs being carried in this state'''
        return self.state.jobs_carried
    
    def get_load(self):
#IMPLEMENT
        '''Return total weight being carried in this state'''
        return self.state.jobs_carried_weight
    
    def get_time(self):
#IMPLEMENT
        '''Return current time in this state'''
        return self.state.time
    
    def get_earned(self):
#IMPLEMENT
        '''Return amount earned so far in this state'''
        return self.state.earnings
    
    def get_unstarted(self):
#IMPLEMENT
        '''Return list of NAMES of jobs not yet stated in this state''' 
        return self.state.jobs_not_started

#
# Custom functions start here
#
def get_job_info(job_name, job_list):
    ''' Given a job name return its corresponding entry in job_list. 
        Assume there always exists a corresponding entry. '''
    for index in range(len(job_list)):
        if job_list[index][0] == job_name:
            return job_list[index]

def get_travel_time(locA, locB, loc_map):
    ''' Given two locations return the associated travel time in map.
        Assume there always exists a corresponding entry. '''
    if locA == locB:
        return 0
    
    check = False    
    for index in range(len(loc_map[1])):
        check = all(x in loc_map[1][index] for x in [locA, locB])
        if check == True:
            break
        
    return loc_map[1][index][2]

def get_job_earning(time, job_name, job_list):
    ''' Given a delivery time and a job name return the earning
        achieved when delivering the job at that time. '''
    for index in range(len(job_list)):
        if job_list[index][0] == job_name:
            break
        
    earnings_list = job_list[index][5]
    earning = 0
    
    for elem in earnings_list:
        if time <= elem[0]:
            earning = elem[1]
            break
    
    return earning

def get_job_loss(time, job_name, job_list):
    ''' Given a delivery time and a job name return the loss
        incurred when delivering the job at that time. '''
    for index in range(len(job_list)):
        if job_list[index][0] == job_name:
            break
    
    earnings_list = job_list[index][5]
    earning = 0
    
    for elem in earnings_list:
        if time <= elem[0]:
            earning = elem[1]
            break
            
    earning_loss = earnings_list[0][1] - earning
    return earning_loss
#
# Custom functions end here
#

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
    #point then to J's dropoff point and then deliver J.
    # TODO

def heur_max_delivery_costs(state):
#IMPLEMENT
    '''Bicycle Heuristic sum of delivery costs.'''
    #m1 = Max over every job J being carried: Lost revenue if we immediately travel to J's dropoff
    #point and deliver J.
    #m2 = Max over every unstarted job J: Lost revenue if we immediately travel to J's pickup 
    #point then to J's dropoff poing and then deliver J.
    #heur_max_delivery_costs(state) = max(m1, m2)
    # TODO

def bicycle_goal_fn(state):
#IMPLEMENT
    '''Have we reached the goal (where all jobs have been delivered)?'''
    return len(state.get_carrying()) == 0 and len(state.get_unstarted()) == 0

def make_start_state(loc_map, job_list):
#IMPLEMENT
    '''Input a map list and a job_list. Return a bicycle StateSpace object
    with action "START", gval = 0, and initial location "home" that represents the 
    starting configuration for the scheduling problem specified'''
    
    jobs_not_started = []
    for job in job_list:
        jobs_not_started.append(job[0]);
    
    bStateInfo = bicycleStateInfo([], 0, "home", 420, 0, jobs_not_started)
    start_state = bicycle("START", 0, bStateInfo, loc_map, job_list)
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
