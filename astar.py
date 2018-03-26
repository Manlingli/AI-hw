# coding: utf-8 
'''
Created on Apr 19, 2017

@author: manlingli
'''

import state
import copy



class Search(object):
    '''
    It must implement the following methods:
    __init__
    search, which returns a triplet of:
        solution:anarrayofmovesinorder(e.g.,[‘N’, ‘E’, ‘E’]),orNone 
        frontier: an array of states which are in the frontier at the end of the search. 
        visited: an array of states that have been expanded during the search.
    The member data in Search is up to you, but a reasonable set might be: 
    frontier (array of States)
    visited (array of States)
    environment (pointer to the global environment)
    '''
    

    def __init__(self, initial_state, env):
        self.frontier = []
        self.visited = []
        #self.start_x = initial_state.x
        #self.start_y = initial_state.y
        self.env = env
        self.initial_state = initial_state

        

    
    def get_heuristic(self, state):
        return abs(self.env.end_x - state.x) + abs(self.env.end_y - state.y) + abs(self.env.elevations[self.env.end_y][self.env.end_x] - self.env.elevations[state.y][state.x])
    
    def get_cost(self, state_old, state):
        old_elev = self.env.elevations[state_old.y][state_old.x]
        new_elev = self.env.elevations[state.y][state.x]
        if old_elev == new_elev:  # flat move
            cost = state_old.cost_so_far + 1
        if new_elev > old_elev:  # uphill move
            cost = state_old.cost_so_far + 1 + pow((new_elev - old_elev), 2)
        if new_elev < old_elev:  # downhill move
            cost = state_old.cost_so_far + 1 + (old_elev - new_elev)
        return cost
            
    
    def search(self):
        timestamp = 1
        self.initial_state.f = self.get_heuristic(self.initial_state) + self.initial_state.cost_so_far
        self.frontier.append(self.initial_state)
        while len(self.frontier):
            state_closed = self.frontier.pop()
            self.visited.append(state_closed)
            # self.visited_coor.append((state_closed.x,state_closed.y))
            if self.env.is_goal(state_closed): 
                # self.frontier.sort(key=lambda state:(state.f,state.timestamp),reverse=True)               
                return state_closed, self.frontier, self.visited
            available_moves = self.env.available_moves(state_closed)
            moves = state_closed.moves_so_far
            for i in available_moves:
                move, (x, y) = available_moves[i]
                timestamp += 1
                new_state = state.State(x, y)        
                if new_state not in self.visited: 
                    moves.append(move)
                    new_state.moves_so_far = copy.deepcopy(moves)
                    new_state.cost_so_far = self.get_cost(state_closed, new_state)
                    new_state.f = self.get_heuristic(new_state) + new_state.cost_so_far
                    new_state.timestamp = timestamp
                    if new_state in self.frontier:
                        frontier_index = self.frontier.index(new_state)
                        if new_state.f < self.frontier[frontier_index].f:
                            self.frontier.pop(frontier_index)  # remove the state with larger f
                            self.frontier.append(new_state)  # add the new one
                    elif new_state not in self.frontier:
                        if new_state.cost_so_far <= self.env.energy_budget:
                            self.frontier.append(new_state)
                    moves.pop()
            self.frontier.sort(key=lambda state:(state.f, state.timestamp), reverse=True)  # sort by f, timestamp
        return [], self.frontier, self.visited           
                        
                        
                        
                        
                
                

        
        
