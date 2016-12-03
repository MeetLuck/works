from random import random,choice
from colors import *
import pygame

maps = [
        [list("   * "),
         list(" *** "),
         list("     "),
         list("* ** "),
         list("*    ") ],

        [list("        "),
         list("    *   "),
         list("    *   "),
         list("    *   "),
         list("        "),
         list("        ")],
        ]

amap = maps[1]

angle,scale = 0,0.5
imgN = pygame.image.load('../arrow-N.png')
imgS = pygame.image.load('../arrow-S.png')
imgE = pygame.image.load('../arrow-E.png')
imgW = pygame.image.load('../arrow-W.png')

imgNEWS = {'N':imgN, 'S':imgS, 'E':imgE, 'W':imgW }
for direction,img in imgNEWS.items():
    img0 = pygame.transform.rotozoom(img,angle,scale)
    imgNEWS[direction] = img0
imgNE = pygame.transform.rotozoom(imgE,+45,scale)
imgSE = pygame.transform.rotozoom(imgE,-45,scale)
imgNW = pygame.transform.rotozoom(imgW,-45,scale)
imgSW = pygame.transform.rotozoom(imgW,+45,scale)
imgNEWS.update( {'NE':imgNE,'SE':imgSE,'NW':imgNW,'SW':imgSW } )

import collections
class Queue:
    def __init__(self):
        self.elements = collections.deque()
    def empty(self):
        return len(self.elements) == 0
    def put(self,val):
        self.elements.append(val)
    def get(self):
        return self.elements.popleft()

def printNodesList(search):
    print '============== self.reachable, self.explored  =============='
    for node in search.reachable:
        #if node in [self.start,self.goal]: continue
        print node.label,
    print '  :  ',
    for node in search.explored:
        #if node in [self.start,self.goal]: continue
        print '%s(%s)' %(node.label,node.camefrom),
    print

def printNodes(graph):
    print '================= self.nodes ==============='
    for r,row in enumerate(graph.grid):
        for c,col in enumerate(row):
            node = graph.grid[r][c]
            print 'g[%s][%s] = %s' %(r,c,node.label),
        print
def renderSearch(search):
    print '================== render =============='
    print 'reachable ==>'
    for rnode in search.reachable:
        print rnode.label,
    print
    print 'explored ==>'
    for enode in search.explored:
        print enode.label,
    print
    print 'path  ==>'
    print search.path
