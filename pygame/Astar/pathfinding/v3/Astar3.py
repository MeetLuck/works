import sys
sys.path.append('..')
from PriorityQueue import *
from math import sqrt
import pygame

class Node:
    def __init__(self,coord):
        self.coord = coord
        self.G = self.F = self.H = 1000#""
        self.camefrom = None
    def __eq__(self,other):
#       print '... __eq__',self.coord,other.coord
        return self.coord == other.coord
    def __cmp__(self,other):
#       print '... __cmp__'
        return cmp(self.F, other.F)
    def __hash__(self):
#       print '... __hash__'
        return hash(self.coord)
    def __str__(self):
        return "Node(%s)" % str(self.coord) # -> G:%s, H:%s, F:%s" %(self.coord,self.G,self.H,self.F)
    def __repr__(self):
        return self.__str__()

class Astar:
    #def __init__(self,getReachables):
    def __init__(self,app):
        self.app = app
        self.reset()
    def reset(self):
        self.found = False
        self.current = self.camefrom = None 
        self.getReachables = self.app.gridmap.getReachables
        start_pos,goal_pos = self.app.gridmap.start_pos, self.app.gridmap.goal_pos
        self.start = Node(start_pos)
        self.goal  = Node(goal_pos)
        self.start.G = 0
        self.start.F = self.start.G + self.getHeuristic(self.start,self.goal) 
        self.reachables = PriorityQueue()
        self.reachables.put(self.start)
        self.explored = list()

    def getHeuristic(self,node,goal):
        r1,c1 = node.coord
        r2,c2 = goal.coord
        node.H = 10*( abs(r1-r2) + abs(c1-c2) )
        return node.H 

    def moveCost(self,from_node,to_node):
        r1,c1 = from_node.coord
        r2,c2 = to_node.coord
        distance = 10*sqrt( (r1-r2)**2 + (c1-c2)**2 )
        return distance

    def buildPath(self,node):
        path = list()
        while node:
            path.append(node)
            node = node.camefrom
        return path

    def step(self):
        if self.found: return
        self.current = self.reachables.get()
        self.explored.append(self.current)
#       self.app.drawExplored(self.explored)
#       pygame.display.flip()
        if self.current == self.goal:
            self.found = True
            return self.current #return self.buildPath(current)
        for reachable_coord in self.getReachables(self.current.coord):
            reachable = Node(reachable_coord)
            if reachable in self.explored: continue
            if reachable in self.reachables:
                pass
            else:
                reachable.G = self.current.G + self.moveCost(self.current, reachable)
                reachable.F = reachable.G + self.getHeuristic(reachable, self.goal)
                reachable.camefrom = self.current
                self.reachables.put(reachable)

    def findPath(self): #,start_coord,goal_coord):
        self.reset() #start_coord,goal_coord)
        while not self.reachables.empty():
            current = self.step()
            if self.found:
                return self.buildPath(current)
        raise Exception('not found path')

if __name__ == '__main__':
    c1 = 1,1
    c2 = 1,2
    c3 = 3,5
    n1 = Node(c1)
    n2 = Node(c2)
    n3 = Node(c3)
    n4 = Node(c1)
    n1.F = 1
    n4.F = 2
    explored = list()
    explored.append(n1)
    explored.append(n2)
    print n1 in explored
    print n4 in explored
    print n4 >= n1
