#import pygame,sys,random
#import itertools
#from pygame.locals import *
#from constant import *

class boardPos:
    def __init__(self,x,y):
        self.x,self.y = x,y

class Box:
    def __init__(self,tu): #shape,color):
        self.shape, self.color = tu #shape,color
        self.reveal = False

    def getDisplayPos(self,boardpos):
        '''
        convert board coordinates to display coordinates
        boardpos = boardPos(boardX, boardY)
        return tuple (displayX, displayY)
        '''
        left = boardpos.x * (boxsize + gapsize) + xmargin
        top  = boardpos.y * (boxsize + gapsize) + ymargin
        return (left,top)

    def getDisplayPosXY(self,boardX,boardY):
        return self.getDisplayPos( boardPos(boardX,boardY) )

    def drawXY(self,surface,boardX,boardY):
        self.draw( surface,boardPos(boardX,boardY) )
    def draw(self,surface,boardpos):
        # tuple pos : display Position (x,y)
        pos = self.getDisplayPos(boardpos)
        if self.reveal:
            self.drawIcon(surface,pos)
        else:
            self.drawCover(surface,pos)

    def drawIcon(self,surface,pos):
        quarter = int(boxsize/4)
        half    = int(boxsize/2)
        x,y = pos
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
        pygame.display.update()
        #fpsclock.tick(fps)

    def drawCover(self,surface,pos):
        rect = pos,(boxsize,boxsize)
        pygame.draw.rect(surface,boxcolor,rect)
        pygame.display.update()
        #fpsclock.tick(fps)

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

    def drawBoard(self,surface):
        # draws all of the boxes in their covered or revealed state
        for index,box in enumerate(self.board):
            x = index % boardwidth 
            y = index // boardwidth
            boardpos = boardPos(x,y)
            box.draw(surface, boardpos)

    def getBoxPos(self,boardpos):
        return self.board[ boardpos.x + boardwidth * boardpos.y ]

    def getBoxPosXY(self,boardX,boardY):
        boardpos = boardPos(boardX,boardY)
        return self.getBoxPos(boardpos)

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

