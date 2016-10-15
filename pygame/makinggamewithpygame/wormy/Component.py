import pygame, sys, random, copy
from pygame.locals import *
from constants import *

class boardPos:
    def __init__(self,x,y):
        self.x,self.y = x,y
    def __iter__(self):
        return iter((self.x, self.y) )

class Element(object):
    def __init__(self,boardpos):
        self.boardpos = boardpos
        self.x,self.y = boardpos.x, boardpos.y
    def __eq__(self,other):
        return (self.x,self.y) == (other.x,other.y)
    def converToPixelPos(self):
        self.pixelX,self.pixelY = self.x * cellsize, self.y * cellsize
        return (self.pixelX,self.pixelY)
    def __str__(self):
        return '(%s,%s)' %(self.x,self.y)

class WormElement(Element):
    def __init__(self,boardpos):
        Element.__init__(self,boardpos)
    def draw(self,surface):
        self.converToPixelPos() #pixelX,pixelY = self.x * cellsize, self.y * cellsize
        self.rect = pygame.Rect( self.pixelX,self.pixelY,cellsize,cellsize )
        self.innerrect = pygame.Rect( self.pixelX+4, self.pixelY+4, cellsize-8, cellsize-8 )
        pygame.draw.rect(surface,darkgreen,self.rect)
        pygame.draw.rect(surface,green,self.innerrect)

class Apple(Element):
    def __init__(self,boardpos):
        Element.__init__(self,boardpos)
    def draw(self,surface):
        self.converToPixelPos()
        self.rect = pygame.Rect(self.pixelX,self.pixelY,cellsize,cellsize)
        self.innerrect = pygame.Rect( self.pixelX+4, self.pixelY+4, cellsize-8, cellsize-8 )
        pygame.draw.rect(surface,darkred,self.rect)
        pygame.draw.rect(surface,red,self.innerrect)

class Worm:
    def __init__(self):
        self.direction = right
        self.score = 0
        self.worm = []
        startX = random.randint(5,boardwidth-6)
        startY = random.randint(5,boardheight-6)
        for i in range(5):
            boardpos = boardPos(startX-i,startY)
            element = WormElement(boardpos)
            self.worm.append(element)
        # after worm created
        self.generateApple()

    def isDied(self):
#       if self.isHitItself() or self.isHitEdge():
        if len(self.worm) == 0:
            print 'isDied'
            return True
        return False

    def hasEaten(self):
        if self.worm[0] == self.apple: # head = self.worm[0]
            self.score += 1
            self.generateApple()
            return True
        return False

    def makeMove(self,direction):
        if self.isValidMove(direction): # valid direction
            self.direction = direction 
        else:
            pass # keep going in the last direction

        assert self.isDied()==False, len(self.worm)
        if len(self.worm) <= 3:
            print 'warning ...'

        head = self.worm[0]
        print head

        # make move
        newhead = copy.copy(head)
        if not self.hasEaten():
            self.worm.pop() # remove tail
        if   self.direction == right: newhead.x += +1
        elif self.direction == left:  newhead.x += -1
        elif self.direction == up:    newhead.y += -1
        elif self.direction == down:  newhead.y += +1
        else: raise Exception('no such direction')
        self.worm.insert(0,newhead) # add new head

    def checkForCollision(self): # collision detection

        if self.isHitItself():
            print 'hit itself...'
            #pygame.time.wait(2000)
            self.worm.pop()
        elif self.isHitEdge(): # hit one of four edges
            print 'hit edge...'
            #pygame.time.wait(2000)
            head = self.worm[0]
            self.worm.pop() # remove tail
            # change head position 
            if head.x == -1:            # hit left wall
                head.x = boardwidth -1
            elif head.x == boardwidth:  # hit right wall
                head.x = 0
            elif head.y == -1:          # hit top wall
                head.y = boardheight -1
            elif head.y == boardheight: # hit bottom wall
                head.y = 0

    def isValidMove(self,direction):
        if (self.direction,direction) == (right,left): return False
        if (self.direction,direction) == (left,right): return False
        if (self.direction,direction) == (up,down): return False
        if (self.direction,direction) == (down,up): return False
        return True

    def isHitItself(self):
        head = self.worm[0]
        return (head.x,head.y) in self.getPosList()[1:]

    def isHitEdge(self):
        head = self.worm[0]
        return not ( head.x in range(boardwidth) and head.y in range(boardheight) )

    def getPosList(self):
        poslist = []
        for element in self.worm:
            poslist.append((element.x,element.y))
        return poslist

    def generateApple(self):
        poslist = self.getPosList()
        while True:
            x = random.randint(0,boardwidth-1)
            y = random.randint(0,boardheight -1)
            applepos = boardPos(x,y)
            if (applepos.x,applepos.y) in poslist: continue
            self.apple = Apple(applepos) 
            return True

    def draw(self,surface):
        for part in self.worm: #print part.x,part.y
            part.draw(surface)
            if part == self.worm[0]: #if self.worm.index(part) == 0:
                pygame.draw.rect(surface,blue,part.innerrect)
        self.apple.draw(surface)
        self.drawScore(surface)
    def drawScore(self,surface):
        scorefont = pygame.font.Font('freesansbold.ttf',20)
        scoresurf = scorefont.render('Score: %s' %self.score, True,white)
        scorerect = scoresurf.get_rect()
        scorerect.topleft = (width-120,10)
        surface.blit(scoresurf,scorerect)


if __name__ == '__main__':

    print right
    pygame.init()
    surface = pygame.display.set_mode((width,height))
    pygame.display.set_caption('Wormy')
    worm = Worm()
    move = right
    while True:
        surface.fill(bgcolor)
        #worm.draw(surface)
        for e in pygame.event.get():
            if e.type == QUIT:
                terminate()
            elif e.type == KEYDOWN:
                if   e.key in (K_LEFT, K_a):    move = left
                elif e.key in (K_RIGHT, K_d):   move = right
                elif e.key in (K_UP,K_w):       move = up
                elif e.key in (K_DOWN,K_s):     move = down
                elif e.key == K_ESCAPE:         terminate()

        worm.makeMove(move)
        worm.draw(surface)
        pygame.display.update()
        pygame.time.wait(200)

