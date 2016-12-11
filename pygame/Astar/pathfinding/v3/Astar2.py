import sys
sys.path.append('..')
from PriorityQueue import *
from math import sqrt

class Node:
    def __init__(self,coord):
        self.coord = coord
        self.G = self.F = self.H = ""
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
        return "N(%s) -> G:%s, H:%s, F:%s" %(self.coord,self.G,self.H,self.F)
    def __repr__(self):
        return self.__str__()

class Astar:
    def __init__(self,getReachables):
        self.getReachables = getReachables

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
        reachables = PriorityQueue()
        reachables.put(start)
        explored = list()
        while not reachables.empty():
            current = reachables.get()
            if current == goal: 
                return self.buildPath(current)
            explored.append(current)

            for reachable_coord in self.getReachables(current.coord):
                reachable = Node(reachable_coord)
                print 'current,reachable',current,reachable
                if reachable in explored: continue 
                # not explored node
                if reachable in reachables: # old reachable
                    pass
                else: # new reachable
                    reachable.G = current.G + self.moveCost(current,reachable)
                    reachable.F = reachable.G + self.getHeuristic(start,goal)
                    reachables.put(reachable)
        return None

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
