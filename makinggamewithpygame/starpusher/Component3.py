from constants import *

class Level:
    def __init__(self,start,stars,mapobj,goals):
        self.player = start
        self.stars  = stars
        self.map    = mapobj
        self.goals  = goals
        self.width  = len(self.map[0])
        self.height = len(self.map)
        self.stepcounter = 0
        self.gamestate = {'player':self.player,
                            'stepcounter':self.stepcounter,
                            'stars': self.stars }

def getValue(lst,x,y):
    return lst[y][x]

def readLevelsFile(filename):
    assert os.path.exists(filename), 'Cannot find the level file: %s' % filename
    mapfile = open(filename,'r')
    # each level must end with a blank line
    content = mapfile.readlines() + ['\r\n']
    mapfile.close()

    levels = [] # will contain a list of level objects
    levelNum = 0
    singlelevel = [] # contains the lines for a single level's map
    mapobj = [] # the map object made from the data in singlelevel
    for linenum,line in enumerate(content[:90]): #range(len(content)):
        line = line.rstrip('\r\n')
        if ';' in line: 
            line = line[:line.find(';')]
        if line != '': # this line is part of the map, not blank line
            singlelevel.append(line)
        elif line == '' and len(singlelevel) > 0:
            # a blank line indicates the end of a level's map in the file
            # convert the text in singlelevel into a level object
            # find the longest row in the map
            maxwidth = max( map(len,singlelevel) )
            # add spaces to the ends of the shorter row.this ensures the map will be rectangular
            for index,line in enumerate(singlelevel):
                singlelevel[index] += ' '* (maxwidth - len(line) )

            # convert singlelevel to a map object
            print '\n'.join(singlelevel)
            mapobj = map(list,singlelevel)
#           for line in mapobj: print line

            # loop through the spaces in the map and find the '@','.',and '$'
            # characters for the starting game state
            startx,starty = None,None # player's starting position
            goals= [] # a list of (x,y) for each goal
            stars = [] # a list of (x,y) for each star's starting position
            for y,row in enumerate(mapobj):
                for x,col in enumerate(row):
                    val = col #getValue(mapobj,x,y) # val = col
                    if val in ('@','+'):        # '@' is player, '+' is player and goal
                        startx,starty = x,y
                    if val in ('.','+','*'):    # '.' is goal, '*' is star and goal
                        goals.append((x,y))
                    if val in ('$','*'):        # '$' is start position
                        stars.append((x,y))

            # create level object and starting game state object
            gamestateobj = {'player':(startx,starty),
                            'stepcounter':0,
                            'stars': stars }
            levelobj = {'width':maxwidth,
                        'height': len(mapobj),
                        'mapobj':mapobj,
                        'goals':goals,
                        'startstate':gamestateobj }
            start = startx,starty
            level = Level(start,stars,mapobj,goals)
            levels.append(level)
            #levels.append(levelobj)
            # reset the variables for reading the next map
            singlelevel = []
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
                basetile = tilemapping[mapobj[x][y]]
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
                    mapsurf.blit(images.coveredgoal,spacerect)
                # then draw the star sprite
                mapsurf.blit(images.star,spacerect)
            elif (x,y) in goals:
                # draw a goal without a star on it
                mapsurf.blit(images.uncoveredgoal,spacerect)
            # last draw the player on the board
            if (x,y) == gamestateobj['player']:
                # note currentimage referes to a key in 'playerimages' which 
                # has the specific player image 
                mapsurf.blit(playerimages[currentimage],spacerect)
    return mapsurf
def isLevelFinished(levelobj,gamestateobj):
    ''' return True if all the goals have stars in them '''
    print 'isLevelFinshed'
    for goal in levelobj.goals:
        if goal not in gamestateobj['stars']:
            # found a space with a goal but no star on it
            return False
    return True

def terminate():
    pygame.quit(); sys.exit()


def isWall(mapobj,x,y):
    ''' returns True if the (x,y) position on the map is a wall, otherwise return False '''
    if x< 0 or x >= len(mapobj) or y<0 or y>=len(mapobj[x]):
        return False
    elif mapobj[x][y] in ('#','x'):
        return True
    return False
def decorateMap(mapobj,startxy):
    ''' makes a copy of the given map object and modifies it
        here is what is done to it.
         * walls that are corners are turned into corner pieces.
         * the outside/inside floor tile distinction is made
         * tree/rock decorations are randomly added to the outside tiles
        returns the decorated map object '''

    startx,starty = startxy
    print startxy
    mapobjcopy = copy.deepcopy(mapobj)
    # remove the non-wall characters form the map data
    for y,row in enumerate(mapobjcopy):
        for x,col in enumerate(row):
            val = col 
            if val in ('$','.','@','+','*'):
                mapobjcopy[y][x] = ' '
#   for x in range(len(mapobjcopy)):
#       for y in range(len(mapobjcopy[0]) ):
#           if mapobjcopy[x][y] in 
#               mapobjcopy[x][y] = ' '
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
            elif mapobjcopy[x][y] == ' ' and random.randint(0,99) < outside_decoration_pct:
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

def makeMove(mapobj,gamestateobj,playermoveto):
    ''' given a map and game state object, see if it is possible for the player to make the given move.
        if it is, then change the player's position(and the position of any pushed start).
        if not, do nothing
        returns True if the player moved, otherwise False. '''
    # make sure the player can move in the direction they want
    playerx,playery = gamestateobj['player']
    stars = gamestateobj['stars']
    # the code for handling each of the directions
    if playermoveto   == up:        xoffset,yoffset = 0, -1
    elif playermoveto == down:      xoffset,yoffset = 0, +1
    elif playermoveto == left:      xoffset,yoffset = -1,0
    elif playermoveto == right:     xoffset,yoffset = +1,0

    # update player position
    playerx += xoffset
    playery += yoffset
    
    # see if the  player can move in that direction
    if isWall(mapobj,playerx,playery): #playerx+xoffset,playery+yoffset):
        return False
    if (playerx,playery) in stars:
        # there is a star in the way, see if the player can push it
        if isBlocked(mapobj,gamestateobj,playerx+xoffset,playery+yoffset):
            return False
        # move the star
        ind = stars.index( (playerx,playery) ) # get stars position
        stars[ind] = stars[ind][0] + xoffset, stars[ind][1]+yoffset
    # move the player upwards
    gamestateobj['player'] = playerx,playery
    return True

def startScreen():
    ''' display the start screen(which has the title and instructions) until key pressed
        return None '''
    titlerect = images.title.get_rect()
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
    displaysurf.blit(images.title,titlerect)
    # position and draw text
    for i in range(len(instruction)):
        instsurf = basicfont.render(instruction[i],1,textcolor)
        instrect = instsurf.get_rect()
        topcoord += 10 # 10 pixels between each line
        instrect.top = topcoord
        instrect.centerx = halfwinwidth
        topcoord += instrect.height # adjust for the height of the line
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

if __name__ == '__main__':
    os.system('cls')
    levels = readLevelsFile('starPusherLevels.txt')
    print 'Levels\n'
    for level in levels[:3]:
        startstate = level['startstate']
        width = level['width']
        height = level['height']
        mapobj = level['mapobj']
        print repr(level.keys() )
        print startstate
        print width,height
        for row in mapobj:
            print ''.join(row)
        print 
