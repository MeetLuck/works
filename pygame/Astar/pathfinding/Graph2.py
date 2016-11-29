from random import random,choice
from colors import *
import pygame
bgcolor = lightgray

grid = ["   * ",
        " *** ",
        "     ",
        "* ** ",
        "*    "]

class Node:
    def __init__(self):
        self.wall = False
        self.adjacent = [] # UP,DOWN,LEFT,RIGHT(NWSE)
        self.previous = None
        self.label = ""
        self.reset()
    def reset(self):
        self.fontcolor = black
        self.bgcolor = bgcolor
        self.previous = None
        self.cost = 'Infinity'
        self.Goal = False
    def __str__(self):
        return self.label
    def draw(self):
        if self.wall: self.bgcolor = darkgray
        self.image = pygame.Surface((50,50))
        self.image.fill(self.bgcolor)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image,gray,self.rect,1)
        if self.Goal:
            pygame.draw.rect(self.image,green,self.rect,2)
        font = pygame.font.SysFont('Arial', 20)
        text = font.render(self.label, True, self.fontcolor)
        rect = text.get_rect()
        rect.center = self.rect.center
        self.image.blit(text,rect)
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
        ajacent = list()
        for r in range(self.rows):
            for c in range(self.cols):
                if node != self.nodes[self.cols * r + c]: continue
                # ignore blocked squares
                if grid[r][c] == '*': continue
                # figure out the adjacent nodes
                if r > 0 and grid[r-1][c] == ' ': # UP 
                    adjacent.append(self.nodes[self.cols*(r-1) + c])
                if r < self.rows-1 and grid[r+1][c] == ' ': # DOWN
                    node.adjacent.append(self.nodes[self.cols*(r+1) + c])
                if c > 0 and grid[r][c-1] == ' ': # LEFT
                    node.adjacent.append(self.nodes[self.cols*r + c-1])
                if c < self.cols-1 and grid[r][c+1] == ' ': # RIGHT 
                    node.adjacent.append(self.nodes[self.cols*r + c+1])
        return node.adjacent

    def printNodes(self):
        print '================= self.nodes ==============='
        for r,row in enumerate(self.grid):
            for c,col in enumerate(row):
                node = self.nodes[r*self.cols + c]
                print node,col,
            print

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
class Search:
    def __init__(self, graph,start,goal):
        self.graph = graph
        self.start_label = start
        self.goal_label = goal

    def reset(self):
        self.found = False
        for i,node in enumerate(self.graph.nodes):
            self.graph.nodes[i].reset()
        self.reachable = list()
        self.explored = list()
        self.path = list()
        self.start = self.graph.findNodeByLabel(self.start_label)
        self.goal =  self.graph.findNodeByLabel(self.goal_label)
        self.start.bgcolor = blue
        self.goal.bgcolor = red
        self.reachable.append(self.start)
        self.iteration = 0

    def foundPath(self,node):
        if node == self.goal:
            node.Goal = True
            while node:
                self.path.append(node)
                node = node.previous
            print '------------- found path ----------------'
            #self.render()
            self.found = True
            return True

    def step(self):
#       self.iteration += 1
        # choose a node to examine next
        if not self.reachable:
            print '============ No Path Found ============='
            return
        elif self.found :
            return
        node = self.chooseNode()
        # are we done yet?
        if self.foundPath(node): return
        # do not repeat
        self.reachable.remove(node)
        self.explored.append(node)
        # where can we get from here?
        new_reachable = self.graph.getAdjacents(node)
        for adjacent in new_reachable:
            if adjacent in self.reachable or adjacent in self.explored: continue
            adjacent.previous = node
            self.reachable.append(adjacent)
        self.printNodesList()
        for rnode in self.reachable:
            if rnode not in [self.start,self.goal]:
                rnode.bgcolor = green
        for enode in self.explored:
            if enode not in [self.start,self.goal]:
                enode.bgcolor = orange

    def chooseNode(self):
        return choice(self.reachable)
        #return self.reachable[ int(random() * len(self.reachable)) ]

    def render(self):
        print '================== render =============='
        print 'reachable ==>'
        for rnode in self.reachable:
            print rnode.label,
        print
        print 'explored ==>'
        for enode in self.explored:
            print enode.label,
        print
        print 'path  ==>'
        print self.path

    def draw(self,surface):
        self.graph.draw(surface)

    def run(self):
        self.reset()
        while not self.found:
            self.step()

    def printNodesList(self):
        print '============== self.reachable, self.explored  =============='
        for node in self.reachable:
            if node in [self.start,self.goal]: continue
            print node.label,
        print '  :  ',
        for node in self.explored:
            if node in [self.start,self.goal]: continue
            print node.label,
        print


if __name__ == '__main__':
    g = Graph(grid)
    g.printNodes()
    search = Search(g,'A','T')
    search.reset()
    search.render()
    for i in range(40):
        search.step()
#   search.step()
#   print g.labels
#   for node in g.nodes:
#       print node


