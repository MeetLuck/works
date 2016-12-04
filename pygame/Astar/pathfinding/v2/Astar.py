from constants2 import *
from math import sqrt
bgcolor = white #lightgray
inf = 1.0E09

class Node:
    def __init__(self):
        self.label = ""
        self.wall = False
        self.reset()
    def reset(self):
        self.G = self.F = self.H = ""
        self.camefrom = ""
        self.previous = None
        self.Goal, self.Start, self.Current = False,False,False
        self.bgcolor = bgcolor

    def drawLabel(self):
        if self.Goal:
            fontName,fontcolor = 'Impact',red
        elif self.Start:
            fontName,fontcolor = 'Impact',blue
        else:
            fontName,fontcolor = 'Courier',black
        self.drawText(self.label,fontName,fontcolor,(5,5) )

    def drawText(self,text,fontName,fontcolor,topleft):
        font = pygame.font.SysFont(fontName, 16) # 'Fixedsys' #'Terminal' #'Impact','Arial'
        text = font.render(text, True, fontcolor)
        rect = text.get_rect()
        rect.topleft = topleft
        self.image.blit(text,rect)

    # ========= draw came from(N,E,W,S) ===========
    def drawNEWS(self):
        if not self.camefrom: return None
        img = imgNEWS[self.camefrom]
        img.set_colorkey(white)
        img = img.convert_alpha()
        imgrect = img.get_rect()
        imgrect.center = self.rect.center
        self.image.blit(img,imgrect)

    def drawCost(self):
        fontName,fontcolor = 'Terminal', blue
        self.drawText( str(self.F),fontName,fontcolor, (self.rect.width//2,10))
        self.drawText( str(self.G),fontName,fontcolor, (self.rect.left+20,self.rect.bottom-20))
        self.drawText( str(self.H),fontName,fontcolor, (self.rect.right-20,self.rect.bottom-20))

    def draw(self,size):
        if self.wall: self.bgcolor = darkgray
        self.image = pygame.Surface((size,size)) #self.image = pygame.Surface((50,50))
        self.image.fill(self.bgcolor)
        self.rect = self.image.get_rect()
        if self.Current:
            pygame.draw.rect(self.image,red,self.rect,2)
        else:
            pygame.draw.rect(self.image,gray,self.rect,1)
        self.drawLabel()
        self.drawCost()
        self.drawNEWS()
        return self.image

class Graph:
    def __init__(self,amap):
        self.amap = amap
        self.Nrows, self.Ncols = len(amap),  len(amap[0])
        self.createGraph()

    def createGraph(self): # create one node per square in the grid
        self.grid = self.amap[:]
        for r,row in enumerate(self.amap):
            for c,col in enumerate(row):
                node = Node()
                index = r * self.Ncols + c
                node.label = chr(65 + index) # i = r*self.cols + c
                if col == '*': node.wall = True
                self.grid[r][c] = node

    def findRC(self,node):
        for r,row in enumerate(self.grid):
            for c,col in enumerate(row):
                if node == self.grid[r][c]:
                    return [r,c]
        return None

    def inBounds(self,rc):
        return 0 <= rc[0] < self.Nrows and 0 <= rc[1] < self.Ncols

    def notWalls(self,rc):
        r,c = rc
        return not self.grid[r][c].wall

    def getAdjacents(self,node):
        # add edges to adjacent nodes
        adjacent = dict()
        r,c = self.findRC(node) # y=r,x=c
        #      c-1  c   c+1
        # r-1  NW   N   NE
        #           
        # r    W  (r,c) E
        #           
        # r+1  SW   S   SE
        #
        N,E,W,S = (r-1,c),(r,c+1),(r,c-1),(r+1,c)
        NE,SE,SW,NW = (r-1,c+1),(r+1,c+1),(r+1,c-1),(r-1,c-1)
        NEWS = [N,E,W,S] + [NE,SE,SW,NW]
        NEWS = filter(self.inBounds,NEWS)
        NEWS = filter(self.notWalls,NEWS)
        if N in NEWS: adjacent['N'] = self.grid[N[0]][N[1]]
        if E in NEWS: adjacent['E'] = self.grid[E[0]][E[1]]
        if W in NEWS: adjacent['W'] = self.grid[W[0]][W[1]]
        if S in NEWS: adjacent['S'] = self.grid[S[0]][S[1]]
        if NE in NEWS and self.notWalls(N) and self.notWalls(E):
            adjacent['NE'] = self.grid[NE[0]][NE[1]]
        if SE in NEWS and self.notWalls(S) and self.notWalls(E):
            adjacent['SE'] = self.grid[SE[0]][SE[1]]
        if SW in NEWS and self.notWalls(S) and self.notWalls(W):
            adjacent['SW'] = self.grid[SW[0]][SW[1]]
        if NW in NEWS and self.notWalls(N) and self.notWalls(W):
            adjacent['NW'] = self.grid[NW[0]][NW[1]]
        return adjacent

    def findNodeByLabel(self,label):
        for r,row in enumerate(self.grid):
            for c,col in enumerate(row):
                if self.grid[r][c].label == label:
                    return col

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

# Search
class Astar:
    def __init__(self, graph,start,goal):
        self.graph = graph
        self.start_label = start
        self.goal_label = goal
    def reset(self):
        self.found = False
        for row in self.graph.grid:
            for node in row:
                node.reset() #self.graph.nodes[i].reset()
        self.reachable = list()
        self.explored = list()
        self.path = list()
        self.start = self.graph.findNodeByLabel(self.start_label)
        self.goal =  self.graph.findNodeByLabel(self.goal_label)
        self.start.G = 0
        self.computeHeuristic(self.start)
        self.start.F = self.start.G + self.start.H
        self.start.Start = True
        self.goal.Goal = True
        self.reachable.append(self.start)
        self.currentNode = self.start
        self.iteration = 0

    def foundPath(self,node):
        if node != self.goal: return False
        print '------------- found path ----------------'
        self.found = True
        #node.bgcolor = yellow
        self.buildPath(node)
        return True

    def buildPath(self,node):
        while node != None:
            node.bgcolor = lightpurple
            self.path.append(node)
            node = node.previous

    def step(self):
#       self.iteration += 1
        # are we done yet?
        if self.foundPath(self.currentNode): return
        # choose current Node from 'reachable'
        self.currentNode.Current = False
        self.currentNode = self.chooseBestNode()
        self.currentNode.Current = True
        # do not repeat
        self.reachable.remove(self.currentNode)
        self.explored.append(self.currentNode)
        # set bgcolor of nodes
        self.markNodes()
        # get new reachable
        self.getNewReachable(self.currentNode)
        printNodesList(self)

    def chooseBestNode(self):
        mincost = inf #float('inf')
        bestnode = None
#       print '========== choose Best Node ================='
        for node in self.reachable:
#           print '{} : {}+{}={}'.format(node.label,node.G,node.H,node.F)
            if node.F < mincost:
                mincost = node.F
                bestnode = node
            elif node.F == mincost:
                bestnode = choice([node,bestnode])
        return bestnode

    def computeHeuristic(self,node): # G : cost from node to Goal
        r1,c1 = self.graph.findRC(node)
        r2,c2 = self.graph.findRC(self.goal)
        node.H = 10*( abs(r2-r1) + abs(c2-c1) )
        return node.H

    def markNodes(self):
        for node in self.reachable: node.bgcolor = green
        for node in self.explored:  node.bgcolor = orange

    def computeCost(self,current,adjacent,direction):
        if direction in ['N','E','W','S']:
            adjacent.G = current.G + 10
        elif direction in ['NE','NW','SE','SW']:
            adjacent.G = current.G + 14
        else:
            raise Exception('no such direction, direction error')
        adjacent.F = adjacent.G + self.computeHeuristic(adjacent)

    def getNewReachable(self, current):
        NEWS  = {'N':'S','S':'N','E':'W','W':'E'}
        changedirection  = {'NE':'SW','SW':'NE','SE':'NW','NW':'SE'}
        changedirection.update(NEWS)
        # where can we get from here?
        new_reachable = self.graph.getAdjacents(current)
        for direction,adjacent in new_reachable.items():
            if adjacent in self.explored: continue
            if adjacent not in self.reachable: # new path
                self.computeCost(current,adjacent,direction)
                adjacent.bgcolor = darkgreen
                adjacent.previous = current
                adjacent.camefrom = changedirection[direction]
                self.reachable.append(adjacent)
            else: # existing path => check whether it is Short Path or not
                if   direction in ['N','E','W','S']:        newG = current.G + 10
                elif direction in ['NE','NW','SE','SW']:    newG = current.G + 14
                if newG < adjacent.G: # short path
                    adjacent.G = newG
                    adjacent.previous = current
                    adjacent.camefrom = changedirection[direction]
                    adjacent.F = adjacent.G + self.computeHeuristic(adjacent)

    def draw(self,surface):
        self.graph.draw(surface)

    def run(self):
        self.reset()
        while not self.found:
            self.step()

if __name__ == '__main__':
    g = Graph(amap)
    printNodes(g)
