import pygame, sys, random, winsound
#from pygame.locals import *
import itertools, copy
from constant import *
fpsclock = pygame.time.Clock()

class boardCoord:
    def __init__(self,x,y):
        self.x,self.y = x,y
    def __str__(self):
        return '(%s,%s)' %(self.x,self.y)
    def __repr__(self):
        return self.__str__()

def boardToScreen(boardcoord): # convert board coordinates to screen positions
    left = boardcoord.x * (boxsize + gapsize) + xmargin
    top  = boardcoord.y * (boxsize + gapsize) + ymargin
    return (left,top)


class Box:

    def __init__(self,tu): #shape,color):
        self.shape, self.color = tu #shape,color
        self.revealed = False
        self.surface = pygame.Surface( [boxsize,boxsize] )
        self.surface.fill(bgcolor)
        self.rect  = self.surface.get_rect()

    def __eq__(self,other):
        if isinstance(other,self.__class__):
            if (self.shape,self.color) == (other.shape,other.color):
                return True
        return False

    def __ne__(self,other): # not __eq__
        return not self.__eq__(other)

    def setboardCoord(self,boardcoord):
        self.screenpos = boardToScreen(boardcoord)
        print self.screenpos
        assert type(self.screenpos[0]) == int, self.screenpos[0]
        assert type(self.screenpos[1]) == int, self.screenpos[1]

#   def draw(self,surface):
#       if self.revealed:
#           self.drawIcon()
#       else:
#           self.drawCover()
#       self.rect.center = self.screenpos
#       surface.blit(self.surface,self.rect)
#       print self.screenpos,self.revealed
#       surface.blit(self.surface,self.screenpos)

    def drawDonut(self,half,quarter):
        pygame.draw.circle(self.surface,self.color,self.rect.center,half-5)
        pygame.draw.circle(self.surface,bgcolor,self.rect.center,quarter-5)

    def drawSquare(self,half,quarter):
        rect = quarter,quarter,boxsize-half,boxsize-half 
        pygame.draw.rect(self.surface,self.color,rect)

    def drawDiamond(self,half,quarter):
        pointList = (half, 0), (boxsize-1,half), (half,boxsize-1), (0,half)
        pygame.draw.polygon(self.surface,self.color,pointList)

    def drawLines(self):
        for i in range(0,boxsize,4):
            pygame.draw.line(self.surface,self.color,(0,i),(i,0))
            pygame.draw.line(self.surface,self.color,(i,boxsize-1),(boxsize-1,i))

    def drawOval(self,half,quarter):
        pygame.draw.ellipse(self.surface,self.color, (0, quarter,boxsize,half) )

    def drawIcon(self):
        quarter,half = int(boxsize/4), int(boxsize/2)
        # draw the shapes
        if   self.shape == donut:   self.drawDonut(half,quarter)
        elif self.shape == square:  self.drawSquare(half,quarter)
        elif self.shape == diamond: self.drawDiamond(half,quarter)
        elif self.shape == lines:   self.drawLines()
        elif self.shape == oval:    self.drawOval(half,quarter)

    def drawCover(self):
#       self.surface.fill(bgcolor)
        print 'draw cover ...'
        pygame.draw.rect(self.surface,boxcolor,(0,0,boxsize-1,boxsize-1))

    def drawHighlight(self,surface):
        rect = (x-5,y-5,boxsize+10,boxsize+10)
        pygame.draw.rect(surface,highlightcolor,rect,4)


class Board:

    def __init__(self):
        self.board = self.getRandomizedBoard()
        # set box Position in board
        for index,box in enumerate(self.board):
            boardcoord = self.convertTo2D(index)
            box.setboardCoord(boardcoord)
    def getRandomizedBoard(self):
        # get a list of every possible shape in every possible color
        icons = itertools.product(allshapes,allcolors)
        boxes = list( itertools.imap(Box,icons)  )
        random.shuffle(boxes)
        # calculate how many icons are needed
        numOfIcons = int( boardwidth*boardheight/2 )
        # need pairs, and not shallow copy
        boardhalf = boxes[:numOfIcons]
#       board = boardhalf + copy.deepcopy(boardhalf)
        board = boardhalf + copy.copy(boardhalf)
        random.shuffle(board)
        return board
    def drawBoard(self,surface):
        for box in self.board:
            print box.shape,box.color,box.revealed
            surface.blit(box.surface,box.screenpos)
    def coverBoxesAnimation(self,surface,boxes):
        coverages = range(1, boxsize, revealspeed)
        if boxsize not in coverages: coverages.append(boxsize)
        for coverage in coverages: 
            if coverage > boxsize: continue
            for box in boxes:
                rect = box.pos,(coverage,boxsize)
                box.drawCover(surface,rect)
#           pygame.display.update()
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
#           pygame.display.update()
            fpsclock.tick(2*fps)
    def startGameAnimation(self,surface):
        #surface.fill(bgcolor)
        self.drawBoard(surface)
        # shallow copy needed here
        # A = [box1,box2,box3] , B = A[:], random.shuffle(B)
        # B = [box2,box1,box3], 'box1 of A' is 'box1 of B'
        shallowboard = self.board[:] 
        random.shuffle(shallowboard)
        boxgroups = groupOf( 8,shallowboard )
        for boxgroup in boxgroups:
            for box in boxgroup:
                box.revealed = True
            self.revealBoxesAnimation(surface, boxgroup)
            pygame.time.wait(500)
            self.coverBoxesAnimation(surface, boxgroup)
            for box in boxgroup:
                box.revealed = False
    def gameWonAnimation(self,surface):
        color1,color2 = lightbgcolor, bgcolor
        for i in range(10):
            color1,color2 = color2,color1
            surface.fill(color1)
            self.drawBoard(surface)
#           pygame.display.update()
            pygame.time.wait(100)

    def getBoxAt(self,mouseX,mouseY):
        for box in self.board:
            boxrect = pygame.Rect(*box.rect)
            if boxrect.collidepoint(mouseX,mouseY):
                return box
        # outside of Box
        return None

    def convertTo2D(self,index):
        x,y = index % boardwidth, index // boardwidth
        return boardCoord(x,y) 

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


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption('Memory Puzzle Game')
    screen.fill(bgcolor)
    board = Board()
    board.drawBoard(screen)
#   box = Box( ['oval',red] )
#   box.revealed = True
#   box.setboardCoord( boardCoord(1,1))
#   box1 = copy.deepcopy(box)
#   box1.setboardCoord( boardCoord(1,1))
#   box.draw(screen)
#   box1.draw(screen)
    pygame.time.wait(5000)
    pygame.display.flip()

