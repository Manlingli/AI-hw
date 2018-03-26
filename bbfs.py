'''
Created on Apr 28, 2017

@author: manlingli
'''
import state
import copy


class Search(object):
    '''
    classdocs
    '''


    def __init__(self,initial_state, env):
        self.frontier = []
        self.visited = []
        self.env = env
        self.initial_state = initial_state
        self.goal_state=state.State(env.end_x,env.end_y)

    def get_cost(self, state_old, state,direction):
        old_elev = self.env.elevations[state_old.y][state_old.x]
        new_elev = self.env.elevations[state.y][state.x]
        if old_elev == new_elev:  # flat move
            cost = state_old.cost_so_far + 1
        if new_elev > old_elev:  # uphill move
            if direction=='F':
                cost = state_old.cost_so_far + 1 + pow((new_elev - old_elev), 2)
            elif direction=='B':
                cost = state_old.cost_so_far + 1 + (new_elev - old_elev)
        if new_elev < old_elev: 
            if direction=='F':  # downhill move 
                cost = state_old.cost_so_far + 1 + (old_elev - new_elev)
            if direction=='B':
                cost = state_old.cost_so_far + 1 + pow((new_elev - old_elev), 2)
        return cost
    
    def expand(self,frontier,visited,direction,layer):  
        #expand the node with small layer 

        while frontier[0].layer==layer:
            
            state_close=frontier.pop(0)
            visited.append(state_close)
            available_moves = self.env.available_moves(state_close)
            moves = state_close.moves_so_far
            for i in available_moves:
                move, (x, y) = available_moves[i]
                
                new_state = state.State(x,y)       
                if new_state not in visited:  
                    moves.append(move)
                    new_state.layer=state_close.layer+1
                    new_state.moves_so_far = copy.deepcopy(moves)
                    new_state.cost_so_far = self.get_cost(state_close, new_state,direction)   
                    #
                    
                    if new_state in frontier:
                        frontier_index = frontier.index(new_state)
                        if new_state.cost_so_far < frontier[frontier_index].cost_so_far:
                            frontier.pop(frontier_index)  # remove the state with larger f
                            frontier.append(new_state)  # add the new one                            
                    elif new_state not in frontier:
                        if new_state.cost_so_far <= self.env.energy_budget:
                            frontier.append(new_state)
                            #print frontier[-1]
                    moves.pop()
            #self.frontier.sort(key=lambda state:(state.f, state.timestamp), reverse=True)  # sort by f, timestamp   
            if len(frontier)<1:
                return [],visited
        return frontier,visited       
      
    def trace_back_path(self,moves_so_far):
        moves=[]
        for move in moves_so_far:
            if move=='N':
                moves.append('S')
            elif move=='S':
                moves.append('N')
            elif move=='E':
                moves.append('W')
            elif move=='W':
                moves.append('E')
        moves.reverse()
        return moves
    
        
    def search(self):
        layer=0
        Ffrontier,Bfrontier,Fvisited,Bvisited=[],[],[],[]
        target_state=state.State(self.env.end_x,self.env.end_y)
        target_state.parent=(self.env.end_x,self.env.end_y)
        Ffrontier.append(self.initial_state)
        Bfrontier.append(target_state)
        while len(Ffrontier) and len(Bfrontier):
            #expand both frontier until they intersect
            F_union=list(set(Ffrontier).union(set(Fvisited)))
            B_union=list(set(Bfrontier).union(set(Bvisited)))
            frontier_intersection=[val for val in F_union if val in B_union]
            while len(frontier_intersection):
                solution=[]
                for i in range(len(frontier_intersection)):
                    F_index=F_union.index(frontier_intersection[i])
                    B_index=B_union.index(frontier_intersection[i])
                    total_cost=F_union[F_index].cost_so_far+B_union[B_index].cost_so_far
                    if total_cost<=self.env.energy_budget:
                        goal_state=state.State(self.env.end_x,self.env.end_y)
                        goal_state.cost_so_far=total_cost
                        goal_state.moves_so_far=F_union[F_index].moves_so_far+self.trace_back_path(B_union[B_index].moves_so_far)
                        solution.append(goal_state)
                solution.sort(key=lambda state:state.cost_so_far)
                self.frontier=Ffrontier+Bfrontier
                self.visited=Fvisited+Bvisited
                return solution[0],self.frontier,self.visited
            layer=Ffrontier[0].layer              
            Ffrontier,Fvisited=self.expand(Ffrontier, Fvisited, 'F',layer)
            layer=Bfrontier[0].layer   
            Bfrontier,Bvisited=self.expand(Bfrontier, Bvisited, 'B',layer)
        self.frontier=Ffrontier+Bfrontier
        self.visited=Fvisited+Bvisited        
        return [], self.frontier, self.visited    