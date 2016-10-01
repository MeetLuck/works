import pygame, sys, random, os, copy
from pygame.locals import *
fps = 30
winwidth,winheight = 800,600
wincenter = halfwinwidth,halfwinheight = winwidth/2,winheight/2
# total width and height of each tile in pixels
tilewidth = 50
tileheight = 85
tilefloorheight = 45

camspeed = 5 # how many pixels per frame the camera moves
# the percentage of outdoor titles that have additional decoration
# on them such as tree or rock
outside_decoration_pct = 20
brightblue = 0,170,255
white = 255,255,255
bgcolor = brightblue
textcolor = white

up,down,left,right = 'up','down','left','right'

def main():
    global fpsclock,displaysurf, imagedict, tilemapping,outsidedecomapping, basicfont,
           playerimages, currentimage
    pygame.init()
    fpsclock = pygame.time.Clock()
    displaysurf = pygame.display.set_mode( (winwidth,winheight))
    pygame.display.set_caption('Star Pusher')
    basicfont = pygame.font.Font('freesansbold.ttf',18)
    # a global dict value that will contain all the pygame suface objects returned by
    # pygame.image.load()
    imagesdict = {'uncovered goal':pygame.image.load('RedSelector.png'),
                  'covered goal':pygame.image.load('Selector.png'),
                  'star':pygame.image.load('Star.png'),
                  'corner':pygame.image.load('Wall Block Tall.png'),
                  'wall':pygame.image.load('Wood Block Tall.png'),
                  'inside floor':pygame.image.load('Plain Block.png'),
                  'outside floor':pygame.image.load('Grass Block.png'),
                  'title':pygame.image.load('star_title.png'),
                  'solved':pygame.image.load('star_solved.png'),
                  'princess':pygame.image.load('princess.png'),
                  'boy':pygame.image.load('boy.png'),
                  'catgirl':pygame.image.load('catgirl.png'),
                  'horngirl':pygame.image.load('horngirl.png'),
                  'pinkgirl':pygame.image.load('pinkgirl.png'),
                  'rock':pygame.image.load('Rock.png'),
                  'short tree':pygame.image.load('Tree_Short.png'),
                  'tall tree':pygame.image.load('Tree_Tall.png'),
                  'ugly tree':pygame.image.load('Tree_Ugly.png') }
    # these dict values are global, and map the character that appears in the level file
    # to the surface object it represents
    tilemapping = {'x':imagesdict['corner'],
                    '#':imagesdict['wall'],
                    'o':imagesdict['inside floor'],
                    ' ':imagesdict['outside floor'] }
    outsidedecomapping = {'1':imagesdict['rock'],
                          '2':imagesdict['short tree'],
                          '3':imagesdict['tall tree'],
                          '4':imagesdict['ugly tree'] }
    # playerimages is a list of all possible characters the player can be
    # currentimage is the index of the player's current player image
    currentimage = 0
    playerimages = [ imagesdict['princess'],imagesdict['boy'],imagesdict['catgirl'],
                     imagesdict['horngirl'],imagesdict['pinkgirl'] ]
    startScreen() # show the title screen until the user presses a key
    # read in the levles from the text file. See the readLevelsFile() for details on the format
    # of this file and how to make your own levels
    levels = readLevelsFile('starPusherLevels.txt')
    currentlevelindex = 0
    # the main game loop. this loop runs a singlelevel, when the user finshes that level,
    # the next/previous level is loaded
    while True:
        # run the level to actually start playing the game
        result = runLevel(levels,currentlevelindex)
        if result in ('solved','next'):
            # goto the next level
            currentlevelindex += 1
            if currentlevelindex >= len(levels):
                # there are no more levels, go back to the first one
                currentlevelindex = 0
        elif result == 'back':
            # goto the previous level
            currentlevelindex -= 1
            if currentlevelindex < 0:
                # there are no previous levels, go to the last one
                currentlevelindex = len(levels) -1
        elif result == 'reset':
            pass # do nothing. loop recalls runLevel() to reset the level
def runLevel(levels,levelNum):
    global currentimage
    levelobj = levels[levelnum]
    mapobj = decorateMap(levelobj['mapobj'], levelobj['startstate']['player'])
    gamestateobj = copy.deecopy(levelobj['startstate'])
    mapneedredraw = True # set to True to call drawMap()
    levesurf = basicfont.render('Level %s of %s' %(levelobj['levelNum']+1,totalNumOfLevels),1,textcolor)
    levelrect = levelsurf.get_rect()
    levelrect.bottomleft = 20, winheight-35
    mapwidth = len(mapobj) * tilewidth
    mapheight = (len(mapobj[0])-1)*(tileheight-tilefloorheight)  + tileheight
    max_cam_x_pan = abs(halfwinheight - int(mapheight/2) ) + tilewidth
    max_cam_y_pan = abs(halfwinwidth - int(mapwidth/2) ) + tileheight

    leveliscomplete = False
    # track how much the camera has moved
    cameraoffsetX,cameraoffsetY = 0,0
    # track if the keys to move the camera are being held down
    cameraUp,cameraDown,cameraLeft,cameraRight = False,False,False,False

    while True:
        # reset the variables
        playermoveto = None
        keypressed = False
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                keypressed = True
                if event.key == K_LEFT:
                    playermoveto = left
                elif event.key == K_RIGHT:
                    playermoveto = right
                elif event.key == K_UP:
                    playermoveto = up
                elif event.key == K_DOWN:
                    playermoveto = down
                # set camera move mode
                elif event.key = K_a:
                    cameraLeft = True
                elif event.key = K_d:
                    cameraRight = True
                elif event.key = K_w:
                    cameraUp = True
                elif event.key = K_s:
                    cameraDown = True

                elif event.key == K_n:
                    return 'next'
                elif event.key == K_b:
                    return 'back'
                elif event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_BACKSPACE:
                    return 'reset' # reset level
                elif event.key == K_p:
                    # change the player image to the next one
                    currentimage += 1
                    if currentimage > len(playerimages):
                        # after the last player image, use the first one
                        currentimage = 0
                    mapneedsredraw = True
            elif event.type == KEYUP:
                # unset the camera move mode
                if event.key == K_a: cameraLeft = False
                elif event.key == K_d: cameraRight = False
                elif event.key == K_w: cameraUp = False
                elif event.key == K_s: cameraDown = False
        if playmoveto != None and not leveliscomplete:
            # if player pushed a key to move, make the move
            # if possible and push any start that are pushable
            moved = makeMove(mapobj,gamestateobj,playmoveto)
            if moved:
                # increment the step counter
                gamestateobj['stepcounter'] += 1
                mapeedsredraw = True
            if isLevelFinished(levelobj,gamestateobj):
                # level is solved, we should show the solved image
                leveiscomplete = True
                keypressed = False

        displaysurf.fill(bgcolor)

        if mapeendsredraw:
            mapsurf = drawMap(mapobj,gamestateobj,levelobj['goals'])
            mapneedsredraw = False
        if cameraUp and cameraoffsetY < max_cam_x_pan:
            cameraoffsetY += cam_move_speed
        elif cameraDown and cameraoffsetY > -max_cam_x_pan:
            cameraoffsetY -= cam_move_speed
        if cameraLeft and cameraoffsetX < max_cam_y_pan:
            cameraoffsetX += cam_move_speed
        elif cameraRight and cameraoffsetX > -max_cam_y_pan:
            cameraoffsetX -= cam_move_speed

        # adjust mapsurf's rect object based on the camera offset
        mapsurfrect = mapsurf.get_rect()
        mapsurfrect.center = halfwinwidth+cameraoffsetX, halfwinheight+cameraoffsetY
        displaysurf.blit(mapsurf,mapsurfrect)
        displaysurf.blit(levelsurf,levelrect)
        stepsurf = basicfont.render('Steps: %s' % gamestateobj['stepcounter'],1,textcolor)
        steprect = stepsurf.get_rect()
        steprect.bottomleft = 20,winheight-10
        displaysurf.blit(stepsurf,steprect)

        if leveliscomplete:
            solvedrect = imagesdict['solved'].get_rect()
            solvedrect.center = wincenter
            displaysurf.blit(imagesdict['solved'],solvedrect)
            if keypressed:
                return 'solved'
        pygame.display.update()
        fpsclock.tick()

#----------------- helpers ---------------------------------------------
def decorateMap(mapobj,startx):
    ''' makes a copy of the given map object and modifies it
        here is what is done to it.
         * walls that are corners are turned into corner pieces.
         * the outside/inside floor tile distinction is made
         * tree/rock decorations are randomly added to the outside tiles
        returns the decorated map object '''

    startx,starty = startxy
    mapobjcopy = copy.deepcopy(mapobj)
    # remove the non-wall characters form the map data
    for x in range(len(mapobjcopy)):
        for y in range(len(mapobjcopy[0]) ):
            if mapobjcopy[x][y] in ('$','.','@','+','*'):
                mapobjcopy[x][y] = ' '
    # flood fill to determine inside/outside floor tiles
    floodFill(mapobjcopy, startx,starty,' ', 'o')
    # convert the adjoined walls into corner tiles
    for x in range(len(mapobjcopy)):
        for y in range(len(mapobjcopy[0]) ):
            if mapobjcopy[x][y] == '#':
                if isWall(mapobjcopy,x,y-1) and isWall(mapobjcopy,x+1,y) or \
                   isWall(mapobjcopy,x+1,y) and isWall(mapobjcopy,x,y+1) or \
                   isWall(mapobjcopy,x,y+1) and isWall(mapobjcopy,x-1,y) or \
                   isWall(mapobjcopy,x-1,y) and isWall(mapobjcopy,x,y-1) :
                    mapobjcopy[x][y] = 'x'
            elif mapcopy[x][y] == ' ' and random.randint(0,99) < outside_decoration_pct:
                mapobjcopy[x][y] = random.choice( list(outsidedecomapping.keys()) )
    return mapobjcopy

def isBlocked(mapobj,gamestateobj,x,y):
    ''' returns True if (x,y) position on the map is blocked by a wall or start,
        otherwise return False. '''
    if isWall(mapobj,x,y):
        return True
    elif x<0 or x>=len(mapobj) or y<0 or y>=len(mapobj[x]):
        return True # a star is blocking
    return False

def makeMove(mapobj,gamestateobj,playmoveto):
    ''' given a map and game state object, see if it is possible for the player to make the given move.
        if it is, then change the player's position(and the position of any pushed start).
        if not, do nothing
        returns True if the player moved, otherwise False. '''
    # make sure the player can move in the direction they want
    playerx,playery = gamestateobj['player']
    stars = gamestateobj['starts']
    # the code for handling each of the directions
    if playmoveto == up: xoffset,yoffset = 0, -1
    elif playmoveto == down: xoffset,yoffset = 0, +1
    elif playmoveto == left: xoffset,yoffset = -1,0
    elif playmoveto == right: xoffset,yoffset = +1,0
    
    # see if the  player can move in that direction
    if isWall(mapobj,playerx+xoffset,playery+yoffset):
        return False
    else:
        if (playerx+xoffset,playery+yoffset) in stars:
            # there is a star in the way, see if the player can push it
            if not isBlocked(mapobj,gamestaeobj,playx+2*xoffset,playery+yoffset*2):
                # move the star
                ind = stars.index( (playerx+xoffset,playery+yoffset) )
                stars[ind] = stars[ind][0] + xoffset, stars[ind][1]+yoffset
            else:
                return False
        # move the player upwards
        gamestateobj['player'] = playerx+xoffset,playery+yoffset
        return True

def startScreen():
    ''' display the start screen(which has the title and instructions) until key pressed
        return None '''
    titlerect = imagesdict['title'].get_rect()
    topcoord = 50
    titlerect.top = topcoord
    titlerect.centerx = halfwinwidth
    topcoord += titlerect.height
    # we will use a list with each line in it.
    instruction = ['Push the stars over the marks.',
                   'Arrow kyes to move, WASD for camera control,P to change character.',
                   'Backspace to reset the level, Esc to quit.',
                   'N for next level, B to go back to the previous level.' ]
    # start with drawing a blank color to the entire window
    displaysurf.fill(bgcolor)
    # draw the title image to the window
    displaysurf.blit(imagesdict['title'],titlerect)
    # position and draw text
    for i in range(len(instruction)):
        instsurf = basicfont.render(instruction[i],1,textcolor)
        instrect = instsurf.get_rect()
        topcoord += 10 # 10 pixels between each line
        instrect.top = topcoord
        instrect.centerx = halfwinwidth
        topcoord += instrec.height # adjust for the height of the line
        displaysurf.blit(instsurf,instrect)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT: terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return # user has pressed a key, so return
        # display the contents to the actual screen
        pygame.display.update()
        fpsclock.tick()

def readLevelsFile(filename):
    assert os.path.exists(filename), 'Cannot find the level file: %s' % filename
    mapfile = open(filename,'r')
    # each level must end with a blank line
    content = mapfile.readlines() + ['\r\n']
    mapfile.close()

    levels = [] # will contain a list of level objects
    levelNum = 0
    maptextlines = [] # contains the lines for a single level's map
    mapobj = [] # the map object made from the data in maptextlines
    for linenum in range(len(content)):
        # process each line that was in the level file
        line = content[linenum].rstrip('\r\n')
        if ';' in line:
            # ignore the ; line, they're comments in the level file
            line = line[:line.find(';')]
        if line != '':
            # this line is part of the map
            maptextlines.append(line)
        elif line == '' and len(maptextlines) > 0:
            # a blank line indicates the end of a level's map in the file
            # convert the text in maptextlines into a level object
            # find the longest row in the map
            maxwidth = -1
            for i in range(len(maptextlines)):
                if len(maptextlines[i]) > maxwidth:
                    maxwidth = len(maptextlines[i])
            # add spaces to the ends of the shorter row.
            # this ensures the map will be rectangular
            for i in range(len(maptextlines)):
                maptextlines[i] += ' ' * (maxwidth - len(maptextlines[i]))
            # convert maptextlines to a map object
            for x in range(len(maptextlines[0])):
                mapobj.append([])
            for y in range(len(maptextlines)):
                for x in range(maxwidth):
                    mapobj[x].append(maptextlines[y][x])
            # loop through the spaces in the map and find the @,.,and $
            # characters for the starting game state
            startx,starty = None,None # player's starting position
            goals= [] # a list of (x,y) for each goal
            stars = [] # a list of (x,y) for each star's starting position
            for x in range( len(mapobj[x])):
                for y in range( len(mapobj[x])):
                    if mapobj[x][y] in ('@','+'):
                        # '@' is player, '+' is player & goal
                        startx,starty = x,y
                    if mapobj[x][y] in ('.','+','*'):
                        # '.' is goal, '*' is star and goal
                        goals.append((x,y))
                    if mapobj[x][y] in ('$','*'):
                        # '$' is star
                        stars.append((x,y))
            # basic level design sanity checks:
            assert startx!=None and starty!=None, 'Level %s(around line %s) in %s is missing a "@" or "+"\
                    to mark the start point.' %(levelNum+1,linenum,filename)
            assert len(goals) > 0, 'Level %s(around line %s) in %s must have at least one goal.' \
                    %(levelNum+1,linenum,filename)
            assert len(stars) >= len(goals),'Level %s(around line %s) in %s is impossible to solve. \
                    it has %s goals but only %s starts.'\
                    %(levelNum+1,linenum,filename,len(goals),len(stars))
            # create level object and starting game state object
            gamestateobj = {'player':(startx,starty),
                            'stepcounter':0,
                            'stars': stars }
            levelobj = {'width':maxwidth,
                        'height': len(mapobj),
                        'mapobj':mapobj,
                        'goals':goals,
                        'startstate':gamestateobj }
            levels.append(levelobj)
            # reset the variables for reading the next map
            maptextlines = []
            mapobj = []
            gamestateobj = {}
            levelNum += 1
    return levels

def floodFill(mapobj,x,y,oldcharacter,newcharacter):
    ''' changes any values matching old character on the map object to new character at the (x,y) position,
        and does the same for the positions to the left,right,down and up of (x,y), recursively. '''
    # in this game, the flood fill algoridthm create the inside/outside floor distinction.
    # this is a recursive function
    if mapobj[x][y] == oldcharacter: mapobj[x][y] = newcharacter
    if x < len(mapobj)-1 and mapobj[x+1][y] == oldcharacter:
        floodFill(mapobj,x+1,y,oldcharacter, newcharacter) # call right
    if x > 0  and mapobj[x-1][y] == oldcharacter:
        floodFill(mapobj,x-1,y,oldcharacter, newcharacter) # call left
    if y < len(mapobj[x])-1 and mapobj[x][y+1] == oldcharacter:
        floodFill(mapobj,x,y+1,oldcharacter, newcharacter) # call down
    if y > 0  and mapobj[x][y-1] == oldcharacter:
        floodFill(mapobj,x,y-1,oldcharacter, newcharacter) # call up

def drawMap(mapobj,gamestateobj,goals):
    ''' draws the map to a surface object, including the player and stars.
        this does not call pygame.display.update(), nor does it draw the Level and Steps text '''
    # mapsurf will be the single surface object that the tiles are drawn on,
    # so that it is easy to position the entire map on the displaysurf.
    # first, the width and height must be calculated
    mapsurfwidth = len(mapobj) * tilewidth
    mapsurfheight = ( len(mapobj[0]) -1) * (tileheight - tilefloorheight) + tileheight
    mapsurf = pygame.Surface( (mapsurfwidth,mapsurfheight))
    mapsurf.fill(bgcolor)

    # draw the tile sprites onto this surface
    for x in range(len(mapobj)):
        for y in range(len(mapobj[x])):
            spacerect = pygame.Rect( (x*tilewidth,y*(tileheight-tilefloorheight),tilewidth,tileheight) )
            if mapobj[x][y] in tilemapping:
                basetile = tilemapping[mapobj[x][y])
            elif mapobj[x][y] in outsidedecomapping:
                basetile = tilemapping[' ']
            # first draw the base ground/wall tile
            mapsurf.blit(basetile, spacerect)
            if mapobj[x][y] in outsidedecomapping:
                # draw any tree/rock decorations that are on this tile
                mapsurf.blit(outsidedecomapping[mapobj[x][y]],spacerect)
            elif (x,y) in gamestateobj['stars']:
                if (x,y) in goals:
                    # a goal and star are on this space, draw goal first
                    mapsurf.blit(imagesdict['covered goal'],spacerect)
                # then draw the star sprite
                mapsurf.blit(imagesdict['star'],spacerect)
            elif (x,y) in goals:
                # draw a goal without a star on it
                mapsurf.blit(imagesdict['uncovered goal'],spacerect)
            # last draw the player on the board
            if (x,y) == gamestateobj['player']:
                # note currentimage referes to a key in 'playerimages' which 
                # has the specific player image 
                mapsurf.blit(plyaerimages[currentimage],spacerect)
    return mapsurf

def isLevelFinished(levelobj,gamestateobj):
    ''' return True if all the goals have stars in them '''
    for goal in levelobj['goals']:
        if goal not in gamestateobj['stars']:
            # found a space with a goal but no star on it
            return False
    return True
def terminate():
    pygame.quit(); sys.exit()

if __name__ == '__main__':
    main()



    












