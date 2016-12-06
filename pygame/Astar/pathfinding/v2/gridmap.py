#from constants2 import *
#from math import sqrt
#bgcolor = white #lightgray
#inf = 1.0E09

class GridMap:
    def __init__(self,Nrows,Ncols):
        self.Nrows = Nrows
        self.Ncols = Ncols
        self.reset()
        self.setStart( (0,0) )
        self.setGoal( (3,8) )

    def reset(self): # create one node per square in the grid
        self.map = [ [0]*self.Ncols for i in range(self.Nrows) ]
#       self.nodes = list() 
#       for row in range(self.Nrows):
#           for col in range(self.Ncols):
#               node = Node( (row,col) )
#               self.nodes.append(node)
    def setStart(self,coord):
        self.start_pos = coord
        self.set(coord,'S')
    def setGoal(self,coord):
        self.goal_pos = coord
        self.set(coord,'G')
    def getStart(self):
        return self.start_pos
    def getGoal(self):
        return self.goal_pos
    def set(self,coord,val):
        r,c = coord
        self.map[r][c] = val
    def get(self,coord):
        r,c = coord
        return self.map[r][c]
    def setWall(self,coord): # toggle wall
        self.set( coord,not self.get(coord) )

    def getReachables(self,coord):
        #      c-1  c   c+1
        # r-1  NW   N   NE
        # r    W  (r,c) E
        # r+1  SW   S   SE
        vectors = [1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1], [0,-1], [1,-1] 
        reachables = list()
        for v in vectors:
            reachable = coord[0] + v[0], coord[1] + v[1]
            reachables.append(reachable)
        reachables = filter(self.inBound, reachables)
        reachables = filter(self.notWall, reachables)
        return reachables

    def inBound(self,coord):
        return 0 <= coord[0] < self.Nrows and 0 <= coord[1] < self.Ncols

    def notWall(self,coord):
        return not self.get(coord) # wall -> True

    def printme(self):
        """ Print the map to stdout in ASCII
        """
        for row in range(self.Nrows):
            for col in range(self.Ncols):
                val = self.map[row][col]
                if val in [1,True]: char = '*'
                elif val in [0,False]: char = '.'
                elif val == 'S': char = 'S'
                elif val == 'G': char = 'G'
                print "%s" % char,
            print ''

    def draw(self,surface):
        w,h = surface.get_size()
        size = min(w//self.Ncols,h//self.Nrows)
        for r,row in enumerate(self.grid):
            for c,col in enumerate(row):
                node = self.grid[r][c]
                image = node.draw(size)
                topleft = c*size,r*size
                surface.blit(image,topleft)
        return surface


if __name__ == '__main__':
    g = GridMap(10,10)
    for b in [ (1,2),(0,3),(1,3),(2,3) ]:
        g.setWall(b)
    g.printme()
    print g.getReachables([1,4])
