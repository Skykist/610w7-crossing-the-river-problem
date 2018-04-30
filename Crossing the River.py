#Michael Chau
"""
Three missionaries and three cannibals come to a river
and find a boat that holds two people. Everyone must get
across the river to continue on the journey. However, if
the cannibals ever outnumber the missionaries on either bank,
the missionaries will be eaten.

Find a series of crossings that will get everyone safely to
the other side of the river.
"""

import math

class State():
    """
    Initial state should have 3 cannibals and 3 missionaries.
    boat = 1 for having boat on initial bank
    boat = 0 when boat is on the other bank
    """
    def __init__(self, cannibals, missionaries, boat):
        self.cannibals = cannibals
        self.missionaries = missionaries
        self.boat = boat
        self.parent = None

    def is_goal(self):
        return self.cannibals == 0 and self.missionaries == 0
    
    def is_valid(self):
        #check if parameters are within limits
        if 0 <= self.boat <= 1:
            if 0 <= self.missionaries <= 3:
                if 0 <= self.cannibals <= 3:
                    # Check if cannibals outnumber missionaries
                    if self.missionaries < self.cannibals and self.missionaries != 0:
                        return False
                    # Check for the other side
                    if self.missionaries > self.cannibals and self.missionaries != 3:
                        return False
                    else:
                        return True
        else:
            return False
        
    def __str__(self):
        #returns a formatted string for printing when called
        left_bank = "%sM %sC" %(self.missionaries, self.cannibals)
        right_bank = "%sM %sC" %(3-self.missionaries, 3-self.cannibals)
        if self.boat == 1:
            boat = "<==>-------"
        else:
            boat = "-------<==>"
        return "(%s,%s,%s): %s %s %s" %(self.cannibals, self.missionaries, self.boat, left_bank, boat, right_bank)
            
    def __eq__(self, other):
        #for == operation
        return self.cannibals == other.cannibals and self.missionaries == other.missionaries and self.boat == other.boat

    def __hash__(self):
        return hash((self.cannibals, self.missionaries, self.boat))

def successors(cursor):
    # returns list of valid states
    children = [];
    
    def append_child(can, mis):
        #appends valid states to list
        new_state = State(cursor.cannibals + can, cursor.missionaries + mis, boat_pos)
        
        if new_state.is_valid():
            #new state will point to a parent
            new_state.parent = cursor
            children.append(new_state)
        '''
        #this is for testing
        else: print (new_state, "is not valid")
        '''
    #if boat is on left
    if cursor.boat == 1:
        boat_pos = 0 #changes boat to right for new states
        append_child(-1,-1) #moves mis and can to right bank
        
    else: #else it's on right
        boat_pos = 1 #chanes boat to left for new states
        append_child(1,1)
    
    for x in [1,2]:
        #move a mis and can one at a time
        if boat_pos == 0:
            #if boat is moving right, we subtract people
            x = -x
            
        append_child(x,0)
        append_child(0,x)
    
    return children

def bfs(initial_state):
    #bfs implementation
    frontier = []
    explored = set()
    frontier.append(initial_state)
    
    while frontier:
        #check state/node
        state = frontier.pop(0)
	    
        if state.is_goal():
            #when objective state is reached
            return state
        
        explored.add(state) #adds to list so we don't have to check again
        children = successors(state) #create a list of valid child nodes
        
        for child in children:
            if (child not in explored) or (child not in frontier):
                #if not checked yet, save to check later
                frontier.append(child)
    return

def display_solution(solution):
    #displays path for solution
    path = [solution]
    parent = solution.parent
    
    while parent:
        #go through path
        path.append(parent)
        parent = parent.parent #redefines the cursor

    for x in range(len(path)):
        #prints each state in list for path
        state = path[len(path) - x - 1]
        print(state)


def main():
	#solution = breadth_first_search()
        initial_state = State(3, 3, 1)
        print ("Initial bank on left, target bank on right:")
        display_solution(bfs(initial_state))


main()
