from math import sqrt
class Node:
    def __init__(self,coord):
        self.coord = coord
        self.explored = False
    def getNodefrom(self,coord):
        if self.coord == coord:
            return self

class Astar:
    def __init__(self,getReachable,getHeuristic,getGcost):
        self.getReachable = getReachable
        self.getHeuristic = getHeuristic
        self.getGcost = getGcost

    def findPath(self,start_coord,goal_coord):
        start = Node(start_coord)
        goal = Node(goal_coord)
#       start.camefrom = None
        start.G = 0
        start.F = self.getFcost(start,goal)
        reachables = PriorityQueue()
        reachables.put(start)
        while not reachables.empty():
            current = reachables.get()
            current.explored = True
            if current == goal: break
            for reachable_coord in self.getReachables(current.coord):
                reachable= Node(reachable_coord)
                if reachable.explored: continue
                reachable.G = self.getGcost(current, reachable)
                reachable.F = self.getFcost(reachable,goal)


    def getHeuristic(self, node, goal): 
        return 10*abs( goal.coord[0] - node.coord[0] ) + abs( goal.coord[1] - node.coord[1] )

    def moveCost(self,from_node,to_node):
        r1,c1 = from_node.coord
        r2,c2 = to_node.coord
        return 10 * sqrt( (r1-r2)**2 + (c1-c2)**2 )

    def getGcost(self,from_node,to_node):
        return from_node.G + moveCost(from_node,to_node)
    def getFcost(self,node,goal):
        return node.G + self.getHeuristic(node,goal)
