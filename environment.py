#!/usr/bin/python
# coding: utf-8 

import sys

class Environment:
    'Map-based environment'
    '''
    You will also need to implement the class Environment. 
    The __init__ function has been given to you. 
    Additional methods should handle environment-related operations 
    like determining if a state is a goal state, 
    and calculating the available moves from a state.
    '''

    # Member data
    # elevations: raw data for each position, stored in a list of lists
    #             (each outer list represents a single row)
    # height: number of rows
    # width: number of elements in each row
    # end_x, end_y: location of goal

    
    def __init__(self, mapfile, energy_budget, end_coords):
        self.elevations = []
        self.height = 0
        self.width = -1
        self.end_x, self.end_y = end_coords
        self.energy_budget = energy_budget
        # Read in the data
        for line in mapfile:
            nextline = [ int(x) for x in line.split() ]
            if self.width == -1:
                self.width = len(nextline)
            elif len(nextline) == 0:
                sys.stderr.write("No data (or parse error) on line %d\n"
                                 % (len(self.elevations) + 1))
                sys.exit(1)
            elif self.width != len(nextline):
                sys.stderr.write("Inconsistent map width in row %d\n"
                                 % (len(self.elevations) + 1))
                sys.stderr.write("Expected %d elements, saw %d\n"
                                 % (self.width, len(nextline)))
                sys.exit(1)
            self.elevations.insert(0, nextline)
        self.height = len(self.elevations)
        if self.end_x == -1:
            self.end_x = self.width - 1
        if self.end_y == -1:
            self.end_y = self.height - 1
    '''
    def __init__(self, mapfile, energy_budget, end_coords):
        self.elevations = []
        self.height = 0
        self.width = -1
        self.end_x, self.end_y = end_coords
        self.energy_budget = energy_budget
        # Read in the data
        with open(mapfile,'r') as ff:
            for line in ff:                
                nextline = [ int(x) for x in line.split() ]
                if self.width == -1:
                    self.width = len(nextline)
                elif len(nextline) == 0:
                    sys.stderr.write("No data (or parse error) on line %d\n"
                                     % (len(self.elevations) + 1))
                    sys.exit(1)
                elif self.width != len(nextline):
                    sys.stderr.write("Inconsistent map width in row %d\n"
                                     % (len(self.elevations) + 1))
                    sys.stderr.write("Expected %d elements, saw %d\n"
                                     % (self.width, len(nextline)))
                    sys.exit(1)
                self.elevations.insert(0, nextline)
        self.height = len(self.elevations)
        if self.end_x == -1:
            self.end_x = self.width - 1
        if self.end_y == -1:
            self.end_y = self.height - 1
    '''
            
    def is_goal(self,state):
        if state.x==self.end_x and state.y==self.end_y:
            return True
        else:
            return False
    
    def available_moves(self,state):
        moves={}
        x=state.x
        y=state.y
        #1-‘N' 2-E 3-S 4-W
        moves[1]=['N',(x,y+1)]
        moves[2]=['E',(x+1,y)]
        moves[3]=['S',(x,y-1)]
        moves[4]=['W',(x-1,y)]
        
        if x==0:
            moves.pop(4)
        elif x==self.width-1:
            moves.pop(2)
        if y==0:
            moves.pop(3)
        elif y==self.height-1:
            moves.pop(1)
        return moves

    
            