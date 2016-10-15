from Component import *
fps = 35

def main():
    global fpsclock, displaysurf, basicfont, bigfont
    pygame.init()
    fpsclock = pygame.time.Clock()
    displaysurf = pygame.display.set_mode( (width,height))
    basicfont = pygame.font.Font('freesansbold.ttf',18)
    bigfont = pygame.font.Font('freesansbold.ttf',100)
    pygame.display.set_caption('Tetromino')
    #showTextScreen('Tetromino')
    while True:
        if random.randint(0,1) == 0:
            pygame.mixer.music.load('tetrisb.mid')
        else:
            pygame.mixer.music.load('tetrisc.mid')
        pygame.mixer.music.play(-1,0.0)
        runGame()
        pygame.mixer.music.stop()
        showTextScreen('Game Over')

def runGame():
    import copy
    mb = Board()
    #mb.generateNewPiece()
    move = None 
    lastfalltime = time.time()
    fallfreq = 30 * (1.0/fps)
    while True:
        checkForQuit()
        if not mb.isValidPosition(mb.fallingpiece,None):
            print mb.fallingpiece.boardpos.x,mbfallingpiece.boardpos.y
            print 'Game Over'
            return
        for e in pygame.event.get():
            if e.type == KEYDOWN:
                if e.key == K_LEFT and mb.isValidPosition(mb.fallingpiece,left):
                    mb.movePiece(left)
                elif e.key == K_RIGHT and mb.isValidPosition(mb.fallingpiece,right):
                    mb.movePiece(right)
                elif e.key == K_DOWN and mb.isValidPosition(mb.fallingpiece,down):
                    mb.movePiece(down)
                elif e.key == K_UP and mb.isValidPosition(mb.fallingpiece,up):
                    print 'rotating..'
                    mb.fallingpiece.rotate()
                elif e.key == K_SPACE:
                    while True:
                        if not mb.isValidPosition(mb.fallingpiece,down):
                            break
                        mb.movePiece(down)
            # move the piece fall faster with the down key
            # add code here ...
            if e.type == KEYUP:
                move = None
        # drawing everything on the screen
        if time.time() - lastfalltime > fallfreq:
            if mb.isValidPosition(mb.fallingpiece,down):
                mb.movePiece(down)
            else: # landed
                mb.addToBoard(mb.fallingpiece)
                numremovedlines = mb.removeCompleteLines()
                print numremovedlines
                mb.generateNextPieces()
            lastfalltime = time.time()
                #mb.fallingpiece = None

        displaysurf.fill(bgcolor)
        mb.draw(displaysurf)
        pygame.display.update()
        #fpsclock.tick(fps)
        fpsclock.tick(15)

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

if __name__ == '__main__':
    main()


