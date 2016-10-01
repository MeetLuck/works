from constants import *
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
            # add spaces to the ends of the shorter row.
            # this ensures the map will be rectangular
            for index,line in enumerate(singlelevel):
                singlelevel[index] += ' '* (maxwidth - len(line) )

            # convert singlelevel to a map object
            print '\n'.join(singlelevel)
            mapobj = map(list,singlelevel)
            # check row,column length
            if maxwidth > len(mapobj):
                print maxwidth,len(mapobj)
                for i in range(maxwidth - len(mapobj)):
                    mapobj.append([])

            for line in mapobj:
                print line
            # loop through the spaces in the map and find the @,.,and $
            # characters for the starting game state
            startx,starty = None,None # player's starting position
            goals= [] # a list of (x,y) for each goal
            stars = [] # a list of (x,y) for each star's starting position
            for x in range(maxwidth):
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
#           assert startx!=None and starty!=None, 'Level %s(around line %s) in %s is missing a "@" or "+"\
#                   to mark the start point.' %(levelNum+1,linenum,filename)
#           assert len(goals) > 0, 'Level %s(around line %s) in %s must have at least one goal.' \
#                   %(levelNum+1,linenum,filename)
#           assert len(stars) >= len(goals),'Level %s(around line %s) in %s is impossible to solve. \
#                   it has %s goals but only %s starts.'\
#                   %(levelNum+1,linenum,filename,len(goals),len(stars))
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

#def drawMap(mapobj,gamestateobj,goals):
    ''' draws the map to a surface object, including the player and stars.
        this does not call pygame.display.update(), nor does it draw the Level and Steps text '''
    # mapsurf will be the single surface object that the tiles are drawn on,
    # so that it is easy to position the entire map on the displaysurf.
    # first, the width and height must be calculated
'''
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
'''
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
