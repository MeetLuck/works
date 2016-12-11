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
    def __init__(self,app): #,getReachables):
        self.app = app
        self.getReachables = app.gridmap.getReachables
        self.explored = list()
        self.reachables = PriorityQueue()

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
        print '========== found path =========='
        path = list()
        while not node.camefrom:
            path.append(node)
            node = node.camefrom
        return path

    def findPath(self,start_coord,goal_coord):
        start = Node(start_coord)
        goal  = Node(goal_coord)
        start.G = 0
        start.F = start.G + self.getHeuristic(start,goal) 
        #self.reachables = PriorityQueue()
        self.reachables.put(start)
        #self.explored = list()
        print start.coord, goal.coord
        while not self.reachables.empty():
            current = self.reachables.get()
            self.explored.append(current)
            if current.coord == goal.coord: 
                return self.buildPath(current)
            self.app.drawExplored(self.explored)
            pygame.display.flip()
            #print 'current,reachable',current,self.reachables
            #print 'explored', self.explored

            for reachable_coord in self.getReachables(current.coord):
                reachable = Node(reachable_coord)
                if reachable_coord == goal.coord:
                    print 'reachable is goal'
                #print 'current,reachable',current,reachable
                if reachable in self.explored: #continue 
                    #print reachable.coord, explored
                    continue
                # not explored node
                if reachable in self.reachables: # old reachable
                    #print 'old reachable',reachable.coord
                    pass
                else: # new reachable
                    reachable.G = current.G + self.moveCost(current,reachable)
                    reachable.F = reachable.G + self.getHeuristic(start,goal)
                    #print 'new reachable',reachable.coord
                    self.reachables.put(reachable)
        raise Exception('not found path')
#       return None

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
