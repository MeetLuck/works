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
    def draw(self):
        if self.wall: self.bgcolor = darkgray
        self.image = pygame.Surface((50,50))
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
    def __init__(self,grid):
        self.grid = grid
        self.rows,self.cols = len(grid),  len(grid[0])
        self.createNodes()
    def createNodes(self): # create one node per square in the grid
        self.nodes = list()
        for r,row in enumerate(self.grid):
            for c,col in enumerate(row):
                i = r*self.cols + c
                node = Node()
                node.label = chr(65+i)
                if col == '*':
                    node.wall = True
                self.nodes.append(node)
    def getAdjacents(self,node):
        # add edges to adjacent nodes
        adjacent = dict()
        for r in range(self.rows):
            for c in range(self.cols):
                if node != self.nodes[self.cols * r + c]: continue
                # ignore blocked squares
                if grid[r][c] == '*': continue
                # figure out the adjacent nodes
                if r > 0 and grid[r-1][c] == ' ': # UP 
                    adjacent['N'] = self.nodes[self.cols*(r-1) + c]
                if r < self.rows-1 and grid[r+1][c] == ' ': # DOWN
                    adjacent['S'] = self.nodes[self.cols*(r+1) + c]
                if c > 0 and grid[r][c-1] == ' ': # LEFT
                    adjacent['W'] = self.nodes[self.cols*r + c-1]
                if c < self.cols-1 and grid[r][c+1] == ' ': # RIGHT 
                    adjacent['E'] = self.nodes[self.cols*r + c+1]
        return adjacent

    def findNodeByLabel(self,label):
        for i,val in enumerate(self.nodes):
            if self.nodes[i].label == label:
                return val
    def draw(self,surface):
        for r,row in enumerate(self.grid):
            for c,col in enumerate(row):
                node = self.nodes[self.cols*r + c]
                image = node.draw()
                topleft = c*50,r*50
                surface.blit(image,topleft)
        return surface

# Search
class BreadFirstSearch:
    def __init__(self, graph,start,goal):
        self.graph = graph
        self.start_label = start
        self.goal_label = goal
    def reset(self):
        self.found = False
        for node in self.graph.nodes:
            node.reset() #self.graph.nodes[i].reset()
        self.reachable = Queue()
        self.explored = list()
        self.path = list()
        self.start = self.graph.findNodeByLabel(self.start_label)
        self.goal =  self.graph.findNodeByLabel(self.goal_label)
        self.start.Start = True
        self.goal.Goal = True
        self.reachable.put(self.start)
        self.currentNode = self.start
        self.iteration = 0

    def foundPath(self,node):
        if node != self.goal: return False
        print '------------- found path ----------------'
        self.found = True
        node.bgcolor = yellow
        self.buildPath(node)
        return True
    def buildPath(self,node):
        pass

    def step(self):
#       self.iteration += 1
        # are we done yet?
        if self.foundPath(self.currentNode): return
        # choose current Node from 'reachable'
        self.chooseCurrentNode()
        # do not repeat
        #self.reachable.remove(self.currentNode)
        self.explored.append(self.currentNode)
        # get new reachable
        self.getNewReachable(self.currentNode)
        printNodesList(self)
        # set bgcolor of nodes
        self.markNodes()

    def chooseCurrentNode(self):
        self.currentNode.Current = False
        self.currentNode = self.reachable.get()
        self.currentNode.Current = True
        #return choice(self.reachable)

    def markNodes(self):
        for node in self.reachable.elements: node.bgcolor = green
        for node in self.explored:  node.bgcolor = orange

    def getNewReachable(self,current):
        # where can we get from here?
        new_reachable = self.graph.getAdjacents(current)
        for direction,adjacent in new_reachable.items():
            if adjacent in self.reachable.elements or adjacent in self.explored: continue
            #if adjacent in self.explored: continue
            adjacent.previous = current
            if direction == 'N': adjacent.camefrom = 'S'
            if direction == 'S': adjacent.camefrom = 'N'
            if direction == 'E': adjacent.camefrom = 'W'
            if direction == 'W': adjacent.camefrom = 'E'
            self.reachable.put(adjacent)

    def draw(self,surface):
        self.graph.draw(surface)

    def run(self):
        self.reset()
        while not self.found:
            self.step()
