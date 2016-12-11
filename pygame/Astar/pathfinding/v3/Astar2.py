import sys
sys.path.append('..')
from PriorityQueue import *
class Node:
    def __init__(self,coord):
        self.coord = coord
        self.G = self.F = self.H = ""
    def __eq__(self,other):
        print '... __eq__'
        return self.coord == other.coord
    def __cmp__(self,other):
        print '... __cmp__'
        return cmp(self.F, other.F)
    def __hash__(self):
        print '... __hash__'
        return hash(self.coord)
    def __str__(self):
        return "N(%s) -> G:%s, H:%s, F:%s" %(self.coord,self.G,self.H,self.F)
    def __repr__(self):
        return self.__str__()

class Astar:
    def __init__(self,getReachable):
        self.getReachable = getReachable
    def findPath(self,start_coord,goal_coord):
        start = Node(start_coord)
        goal  = Node(goal_coord)
        start.G = 0
        start.F = start.G + self.getHeuristic(start,goal) 
        reachabes = PriorityQueue()
        reachabes.put(start)
        explored = list()
        while not reachables.empty():
            current = reachables.get()
            if current == goal: 
                return self.buildPath(current)
            explored.append(current)

            for reachable_coord in self.getReachable(current.coord):
                reachable = Node(reachable_coord)
                if reachable in explored: continue 
                # not explored node
                if reachable in reachables: # old reachable
                    pass
                else: # new reachable
                    reachable.G = current.G + self.moveGost(current,reachable)
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