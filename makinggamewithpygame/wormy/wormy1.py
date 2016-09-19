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

if __name__ == '__main__':
    main()
