from Component4 import *
#fps = 25

def main():
    global fpsclock, displaysurf, basicfont, bigfont
    pygame.init()
    fpsclock = pygame.time.Clock()
    displaysurf = pygame.display.set_mode( (screenwidth,screenheight))
    basicfont = pygame.font.Font('freesansbold.ttf',18)
    bigfont = pygame.font.Font('freesansbold.ttf',100)
    pygame.display.set_caption('Tetromino')
    #showTextScreen('Tetromino')
    while True:
#       if random.randint(0,1) == 0:
#           pygame.mixer.music.load('tetrisb.mid')
#       else:
#           pygame.mixer.load('mz_545_3_format0')
#           #pygame.mixer.music.load('tetrisc.mid')
        pygame.mixer.music.load('mz_545_3_format0.mid')
        pygame.mixer.music.play(-1,0.0)
        runGame()
        pygame.mixer.music.stop()
        showTextScreen('Game Over')

def runGame():
    import copy
    mb = Board()
    lastfalltime = time.time()
    displaysurf.fill(screenbgcolor)
    showStartLevel(level=1)
    starttime = time.time()
    completesound = pygame.mixer.Sound('blip2.wav')
    while True:
        checkForQuit()
        if not mb.isValidPosition(mb.fallingpiece):
            print 'Game Over'
            return
        for event in pygame.event.get(KEYDOWN): #if event.type == KEYDOWN:
            if event.key == K_LEFT and mb.isValidPosition(mb.fallingpiece, moveX = -1):
                mb.movePiece(moveX = -1)
            elif event.key == K_RIGHT and mb.isValidPosition(mb.fallingpiece, moveX = +1):
                mb.movePiece(moveX = +1)
            elif event.key == K_DOWN and mb.isValidPosition(mb.fallingpiece, moveY = +1):
                mb.movePiece(moveY = +1)
            elif event.key == K_UP and mb.isValidPosition(mb.fallingpiece,rotate=True): # rotate if moveY=-1
                print 'rotating..'
                mb.fallingpiece.rotate()
            elif event.key == K_SPACE:
                while True:
                    if not mb.isValidPosition(mb.fallingpiece, moveY = +1):
                        break
                    mb.movePiece(moveY = +1)
            # add code here ...
        for event in pygame.event.get(KEYUP): 
            pass

        # let the piece fall naturally
        if time.time() - lastfalltime > mb.fallfreq:
            if mb.isValidPosition(mb.fallingpiece, moveY = +1):
                mb.movePiece(moveY = +1)
            else: # landed
                mb.addToBoard(mb.fallingpiece)
                mb.removeCompleteLines()
                mb.generateNextPieces()
            lastfalltime = time.time()

        # drawing everything on the screen
        displaysurf.fill(screenbgcolor)
        mb.draw(displaysurf,starttime)
        pygame.display.update()
        fpsclock.tick(fps)

        # start Next Level
        if mb.completeLevel():
            pygame.time.delay(1000)
            level = mb.level + 1
            showStartLevel(level)
            mb = Board(level)


def terminate():
    pygame.quit(); sys.exit()

def checkForQuit():
    for e in pygame.event.get(QUIT): # get all the QUIT events
        terminate()
    for e in pygame.event.get(KEYUP): # get all the KEYUP events
        if e.key == K_ESCAPE:
            terminate()
        pygame.event.post(e)
def showTextScreen(text):
    print text
    pygame.time.wait(5000)
def showStartLevel(level):
    # draw Level 1 : text drop shadow 
    #textcolor = 0,100,20,255 
    textcolor = getDarkColor('darkgreen',110)
    shadowcolor = getDarkColor(textcolor,70)
    textsurf,textrect = getTextObj(text='LEVEL %s' %level, fontsize=60, color=shadowcolor)
    textrect.center = screenwidth/2, screenheight/2 - 40
    displaysurf.blit(textsurf,textrect)
    # draw Level 1 : text 
    #textcolor = getDarkColor(pygame.Color(shadowcolor),140)
    r,g,b,a = shadowcolor
    br = 10
    #textcolor = r+br,g+br,+b+br,a
    textsurf,textrect = getTextObj(text='LEVEL %s' %level, fontsize=60, color=textcolor)
    textrect.center = screenwidth/2 - 3, screenheight/2 - 40 - 3
    displaysurf.blit(textsurf,textrect)
    # draw Press a key to start
    color = getDarkColor(textcolor,70) 
    textsurf,textrect = getTextObj(text='Press a key to start', fontsize=30, color=color)
    textrect.center = screenwidth/2, screenheight/2 + 40
    displaysurf.blit(textsurf,textrect)
    pygame.display.update()
    pygame.time.wait(500)
    while True:
        if checkForKeyPress():
            return

def checkForKeyPress():
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None

if __name__ == '__main__':
    main()


