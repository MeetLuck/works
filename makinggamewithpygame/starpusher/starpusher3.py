from Component3 import *

def main():
    startScreen() # show the title screen until the user presses a key
    levels = readLevelsFile('starPusherLevels.txt')
    os.system('cls')
    currentlevelindex = 0
    while True: # this loop runs a singlelevel
        result = runLevel(levels,currentlevelindex) # run the level to actually start playing the game
        if result in ('solved','next'): # goto the next level
            currentlevelindex += 1
            if currentlevelindex >= len(levels): # there are no more levels, go back to the first one
                currentlevelindex = 0
        elif result == 'back': # goto the previous level
            currentlevelindex -= 1
            if currentlevelindex < 0: # there are no previous levels, go to the last one
                currentlevelindex = len(levels) -1
        elif result == 'reset': # do nothing. loop recalls runLevel() to reset the level
            print 'BackSpace pressed'
            #pass 

def runLevel(levels,levelNum):
    level = levels[levelNum]
    level.restoreStartGameState()
    levelsurf = basicfont.render('Level %s of %s' % (levelNum + 1, len(levels)), 1, textcolor)
    levelrect = levelsurf.get_rect()
    levelrect.bottomleft = 20, winheight-35

    levelIsComplete = False
    level.printMap()

    while True:
        # reset the variables
        playermoveto = None
        keypressed = False
        for event in pygame.event.get():
            if event.type == QUIT: terminate()
            elif event.type == KEYDOWN:
                keypressed = True
                if event.key == K_ESCAPE:       terminate()
                elif event.key == K_LEFT:       playermoveto = left
                elif event.key == K_RIGHT:      playermoveto = right
                elif event.key == K_UP:         playermoveto = up
                elif event.key == K_DOWN:       playermoveto = down
                elif event.key == K_n:          return 'next'
                elif event.key == K_b:          return 'back'
                elif event.key == K_BACKSPACE:  return 'reset' # reset level
                elif event.key == K_z:          level.restoreLastGameState()
                elif event.key == K_p: # change the player image to the next one
                    level.changePlayer()
            elif event.type == KEYUP:
                keypressed = False

        if playermoveto != None: # and not levelIsComplete:
            # if player pushed a key to move, make the move
            # if possible and push any star that are pushable
            moved = level.makeMove(playermoveto)
            if moved: # increment the step counter
                #print moved
                level.stepcounter += 1
            if level.isLevelFinished(): # level is solved, we should show the solved image
                levelIsComplete = True
                keypressed = False

        # draw level
        displaysurf.fill(bgcolor)
        mapsurf = level.drawMap()
        mapsurfrect = mapsurf.get_rect()
        mapsurfrect.center = halfwinwidth, halfwinheight
        displaysurf.blit(mapsurf,mapsurfrect)
        displaysurf.blit(levelsurf,levelrect)
        stepsurf = basicfont.render('Steps: %s' % level.stepcounter,1,textcolor)
        steprect = stepsurf.get_rect()
        steprect.bottomleft = 20,winheight-10
        displaysurf.blit(stepsurf,steprect)

        if levelIsComplete:
            solvedrect = images.solved.get_rect()
            solvedrect.center = wincenter
            displaysurf.blit(images.solved,solvedrect)
            if keypressed:
                return 'solved'
        pygame.display.update()
        fpsclock.tick()

if __name__ == '__main__':
    main()
