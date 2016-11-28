from random import random
from colors import *
import pygame
bgcolor = lightgray

grid = ["   * ",
        " *** ",
        "     ",
        "* ** ",
        "*    "]

def findNode(node,lst):
    return node in lst

class Node:
    def __init__(self):
        self.wall = False
        self.adjacent = [] # UP,DOWN,LEFT,RIGHT(NWSE)
        self.previous = None
        self.label = ""
        self.color = black
        self.bgcolor = bgcolor
    def clear(self):
        self.previous = None
        self.cost = 'Infinity'
    def __str__(self):
        return self.label
    def draw(self):
        if self.wall: self.bgcolor = purple
        self.image = pygame.Surface((50,50))
        self.image.fill(self.bgcolor)
        font = pygame.font.SysFont('Arial', 20)
        text = font.render(self.label, True, self.color)
        rect = text.get_rect()
        rect.center = self.image.get_rect().center
        self.image.blit(text,rect)
        return self.image

class Graph:
    def __init__(self,grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.nodes = list()
        self.labels = list()
        self.createNodes()
#       for i in range(65,91):
#           self.labels.append( chr(i) )
    def createNodes(self):
        # create one node per square in the grid
        i = 65
        for row in self.grid:
            for col in row:
                node = Node()
                node.label = chr(i)
                if col == '*':
                    node.wall = True
                self.nodes.append(node)
                i += 1
#       for i in range(self.rows*self.cols):
#           node = Node()
#           node.label = self.labels[i]
#           self.nodes.append(node)
        # add edges to adjacent nodes
        for r in range(self.rows):
            for c in range(self.cols):
                node = self.nodes[self.cols * r + c]
                # ignore blocked squares
                if grid[r][c] == '*': continue
                # figure out the adjacent nodes
                if r > 0 and grid[r-1][c] == ' ': # UP 
                    node.adjacent.append(self.nodes[self.cols*(r-1) + c])
                if r < self.rows-1 and grid[r+1][c] == ' ': # DOWN
                    node.adjacent.append(self.nodes[self.cols*(r+1) + c])
                if c > 0 and grid[r][c-1] == ' ': # LEFT
                    node.adjacent.append(self.nodes[self.cols*r + c-1])
                if c < self.cols-1 and grid[r][c+1] == ' ': # RIGHT 
                    node.adjacent.append(self.nodes[self.cols*r + c+1])

    def findNodeByLabel(self,label):
        for i,val in enumerate(self.nodes):
            if self.nodes[i].label == label:
                return val
    def draw(self,surface):
        for row in range(self.rows):
            for col in range(self.cols):
                node = self.nodes[self.cols*row + col]
                image = node.draw()
                topleft = row*50,col*50
                surface.blit(image,topleft)
        return surface

# Search
class Search:
    def __init__(self, graph,start,goal):
        self.graph = graph
        self.reachable = list()
        self.explored = list()
        self.path = list()
        self.start_label = start
        self.goal_label = goal

    def reset(self):
        self.start = self.graph.findNodeByLabel(self.start_label)
        self.goal =  self.graph.findNodeByLabel(self.goal_label)
        self.start.bgcolor = green
        self.goal.bgcolor = red
        self.reachable.append(self.start)
        self.explored = list()
        self.path = list()
        self.iteration = 0
        for i,node in enumerate(self.graph.nodes):
            self.graph.nodes[i].clear()
        #self.reachable[0].cost = 0
        #self.render()

    def step(self):
        if len(self.path) > 0: # is the search already done ?
            return
        # if there are no more nodes to consider, we're done
        if len(self.reachable) == 0:
            self.finished = True
            return
        self.iteration += 1
        # choose a node to examine next
        node = self.chooseNode()
        # are we done yet?
        if node== self.goal:
            while node:
                self.path.append(node)
                node = node.previous
            print '------------- find path ----------------'
            self.render()
            return
        # do not repeat
        self.reachable.remove(node)
        self.explored.append(node)
        if node in self.explored:
            if node != self.start:
                node.bgcolor = orange
        # where can we get from here?
#       self.render()
#       if node is None: return
        for adjnode in node.adjacent:
            self.addAdjacent(node,adjnode)
        self.render()

    def chooseNode(self):
        return self.reachable[ int(random() * len(self.reachable)) ]

    def addAdjacent(self,node,adjacent):
        if findNode(adjacent,self.explored) or findNode(adjacent,self.reachable):
            return
        adjacent.previous = node
        self.reachable.append(adjacent)

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


if __name__ == '__main__':
    g = Graph(grid)
    search = Search(g,'A','T')
    search.reset()
    search.render()
    for i in range(40):
        search.step()
#   search.step()
#   print g.labels
#   for node in g.nodes:
#       print node


