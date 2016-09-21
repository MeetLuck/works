from Component import *

def main():
    global fpsclock,basicfont
    pygame.init()
    surface = pygame.display.set_mode((width,height))
    pygame.display.set_caption('Wormy')
    fpsclock = pygame.time.Clock()
    basicfont = pygame.font.Font('freesansbold.ttf',18)

    while True:
        showStartScreen(surface)
        runGame(surface)
        showGameOverScreen(surface)

def showStartScreen(surface):
    pass
def runGame(surface):
    worm = Worm()
    move = right
    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                terminate()
            elif e.type == KEYDOWN:
                if   e.key in (K_LEFT, K_a):    move = left
                elif e.key in (K_RIGHT, K_d):   move = right
                elif e.key in (K_UP,K_w):       move = up
                elif e.key in (K_DOWN,K_s):     move = down
                elif e.key == K_ESCAPE:         terminate()
        surface.fill(bgcolor)
        drawGrid(surface)
        if worm.isDied(): return
        worm.makeMove(move)
        worm.checkForCollision()
        worm.draw(surface)
        pygame.display.update()
        fpsclock.tick(fps)

def showGameOverScreen(surface):
    print 'GameOver'
    gameoverfont = pygame.font.Font('freesansbold.ttf',150)
    gamesurf = gameoverfont.render('Game',True,white)
    oversurf = gameoverfont.render('Over',True,white)
    gamerect = gamesurf.get_rect()
    overrect = oversurf.get_rect()
    gamerect.midtop = (width/2, 10)
    overrect.midtop = (width/2, gamerect.height+10+25)

    surface.blit(gamesurf,gamerect)
    surface.blit(oversurf,overrect)
    drawPressKeyMsg(surface,basicfont)
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()
    while True:
        if checkForKeyPress():
            pygame.event.get()
            return

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
    gridcolor = (20,20,20)
    for x in range(0,width,cellsize): # draw verticals
        pygame.draw.line(surface,gridcolor,(x,0),(x,height))
    for y in range(0,height,cellsize): # draw verticals
        pygame.draw.line(surface,gridcolor,(0,y),(width,y))

if __name__ == '__main__':
    main()
