from collections import defaultdict
from math import sqrt


class GridMap(object):
    """ Represents a rectangular grid map. The map consists of 
        nrows X ncols coordinates (squares). Some of the squares
        can be blocked (by obstacles).
    """
    def __init__(self, nrows, ncols):
        """ Create a new GridMap with the given amount of rows
            and columns.
        """
        self.nrows = nrows
        self.ncols = ncols
        
        self.map = [[0] * self.ncols for i in range(self.nrows)]
        self.blocked = defaultdict(lambda: False)
    
    def set_blocked(self, coord, blocked=True):
        """ Set the blocked state of a coordinate. True for 
            blocked, False for unblocked.
        """
        self.map[coord[0]][coord[1]] = blocked
    
        if blocked:
            self.blocked[coord] = True
        else:
            if coord in self.blocked:
                del self.blocked[coord]
    
    def move_cost(self, c1, c2):
        """ Compute the cost of movement from one coordinate to
            another. 
            
            The cost is the Euclidean distance.
        """
        return sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2) 
    
    def successors(self, coord):
        """ Compute the successors of coordinate 'c': all the 
            coordinates that can be reached by one step from 'c'.
        """
        slist = []
        
        for row in (-1, 0, 1):
            for col in (-1, 0, 1):
                if [row,col] == [0,0]: continue 
                newrow = coord[0] + row
                newcol = coord[1] + col
                if (    0 <= newrow <= self.nrows - 1 and
                        0 <= newcol <= self.ncols - 1 and
                        self.map[newrow][newcol] == False): # Wall: False
                    slist.append((newrow, newcol))
        return slist
    
    def printme(self):
        """ Print the map to stdout in ASCII
        """
        for row in range(self.nrows):
            for col in range(self.ncols):
                print "%s" % ('O' if self.map[row][col] else '.'),
            print ''

if __name__ == '__main__':

    g = GridMap(20,20)
    for b in [  (1, 1), (1, 2), (0, 3), (1, 3), (2, 3), 
                (2, 4), (2, 5), (2, 6)]:
        g.set_blocked(b)
    successor = g.successors( [10,10])
    g.printme()
    print successor
    print
