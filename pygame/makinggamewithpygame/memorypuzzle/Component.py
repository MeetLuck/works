import pygame, sys, random, winsound
from pygame.locals import *
import itertools
from constant import *
fpsclock = pygame.time.Clock()

class boardPos:
    def __init__(self,x,y):
        self.x,self.y = x,y
    def __str__(self):
        return '(%s,%s)' %(self.x,self.y)
    def __repr__(self):
        return self.__str__()

def convertToDisplayPos(boardpos): # convert board coordinates to display coordinates
    left = boardpos.x * (boxsize + gapsize) + xmargin
    top  = boardpos.y * (boxsize + gapsize) + ymargin
    return (left,top)

class Box:

    def __init__(self,tu): #shape,color):
        self.shape, self.color = tu #shape,color
        self.revealed = False

    def __eq__(self,other):
        if isinstance(other,self.__class__):
            if (self.shape,self.color) == (other.shape,other.color):
                return True
        return False

    def __ne__(self,other):
        return not self.__eq__(other)

    def setboardPos(self,boardpos):
        self.boardpos = boardpos
        self.pos = convertToDisplayPos(boardpos)
        self.rect = self.pos, (boxsize, boxsize)

    def draw(self,surface):
        # tuple pos : display Position (x,y)
        if self.revealed:
            self.drawIcon(surface)
        else:
            self.drawCover(surface)

    def drawIcon(self,surface):
        # print 'drawIcon....'
        quarter,half = int(boxsize/4), int(boxsize/2)
        x,y = self.pos
        # draw background rect
        pygame.draw.rect(surface,bgcolor,self.rect)
        # draw the shapes
        if self.shape == donut:
            pygame.draw.circle(surface,self.color,(x+half,y+half),half-5)
            pygame.draw.circle(surface,bgcolor,(x+half,y+half),quarter-5)
        elif self.shape == square:
            rect = (x+quarter, y+quarter, boxsize-half, boxsize-half )
            pygame.draw.rect(surface,self.color,rect)
        elif self.shape == diamond:
            pointList = (x+half, y), (x+boxsize-1,y+half), (x+half,y+boxsize-1), (x,y+half)
            pygame.draw.polygon(surface,self.color,pointList)
        elif self.shape == lines:
            for i in range(0,boxsize,4):
                pygame.draw.line(surface,self.color,(x,y+i),(x+i,y))
                pygame.draw.line(surface,self.color,(x+i,y+boxsize-1),(x+boxsize-1,y+i))
        elif self.shape == oval:
            pygame.draw.ellipse(surface,self.color, (x, y+quarter,boxsize,half) )

    def drawCover(self,surface,rect=None):
        if rect == None:
            rect = self.rect
        pygame.draw.rect(surface,boxcolor,rect)

    def drawHighlight(self,surface):
        x,y = self.pos
        rect = (x-5,y-5,boxsize+10,boxsize+10)
        pygame.draw.rect(surface,highlightcolor,rect,4)

class Board:

    def __init__(self):
        self.board = self.getRandomizedBoard()
        # set box Position in board
        for index,box in enumerate(self.board):
            boardpos = self.convertTo2D(index)
            box.setboardPos(boardpos)

    def getRandomizedBoard(self):
        import itertools, copy
        # get a list of every possible shape in every possible color
        icons = itertools.product(allshapes,allcolors)
        boxes = list( itertools.imap(Box,icons)  )
        random.shuffle(boxes)
        # calculate how many icons are needed
        numOfIcons = int( boardwidth*boardheight/2 )
        # need pairs, and not shallow copy
        boardhalf = boxes[:numOfIcons]
        board = boardhalf + copy.deepcopy(boardhalf)
        random.shuffle(board)
        return board

    def drawBoard(self,surface):
        # draws all of the boxes in their covered or revealeded state
        for box in self.board:
            box.draw(surface)

    def coverBoxesAnimation(self,surface,boxes):
        coverages = range(1, boxsize, revealspeed)
        if boxsize not in coverages:
            coverages.append(boxsize)
        for coverage in coverages: 
            if coverage > boxsize: continue
            for box in boxes:
                rect = box.pos,(coverage,boxsize)
                box.drawCover(surface,rect)
            pygame.display.update()
            fpsclock.tick(2*fps)

    def revealBoxesAnimation(self,surface,boxes):
        coverages = range(boxsize,0,-revealspeed)
        if 0 not in coverages: coverages.append(0)
        for coverage in coverages:
            for box in boxes:
                box.draw(surface)
                rect = box.pos,(coverage,boxsize)
                if coverage > 0:
                    box.drawCover(surface,rect)
            pygame.display.update()
            fpsclock.tick(2*fps)

    def gameWonAnimation(self,surface):
        color1,color2 = lightbgcolor, bgcolor
        for i in range(10):
            color1,color2 = color2,color1
            surface.fill(color1)
            self.drawBoard(surface)
            pygame.display.update()
            pygame.time.wait(100)

    def startGameAnimation(self,surface):
        import copy
        self.drawBoard(surface)
        # shallow copy needed here
        # A = [box1,box2,box3] , B = A[:]
        # B = [box2,box1,box3], 'box1 of A' is 'box1 of B'
        shallowboard = self.board[:] 
        # change box attribute : box.revealed
        random.shuffle(shallowboard)
        boxgroups = groupOf( 8,shallowboard )
        for boxgroup in boxgroups:
            for box in boxgroup:
                box.revealed = True   
            surface.fill(bgcolor)
            self.drawBoard(surface)
            pygame.time.wait(500)
            # reset box.revealed = False
            for box in boxgroup:
                box.revealed = False

    def getBoxAtPos(self,boardpos):
        return self.board[ boardpos.x + boardwidth * boardpos.y ]

    def getBoxAtPosXY(self,boardX,boardY):
        boardpos = boardPos(boardX,boardY)
        return self.getBoxAtPos(boardpos)
    def getBoardPosAt(self,mouseX,mouseY):
        for box in self.board:
            boxrect = pygame.Rect(*box.rect)
            if boxrect.collidepoint(mouseX,mouseY):
                return box.boardpos
        # outside of Box
        return None
    def convertTo1D(self,boardpos):
        return boardpos.x + boardwidth * boardpos.y

    def convertTo2D(self,index):
        x,y = index % boardwidth, index // boardwidth
        return boardPos(x,y) 
    def hasWon(self):
        for box in self.board:
            if box.revealed == False:
                return False
        return True

def groupOf(n,seq):
    " [ group0,group1,...,groupN ] "
    groups = []
    for i in range(0, len(seq), n):
        group = seq[i:i+n]
        groups.append(group)
    return groups
