#Look for #IMPLEMENT tags in this file. These tags indicate changes in the
#file to implement the required routines.


'''8-Puzzle STATESPACE
'''
from search import *

class eightPuzzle(StateSpace):
    StateSpace.n = 0

    # Class variable used to determine the successors of any given state.
    #
    # DO NOT MODIFY THIS STRUCTURE!
    #
    # Warning: Prevention of any any changes made to this structure is not
    #          enforced explicitly.
    _successors_map = { 0 :  [{"DOWN": 3}, {"RIGHT": 1}],
                        1 :  [{"DOWN": 4}, {"RIGHT":2}, {"LEFT": 0}],
                        2 :  [{"DOWN": 5}, {"LEFT": 1}],
                        3 :  [{"DOWN": 6}, {"UP": 0}, {"RIGHT": 4}],
                        4 :  [{"DOWN": 7}, {"UP": 1}, {"RIGHT": 5}, {"LEFT": 3}],
                        5 :  [{"DOWN": 8}, {"UP": 2}, {"LEFT": 4}],
                        6 :  [{"UP": 3}, {"RIGHT": 7}],
                        7 :  [{"UP": 4}, {"RIGHT": 8}, {"LEFT": 6}],
                        8 :  [{"UP": 5}, {"LEFT": 7}] };

    def __init__(self, action, gval, state, parent = None):
        '''Create an 8-puzzle state object.
        The parameter state represents the puzzle configation as a list of 9 numbers in the range [0-8]
        The 9 numbers specify the position of the tiles in the puzzle from the
        top left corner, row by row, to the bottom right corner. E.g.:

        [2, 4, 5, 0, 6, 7, 8, 1, 3] represents the puzzle configuration

        |-----------|
        | 2 | 4 | 5 |
        |-----------|
        |   | 6 | 7 |
        |-----------|
        | 8 | 1 | 3 |
        |-----------|
        '''
        #Note we represent the puzzle configuration in the state member.
        #the list of tile positions.
        StateSpace.__init__(self, action, gval, parent)
        self.state = state

        # The zero_tile attribute represents the index of the zero tile into
        # the state attribute, which is a list.
        self.zero_tile = self.state.index(0);

    def successors(self) :
#IMPLEMENT
        '''Implement the actions of the 8-puzzle search space.'''
        #   IMPORTANT. The list of successor states returned must be in the ORDER
        #   Move blank down, move blank up, move blank right, move blank left
        #   (with some successors perhaps missing if they are not available
        #   moves from the current state, but the remaining ones in this
        #   order!)

        States = list()

        for mapping in self._successors_map[self.zero_tile] :

            # A mapping has the form {'ACTION' : 'SWAP INDEX'}
            succ_action = list(mapping.keys())[0]
            swap_index = mapping[succ_action]

            succ_state = list(self.state)
            succ_state[swap_index], succ_state[self.zero_tile] = succ_state[self.zero_tile], succ_state[swap_index];

            States.append(eightPuzzle(succ_action, self.gval+1, succ_state, self))

        return States

    def hashable_state(self) :
#IMPLEMENT
        return tuple(self.state)

    def print_state(self):
#DO NOT CHANGE THIS METHOD
        if self.parent:
            print("Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index))
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))


        print("|-----------|")
        print("| {} | {} | {} |".format(self.state[0],self.state[1],self.state[2]))
        print("|-----------|")
        print("| {} | {} | {} |".format(self.state[3],self.state[4],self.state[5]))
        print("|-----------|")
        print("| {} | {} | {} |".format(self.state[6],self.state[7],self.state[8]))
        print("|-----------|")

#Set up the goal.
#We allow any full configuration of the puzzle to be a goal state.
#We use the class variable "eightPuzzle.goal_state" to store the goal configuration.
#The goal test function compares a state's configuration with the goal configuration

eightPuzzle.goal_state = False

def eightPuzzle_set_goal(state):
    '''set the goal state to be state. Here state is a list of 9
       numbers in the same format as eightPuzzle.___init___'''
    eightPuzzle.goal_state = state

def eightPuzzle_goal_fn(state):
    return (eightPuzzle.goal_state == state.state)

def heur_zero(state):
    '''Zero Heuristic use to make A* search perform uniform cost search'''
    return 0

def h_misplacedTiles(state):
#IMPLEMENT
    #return the number of tiles (NOT INCLUDING THE BLANK) in state that are not in their goal
    #position. (will need to access the class variable eigthPuzzle.goal_state)
    misplacedTiles = 0
    
    for index in range(len(state.state)):
        # Skip the zero tile
        if state.state[index] == 0:
            continue
        
        if state.state[index] != eightPuzzle.goal_state[index]:
            misplacedTiles += 1
            
    return misplacedTiles

def h_MHDist(state):
    #return the sum of the manhattan distances each tile (NOT INCLUDING
    #THE BLANK) is from its goal configuration.
    #The manhattan distance of a tile that is currently in row i column j
    #and that has to be in row x column y in the goal is defined to be
    #  abs(i - x) + abs(j - y)
    
    mhDist = 0
    
    for index in range(len(state.state)):
        # Skip the zero tile
        if state.state[index] == 0:
            continue
        
        # TODO
        
    return mhDist

#if __name__ == "__main__":
    
    #se = SearchEngine('astar', 'full')
    
    ## Test Group 1
    #eightPuzzle_set_goal([1, 2, 3, 8, 0, 4, 7, 6, 5])
    ## Easy
    #s2 = eightPuzzle("START", 0, [1, 3, 4, 8, 6, 2, 7, 0, 5])    
    
    #print("===========Test 1, EASY, ASTAR, h_misplacedTiles======")
    #se.search(s2, eightPuzzle_goal_fn, h_misplacedTiles)    