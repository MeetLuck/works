from Component2 import *

def main():
    startScreen() # show the title screen until the user presses a key
    levels = readLevelsFile('starPusherLevels.txt')
    currentlevelindex = 0
    # the main game loop. this loop runs a singlelevel, when the user finshes that level,
    # the next/previous level is loaded
    while True:
        # run the level to actually start playing the game
        result = runLevel(levels,currentlevelindex)
        if result in ('solved','next'): # goto the next level
            currentlevelindex += 1
            if currentlevelindex >= len(levels): # there are no more levels, go back to the first one
                currentlevelindex = 0
        elif result == 'back': # goto the previous level
            currentlevelindex -= 1
            if currentlevelindex < 0: # there are no previous levels, go to the last one
                currentlevelindex = len(levels) -1
        elif result == 'reset': # do nothing. loop recalls runLevel() to reset the level
            pass 

def runLevel(levels,levelNum):
    global currentimage
    levelobj = levels[levelNum]
    mapobj = decorateMap(levelobj['mapobj'], levelobj['startstate']['player'])
    gamestateobj = copy.deepcopy(levelobj['startstate'])
    mapneedsredraw = True # set to True to call drawMap()
    levelsurf = basicfont.render('Level %s of %s' % (levelNum + 1, len(levels)), 1, textcolor)
    levelrect = levelsurf.get_rect()
    levelrect.bottomleft = 20, winheight-35
    mapwidth = len(mapobj) * tilewidth
    mapheight = (len(mapobj[0])-1)*(tileheight-tilefloorheight)  + tileheight

    levelIsComplete = False
    # track how much the camera has moved
    cameraoffsetX,cameraoffsetY = 0,0

    while True:
        # reset the variables
        playermoveto = None
        keypressed = False
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                keypressed = True
                if event.key == K_LEFT:         playermoveto = left
                elif event.key == K_RIGHT:      playermoveto = right
                elif event.key == K_UP:         playermoveto = up
                elif event.key == K_DOWN:       playermoveto = down
                elif event.key == K_n:          return 'next'
                elif event.key == K_b:          return 'back'
                elif event.key == K_ESCAPE:     terminate()
                elif event.key == K_BACKSPACE:  return 'reset' # reset level
                elif event.key == K_p:
                    # change the player image to the next one
                    currentimage += 1
                    if currentimage > len(playerimages):
                        # after the last player image, use the first one
                        currentimage = 0
                    mapneedsredraw = True
            elif event.type == KEYUP:
                pass
        if playermoveto != None: # and not levelIsComplete:
            # if player pushed a key to move, make the move
            # if possible and push any star that are pushable
            moved = makeMove(mapobj,gamestateobj,playermoveto)
            if moved:
                # increment the step counter
                gamestateobj['stepcounter'] += 1
                mapneedsredraw = True
            if isLevelFinished(levelobj,gamestateobj):
                # level is solved, we should show the solved image
                print 'level is completed', levelIsComplete
                levelIsComplete = True
                keypressed = False

        displaysurf.fill(bgcolor)

        if mapneedsredraw:
            mapsurf = drawMap(mapobj,gamestateobj,levelobj['goals'])
            mapneedsredraw = False

        # adjust mapsurf's rect object based on the camera offset
        mapsurfrect = mapsurf.get_rect()
        mapsurfrect.center = halfwinwidth+cameraoffsetX, halfwinheight+cameraoffsetY
        displaysurf.blit(mapsurf,mapsurfrect)
        displaysurf.blit(levelsurf,levelrect)
        stepsurf = basicfont.render('Steps: %s' % gamestateobj['stepcounter'],1,textcolor)
        steprect = stepsurf.get_rect()
        steprect.bottomleft = 20,winheight-10
        displaysurf.blit(stepsurf,steprect)

        if levelIsComplete:
            solvedrect = images.solved.get_rect()
            solvedrect.center = wincenter
            displaysurf.blit(images.solved,solvedrect)
            print 'runLevel : level is completed'
            if keypressed:
                return 'solved'
        pygame.display.update()
        fpsclock.tick()

if __name__ == '__main__':
    main()



    












