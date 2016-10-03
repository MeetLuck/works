from Partsv1 import *

def main():
    levels = readLevelsFile('..\\starPusherLevels.txt')
    os.system('cls')
    currentlevel = 0
    while True:
        result = runLevel(levels,currentlevel)
        if result in ('solved','next'):
            currentlevel += 1
        elif result == 'back':
            if currentlevel == 0: continue
            currentlevel += -1
        elif result == 'reset':
            print 'BackSpace pressed'

def runLevel(levels,levelNo):
    level = levels[levelNo]
    levelIsComplete = False
    level.printMap()
    level.reset()
    while True:
        playermoveTo = None
        keypressed = False
        for event in pygame.event.get():
            if event.type == QUIT: terminate()
            elif event.type == KEYDOWN:
                keypressed = True
                if event.key == K_ESCAPE:       terminate()
                elif event.key == K_LEFT:       playermoveTo = left
                elif event.key == K_RIGHT:      playermoveTo = right
                elif event.key == K_UP:         playermoveTo = up
                elif event.key == K_DOWN:       playermoveTo = down
                elif event.key == K_n:          return 'next'
                elif event.key == K_b:          return 'back'
                elif event.key == K_BACKSPACE:  return 'reset' # reset level
                elif event.key == K_z:          level.restoreLastGameState()
                #elif event.key == K_p: # change the player image to the next one
                #   level.changePlayer()
            elif event.type == KEYUP:
                pass
        if playermoveTo != None:
            level.makeMove(playermoveTo)
            if level.isFinished():
                print 'Level Completed'
                levelIsComplete = True
                keypressed = False

        #------------ draw Level -------------------
        #level.printMap()
        displaysurf.fill(bgcolor)
        mapsurf = level.drawMap()
        maprect = mapsurf.get_rect()
        maprect.center = halfwinwidth,halfwinheight
        displaysurf.blit(mapsurf,maprect)
        # --------- draw solved screen ------------
        if levelIsComplete:
            solvedrect = images.solved.get_rect()
            solvedrect.center = wincenter
            displaysurf.blit(images.solved,solvedrect)
            if keypressed:
                return 'solved'
        pygame.display.update()
        fpsclock.tick(fps)

def terminate():
    pygame.quit(); sys.exit()


if __name__ == '__main__':
    main()
