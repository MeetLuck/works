from Component import *

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
        #showTextScreen('Game Over')

def runGame():
    mb = Board()
    #mb.generateNewPiece()
    move = None 
    while True:
        checkForQuit()
        for e in pygame.event.get():
            if e.type == KEYDOWN:
                if e.key == K_LEFT or e.key == K_a:
                    move = left
                elif e.key == K_RIGHT or e.key == K_d:
                    move = right
                elif e.key == K_DOWN or e.key == K_s:
                    move = down
            if e.type == KEYUP:
                move = down
                # drawing everything on the screen
        displaysurf.fill(bgcolor)
        m =  mb.movePiece(move)
        print m

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

if __name__ == '__main__':
    main()


