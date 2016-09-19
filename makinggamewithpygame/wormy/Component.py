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
        self.x,self.y = self.boardpos.x, self.boardpos.y
    def converToPixelPos(self):
        self.pixelX,self.pixelY = self.x * cellsize, self.y * cellsize

class WormElement(Element):
    def __init__(self,boardpos):
        Element.__init__(self,boardpos)
    def draw(self,surface):
        self.converToPixelPos() #pixelX,pixelY = self.x * cellsize, self.y * cellsize
        self.rect = pygame.Rect( self.pixelX,self.pixelY,cellsize,cellsize )
        self.innerrect = pygame.Rect( self.pixelX+4, self.pixelY+4, cellsize-8, cellsize-8 )
        pygame.draw.rect(surface,darkgreen,self.rect)
        pygame.draw.rect(surface,green,self.innerrect)
        print 'element draw...'

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
    def __init__(self,direction=right):
        startX = random.randint(5,boardwidth-6)
        startY = random.randint(5,boardheight-6)
        headpos = boardPos(startX,startY)
        bodypos = boardPos(startX-1,startY)
        tailpos = boardPos(startX-2,startY)
        head = WormElement(headpos)
        body = WormElement(bodypos)
        tail = WormElement(tailpos)
        self.worm = [head,body,tail]
        self.direction = direction
        self.generateApple()
        self.score = 0

    def isDied(self):
        if self.isHitItself() or self.isHitEdge():
            if len(self.worm) == 0:
                return True
        return False
    def makeMove(self,direction):
        if self.isValidMove(direction): # valid direction
            self.direction = direction 
        else:
            pass # keep going in the last direction
#       if not self.isHitItself() or not self.isHitEdge():
#           self.gameOver()
#           return False

        newhead = copy.copy(self.worm[0])
        if not self.hasEaten():
            self.worm.pop() # remove tail
        if   self.direction == right: newhead.x += +1
        elif self.direction == left:  newhead.x += -1
        elif self.direction == up:    newhead.y += -1
        elif self.direction == down:  newhead.y += +1
        else: raise Exception('no such direction')
        self.worm.insert(0,newhead)

    def isValidMove(self,direction):
        if (self.direction,direction) == (right,left): return False
        if (self.direction,direction) == (left,right): return False
        if (self.direction,direction) == (up,down): return False
        if (self.direction,direction) == (down,up): return False
        return True

    def hasEaten(self):
        head = self.worm[0]
        if (self.apple.x,self.apple.y) == (head.x,head.y):
            self.score += 1
            self.generateApple()
            return True
        return False
    def isHitItself(self):
        head = self.worm[0]
        if (head.x,head.y) in self.getPosList()[1:]:
            self.worm.pop()
            return True
        return False
#       if len(self.worm) == 0:
#           return False

    def isHitEdge(self):
        head = self.worm[0]
        if head.x == -1:
            head.x = boardwidth -1
            self.worm.pop() # remove tail
        elif head.y == -1:
            head.y = boardheight -1
            self.worm.pop() # remove tail
        elif head.x == boardwidth:
            head.x = 0
            self.worm.pop() # remove tail
        elif head.y == boardheight:
            head.y = 0
            self.worm.pop() # remove tail
        else:
            return False
        return True
#       if len(self.worm) == 0:
#           return False

    def getPosList(self):
        poslist = []
        for e in self.worm:
            poslist.append((e.x,e.y))
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

def terminate():
    pygame.quit(); sys.exit()

def drawPressKeyMsg(surface,basicfont):
    presskey_surf = basicfont.render('Press a key to play', True, darkgray)
    presskey_rect = presskey_surf.get_rect()
    presskey_rect.topleft = (width-200,height-30)
    surface.blit(presskey_surf,presskey_rect)

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
            terminate()
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0: return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key # KEYUP event

def drawGrid(surface):
    for x in range(0,width,cellsize): # draw verticals
        pygame.draw.line(surface,darkgray,(x,0),(x,height))
    for y in range(0,height,cellsize): # draw verticals
        pygame.draw.line(surface,darkgray,(0,y),(width,y))

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

