import pygame, sys, random
from pygame.locals import *
from constants import *

def main():
    global fpsclock,surface,basicfont
    pygame.init()
    fpsclock = pygame.time.Clock()
    surface = pygame.display.set_mode(resolution)
    basicfont = pygame.font.Font('freesansbold.ttf',18)
    pygame.display.set_caption('Wormy')

    #showStartScreen()
    while True:
        runGame()
        showGameOverScreen()

def runGame():
    # set a random start point
    startX = random.randint(5,boardwidth-6)
    startY = random.randint(5,boardheight-6)
    wormcoords = [ {'x':startX, 'y':startY},
                   {'x':startX-1, 'y':startY},
                   {'x':startX-2, 'y':startY}]
    direction = right
    # start the apple in a random place
    apple = getRandomLocation()
    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                terminate()
            elif e.type == KEYDOWN:
                if (e.key == K_LEFT or e.key == K_a) and direction != right:
                    direction = left
                elif (e.key == K_RIGHT or e.key == K_d) and direction != left:
                    direction = right
                elif (e.key == K_UP or e.key == K_w) and direction != down:
                    direction = up
                elif (e.key == K_DOWN or e.key == K_s) and direction != up:
                    direction = down
                elif e.key==K_ESCAPE:
                    terminate()
        # check if worm has hit itself or the edge
        if wormcoords[head]['x'] == -1 or wormcoords[head]['x'] == boardwidth: return
        if wormcoords[head]['y'] == -1 or wormcoords[head]['y'] == boardheight: return
        for wormbody in wormcoords[1:]: # hit itself
            if wormbody['x'] == wormcoords[head]['x'] and wormbody['y'] == wormcoords[head]['y']:
                return
        # check if worm has eaten and apple
        if wormcoords[head]['x'] == apple['x'] and wormcoords[head]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation() # set a new apple
        else:
            del wormcoords[-1] # remove worm's tail segment
        # move the worm by adding a segment in the direction it is moving
        if direction == up:
            newhead = {'x':wormcoords[head]['x'],'y':wormcoords[head]['y']-1}
        elif direction == down:
            newhead = {'x':wormcoords[head]['x'],'y':wormcoords[head]['y']+1}
        elif direction == left:
            newhead = {'x':wormcoords[head]['x']-1,'y':wormcoords[head]['y']}
        elif direction == right:
            newhead = {'x':wormcoords[head]['x']+1,'y':wormcoords[head]['y']}
        wormcoords.insert(0,newhead)
        surface.fill(bgcolor)
        drawGrid()
        drawWorm(wormcoords)
        drawApple(apple)
        drawScore(len(wormcoords)-3)
        pygame.display.update()
        fpsclock.tick(fps)

def drawPressKeyMsg():
    presskeysurf = basicfont.render('Press a key to play.',True, darkgray)
    presskeyrect = presskeysurf.get_rect()
    presskeyrect.topleft = (width-200,height-30)
    surface.blit(presskeysurf,presskeyrect)
def checkForKeyPress():
    if len(pygame.event.get(QUIT))>0:
        terminate()
    KeyUpEvents = pygame.event.get(KEYUP)
    if len(KeyUpEvents) == 0:
        return None
    if KeyUpEvents[0].key == K_ESCAPE:
        terminate()
    return KeyUpEvents[0].key
def showStartScreen():
    tilefont = pygame.font.Font('freesansbold.ttf',100)
    tilesurf1 = tilefont.render('Wormy!',True, white, darkgreen)
    tilesurf2 = tilefont.render('Wormy!',True, green)
    degrees1 = 0
    degrees2 = 0

    while True:
        surface.fill(bgcolor)

        rotatesurf1 = pygame.transform.rotate(tilesurf1,degrees1)
        rotaterect1 = rotatesurf1.get_rect()
        rotaterect1.center = (width/2, height/2)
        surface.blit(rotatesurf1,rotaterect1)

        rotatesurf2 = pygame.transform.rotate(tilesurf2,degrees1)
        rotaterect2 = rotatesurf2.get_rect()
        rotaterect2.center = (width/2, height/2)
        surface.blit(rotatesurf2,rotaterect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        fpsclock.tick(fps)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame

def terminate():
    pygame.quit(); sys.exit()
def getRandomLocation():
    return {'x':random.randint(0,boardwidth-1), 'y':random.randint(0,boardheight-1) }
def showGameOverScreen():
    gameoverfont = pygame.font.Font('freesansbold.ttf',150)
    gamesurf = gameoverfont.render('Game',True,white)
    oversurf = gameoverfont.render('Over',True,white)
    gamerect = gamesurf.get_rect()
    overrect = oversurf.get_rect()
    gamerect.midtop = (width/2, 10)
    overrect.midtop = (width/2, gamerect.height+10+25)

    surface.blit(gamesurf,gamerect)
    surface.blit(oversurf,overrect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key pressed in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
def drawScore(score):
    scoresurf = basicfont.render('Score: %s' % score, True, white)
    scorerect = scoresurf.get_rect()
    scorerect.topleft = (width-120,10)
    surface.blit(scoresurf,scorerect)

def drawWorm(wormcoords):
    for coord in wormcoords:
        x = coord['x'] * cellsize
        y = coord['y'] * cellsize
        wormsegmentrect = pygame.Rect(x,y,cellsize,cellsize)
        pygame.draw.rect(surface,darkgreen,wormsegmentrect)
        worminnersegmentrect = pygame.Rect(x+4,y+4,cellsize-8,cellsize-8)
        pygame.draw.rect(surface,green,worminnersegmentrect)
def drawApple(coord):
    x = coord['x'] * cellsize
    y = coord['y'] * cellsize
    applerect = pygame.Rect(x,y,cellsize,cellsize)
    pygame.draw.rect(surface,red,applerect)
def drawGrid():
    for x in range(0,width,cellsize): # draw verticals
        pygame.draw.line(surface,darkgray,(x,0),(x,height))
    for y in range(0,height,cellsize): # draw verticals
        pygame.draw.line(surface,darkgray,(0,y),(width,y))

if __name__ == '__main__':
    main()
    




