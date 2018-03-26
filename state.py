#!/usr/bin/python
# coding: utf-8 
'''
Created on Apr 19, 2017

@author: manlingli
'''


class State(object):

    def __init__(self, x_pos, y_pos):
        '''
        Constructor
        '''
        self.x = x_pos
        self.y = y_pos
        self.moves_so_far = []
        self.cost_so_far = 0
        self.f = 0 #A* value
        self.timestamp=0
        self.parent=(0,0)
        self.layer=0
    def add_moves(self, move):
        
        self.moves_so_far.append(move)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __str__(self):
        return "Pos=(%d, %d) Moves=%s Cost=%d" % (self.x, self.y, self.moves_so_far, self.cost_so_far)
        
