from constants import *

class boardPos:
    def __init__(self,x,y):
        self.x,self.y = x,y
    def __iter__(self):
        return iter((self.x, self.y) )

class WarmParts:
    def __init__(self,boardpos=None):
        self.boardpos = boardPos(None,None)
        self.x,self.y = boardpos.x, boardpos.y
    def setBoardPos(self,boardpos):
        self.boardpos = boardpos
        self.x,self.y = boardpos.x, boardpos.y
class Warm:
    def __init__(self,direction=right):
        startX = 15 #random.randint(10,boardwidth-6)
        startY = 15 #random.randint(10,boardheight-6)
        headpos = boardPos(startX,startY)
        bodypos = boardPos(startX-1,startY)
        tailpos = boardPos(startX-2,startY)
        head = WarmParts(headpos)
        body = WarmParts(bodypos)
        tail = WarmParts(tailpos)
        self.poslist = [head,body,tail]
        self.direction = direction
    def makeMove(self,direction):
        if not self.isValidMove(direction): return None
        self.direction = direction
        newhead = copy.copy(self.poslist[0])
        self.poslist.pop() # remove tail
        if   self.direction == right: newhead.x += +1
        elif self.direction == left:  newhead.x += -1
        elif self.direction == up:    newhead.y += -1
        elif self.direction == down:  newhead.y += +1
        else: raise Exception('no such direction')
        self.poslist.insert(0,newhead)
    def isValidMove(self,direction):
        if self.direction == right and direction == left: return False
        if self.direction == left and direction == right: return False
        if self.direction == up and direction == down: return False
        if self.direction == down and direction == up: return False
        return True
    def draw(self,surface):
        for part in self.poslist:
            #print part.x,part.y
            x,y = part.x * cellsize, part.y * cellsize
            wormrect = pygame.Rect( x,y,cellsize,cellsize )
            worminnerrect = pygame.Rect( x+4, y+4, cellsize-8, cellsize-8 )
            pygame.draw.rect(surface,darkgreen,wormrect)
            pygame.draw.rect(surface,green,worminnerrect)


if __name__ == '__main__':
    import pygame, sys, random, copy
    from pygame.locals import *

    print right
    pygame.init()
    surface = pygame.display.set_mode((width,height))
    pygame.display.set_caption('Wormy')
    warm = Warm()
    while True:
        surface.fill(bgcolor)
        #warm.draw(surface)
        move = random.choice([up,down,right,left])
        warm.makeMove(move)
        warm.draw(surface)
        pygame.display.update()
        pygame.time.wait(500)

