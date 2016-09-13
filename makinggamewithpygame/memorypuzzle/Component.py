import pygame,sys,random
import itertools
from pygame.locals import *
from constant import *
surface = pygame.display.set_mode(resolution)

class Box:
    def __init__(self,tu): #shape,color):
        self.shape, self.color = tu #shape,color
        self.reveal = False
    def draw(self):
        if self.reveal:
            self.drawIcon()
        else:
            self.drawCover()
    def drawIcon(self):
        quarter = int(boxsize/4)
        half    = int(boxsize/2)
#       left,top = leftTopCoordsOfBox(boxx,boxy)
        # draw the shapes
        if self.shape == donut:
            pygame.draw.circle(surface,self.color,(half,half),half-5)
            pygame.draw.circle(surface,bgcolor,(half,half),quarter-5)
        elif self.shape == square:
            pygame.draw.rect(surface,self.color,(quarter,quarter,boxsize-half,boxsize-half) )
        elif self.shape == diamond:
            pygame.draw.polygon(surface,self.color,((half,0), (boxsize-1,half),(half,boxsize-1),(0,half) ) )
        elif self.shape == lines:
            for i in range(0,boxsize,4):
                pygame.draw.line(surface,self.color,(0,i),(i,0))
                pygame.draw.line(surface,self.color,(i,boxsize-1),(boxsize-1,i))
        elif shape == oval:
            pygame.draw.ellipse(surface,self.color, (0, quarter,boxsize,half) )
        pygame.display.update()
        fpsclock.tick(fps)
    def drawCover(self):
        pygame.draw.rect(surface,boxcolor,(0,0,boxsize,boxsize) )
        pygame.display.update()
        fpsclock.tick(fps)

class Board:
    def __init__(self):
        self.board = self.getRandomizedBoard()
    def getRandomizedBoard(self):
        # get a list of every possible shape in every possible color
        icons = itertools.product(allshapes,allcolors)
        board = itertools.imap(Box,icons)
        board = list(board)
        random.shuffle(board)
        # calculate how many icons are needed
        numiconsused = int( boardwidth*boardheight/2 )
        # need pairs
        board = board[:numiconsused] * 2 # [1,2,3]*2 = [1,2,3,1,2,3]
        random.shuffle(board)
        return board
    def getBoxAtXY(self,x,y):
        return self.board[ x + boardwidth*y ]


if __name__ == '__main__':
    fps = 20
    pygame.init()
    surface = pygame.display.set_mode(resolution)
    fpsclock = pygame.time.Clock()
    box1 = Box(donut,blue)
    while True: # main loop
        surface.fill(bgcolor)
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                pygame.quit(); sys.exit()
        box1.draw()
#       pygame.time.wait(1000)
#       box2 = Box(donut,red,reveal=True)
#       box2.draw()
        # redraw the screen and wait a clock tick
        box1.reveal = not box1.reveal
        pygame.display.update()
        fpsclock.tick(fps)

    print dir()

