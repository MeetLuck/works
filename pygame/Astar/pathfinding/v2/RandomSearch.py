from constants2 import *
bgcolor = lightgray

class Node:
    def __init__(self):
        self.label = ""
        self.wall = False
        self.reset()
    def reset(self):
        self.bgcolor = bgcolor
        self.camefrom = ""
        self.previous = None
        self.Goal, self.Start, self.Current = False,False,False
    def draw(self,size):
        if self.wall: self.bgcolor = darkgray
        self.image = pygame.Surface((size,size))
        #self.image = pygame.Surface((50,50))
        self.image.fill(self.bgcolor)
        self.rect = self.image.get_rect()
        if self.Current:
            pygame.draw.rect(self.image,red,self.rect,2)
        else:
            pygame.draw.rect(self.image,gray,self.rect,1)
        if self.Goal:
            fontName,fontcolor = 'Impact',red
        elif self.Start:
            fontName,fontcolor = 'Impact',blue
        else:
            fontName,fontcolor = 'Courier',black
        font = pygame.font.SysFont(fontName, 16) # 'Fixedsys' #'Terminal' #'Impact','Arial'
        text = font.render(self.label, True, fontcolor)
        rect = text.get_rect()
        rect.topleft = 5,5
        #rect.center = self.rect.center
        self.image.blit(text,rect)
        # ========= draw came from(N,E,W,S) ===========
        def imageCamefrom():
            if not self.camefrom: return None
            img = imgNEWS[self.camefrom]
            img.set_colorkey(white)
            img = img.convert_alpha()
            imgrect = img.get_rect()
            imgrect.center = self.rect.center
            self.image.blit(img,imgrect)
        imageCamefrom()
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
        N,E,W,S = (r-1,c),(r,c+1),(r,c-1),(r+1,c)
        NEWS = [N,E,W,S]
        NEWS = filter(self.inBounds,NEWS)
        NEWS = filter(self.notWalls,NEWS)
        if N in NEWS: adjacent['N'] = self.grid[N[0]][N[1]]
        if E in NEWS: adjacent['E'] = self.grid[E[0]][E[1]]
        if W in NEWS: adjacent['W'] = self.grid[W[0]][W[1]]
        if S in NEWS: adjacent['S'] = self.grid[S[0]][S[1]]
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
class RandomSearch:
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
        self.chooseCurrentNode()
        # do not repeat
        self.reachable.remove(self.currentNode)
        self.explored.append(self.currentNode)
        # get new reachable
        self.getNewReachable(self.currentNode)
        printNodesList(self)
        # set bgcolor of nodes
        self.markNodes()

    def chooseCurrentNode(self):
        self.currentNode.Current = False
        self.currentNode = choice(self.reachable)
        self.currentNode.Current = True
        #return choice(self.reachable)

    def markNodes(self):
        for node in self.reachable: node.bgcolor = green
        for node in self.explored:  node.bgcolor = orange

    def getNewReachable(self,current):
        changedirection = {'N':'S','S':'N','E':'W','W':'E'}
        # where can we get from here?
        new_reachable = self.graph.getAdjacents(current)
        for direction,adjacent in new_reachable.items():
            if adjacent in self.reachable or adjacent in self.explored: continue
            adjacent.previous = current
            adjacent.camefrom = changedirection[direction]
            self.reachable.append(adjacent)

    def draw(self,surface):
        self.graph.draw(surface)

    def run(self):
        self.reset()
        while not self.found:
            self.step()

if __name__ == '__main__':
    g = Graph(amap)
    printNodes(g)
