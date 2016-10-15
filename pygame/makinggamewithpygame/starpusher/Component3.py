from constants import *

def getValue(lst,x,y):     return lst[y][x]
def setValue(lst,x,y,val): lst[y][x] = val
def rotate(lst):
    lst.insert(0,lst.pop())

class Level:
    playerimages = [images.princess,images.boy,images.catgirl,images.horngirl,images.pinkgirl ]
    def __init__(self,start,stars,mapobj,goals):
        self.player,self.stars,self.goals = start, stars, goals
        self.rawmap = mapobj
        self.width, self.height = len(self.rawmap[0]), len(self.rawmap)
        self.stepcounter = 0
        self.startgamestate = self.player,self.stars
        self.lastgamestate = []
        self.decorateMap()
    def getValue(self,x,y):
        return getValue(self.decomap,x,y) #return self.rawmap[y][x]
    def setValue(self,x,y,val):
        self.decomap[y][x] = val
    def changePlayer(self):
        rotate(self.playerimages)
    def saveLastGameState(self):#,player,stars):
        self.lastgamestate.append([self.player[:],self.stars[:]])
    def restoreLastGameState(self):
        if not self.lastgamestate : return
        self.player,self.stars = self.lastgamestate.pop()#[:]
    def restoreStartGameState(self):
        self.player,self.stars = copy.deepcopy(self.startgamestate)
        self.stepcounter = 0
    def isLevelFinished(self):
        ''' return True if all the goals have stars in them '''
        for goal in self.goals:
            if goal not in self.stars: # found a space with a goal but no star on it
                return False
        return True
    def isWall(self,x,y):
        ''' returns True if the (x,y) position on the map is a wall, otherwise return False '''
        if x< 0 or x >= self.width or y<0 or y>=self.height:
            return False
        elif self.getValue(x,y) in ('#','x'):
            return True
        return False

    def isBlocked(self,x,y):
        ''' returns True if (x,y) position on the map is blocked by a wall or start,
            otherwise return False. '''
        if self.isWall(x,y):
            return True
        elif x<0 or x>=self.width or y<0 or y>=self.height:
            return True  # x,y is not actually on the map
        elif (x, y) in self.stars:
            return True # a star is blocking
        return False

    def makeMove(self,playermoveto):
        ''' given a map and game state object, see if it is possible for the player to make the given move.
            if it is, then change the player's position(and the position of any pushed start).
            if not, do nothing
            returns True if the player moved, otherwise False. '''
        # save last gamestate
        self.saveLastGameState() #self.player,self.stars)
        # make sure the player can move in the direction they want
        playerx,playery = self.player #gamestateobj['player']
        # the code for handling each of the directions
        if playermoveto   == up:        xoffset,yoffset = 0, -1
        elif playermoveto == down:      xoffset,yoffset = 0, +1
        elif playermoveto == left:      xoffset,yoffset = -1,0
        elif playermoveto == right:     xoffset,yoffset = +1,0

        print 'before',playerx,playery,repr(self.getValue(playerx,playery))
        # update player position
        playerx += xoffset
        playery += yoffset
        print 'after',playerx,playery,repr(self.getValue(playerx,playery))
        
        # see if the  player can move in that direction
        if self.isWall(playerx,playery): #playerx+xoffset,playery+yoffset):
            return False
        if (playerx,playery) in self.stars:
            # there is a star in the way, see if the player can push it
            if self.isBlocked(playerx+xoffset,playery+yoffset):
                return False
            # move the star
            ind = self.stars.index( (playerx,playery) ) # get stars position
            self.stars[ind] = self.stars[ind][0] + xoffset, self.stars[ind][1]+yoffset
        # move the player upwards
        self.player = playerx,playery
        return True
    def printMap(self):
        for row in self.rawmap:
            for char in row:
                print char,
            print
    def decorateMap(self):
        ''' makes a copy of the given map object and modifies it
            here is what is done to it.
             * walls that are corners are turned into corner pieces.
             * the outside/inside floor tile distinction is made
             * tree/rock decorations are randomly added to the outside tiles
            returns the decorated map object '''

        startx,starty = self.player #startxy
        self.decomap = copy.deepcopy(self.rawmap)

        for y,row in enumerate(self.decomap): # remove the non-wall characters form the map data
            for x,char in enumerate(row):
                if char in ('$','.','@','+','*'):
                    self.setValue(x,y,val=' ') #mapcopy[y][x] = ' '

        # flood fill to determine inside/outside floor tiles
        floodFill(self.decomap, startx,starty,' ', 'o')

        # convert the adjoined walls into corner tiles
        #
        #      #          #        x #       # x
        #      x #      # x        #           #
        #
        for y,row in enumerate(self.decomap):
            for x,char in enumerate(row):
                if self.getValue(x,y) == '#':
                    if self.isWall(x,y-1) and self.isWall(x+1,y) or \
                       self.isWall(x+1,y) and self.isWall(x,y+1) or \
                       self.isWall(x,y+1) and self.isWall(x-1,y) or \
                       self.isWall(x-1,y) and self.isWall(x,y-1) :
                        self.setValue(x,y,val='x') #mapcopy[x][y] = 'x'
                elif self.getValue(x,y) == ' ' and random.randint(0,99) < outside_decoration_pct:
                    val = random.choice( list(outsidedecomapping.keys()) )
                    self.setValue(x,y,val)

    def drawMap(self):
        ''' draws the map to a surface object, including the player and stars.
            this does not call pygame.display.update(), nor does it draw the Level and Steps text '''
        mapsurfwidth = self.width * tilewidth
        mapsurfheight = (self.height-1)*tilefloorheight + tileheight
        mapsurf = pygame.Surface( (mapsurfwidth,mapsurfheight))
        mapsurf.fill(bgcolor)

        for y,row in enumerate(self.decomap):
            for x,val in enumerate(row): # val = col
                spacerect = pygame.Rect( (x*tilewidth,y*tilefloorheight,tilewidth,tileheight) )
                char = self.getValue(x,y)
                # first draw the base ground/wall tile
                if char in tilemapping:
                    basetile = tilemapping[char]
                elif char in outsidedecomapping:
                    basetile = tilemapping[' ']
                #else:
                #   basetile = tilemapping[' ']
                mapsurf.blit(basetile, spacerect)

                # draw any tree/rock decorations that are on this tile
                if char in outsidedecomapping:
                    mapsurf.blit(outsidedecomapping[char],spacerect)
                elif (x,y) in self.stars:
                    if (x,y) in self.goals:
                        # a goal and star are on this space, draw goal first
                        mapsurf.blit(images.coveredgoal,spacerect)
                    # then draw the star sprite
                    mapsurf.blit(images.star,spacerect)
                elif (x,y) in self.goals: 
                    # draw a goal without a star on it
                    mapsurf.blit(images.uncoveredgoal,spacerect)
                # last draw the player on the board
                if (x,y) == self.player:
                    # note currentimage referes to a key in 'playerimages' which 
                    # has the specific player image 
                    mapsurf.blit(self.playerimages[0],spacerect)
        for x in range(self.width):
            for y in range(self.height):
                drawrectangle(mapsurf,pygame.Color('gray'),x*tilewidth,y*tilewidth,tilewidth,tilewidth)
        return mapsurf


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
    for linenum,line in enumerate(content[:390]): #range(len(content)):
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
            level = []
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
            start = startx,starty
            level = Level(start,stars,mapobj,goals)
            levels.append(level)
            # reset the variables for reading the next map
            singlelevel = []
            mapobj = []
            levelNum += 1
    return levels

def floodFill(mapobj,x,y,oldcharacter,newcharacter):
    ''' changes any values matching old character on the map object to new character at the (x,y) position,
        and does the same for the positions to the left,right,down and up of (x,y), recursively. '''
    # in this game, the flood fill algoridthm create the inside/outside floor distinction.
    # this is a recursive function
    if getValue(mapobj,x,y) == oldcharacter: setValue(mapobj,x,y, val= newcharacter)
    if x < len(mapobj[0])-1 and getValue(mapobj,x+1,y)== oldcharacter:
        floodFill(mapobj,x+1,y,oldcharacter, newcharacter) # call right

    if x > 0  and getValue(mapobj,x-1,y) == oldcharacter:
        floodFill(mapobj,x-1,y,oldcharacter, newcharacter) # call left

    if y < len(mapobj)-1 and getValue(mapobj,x,y+1) == oldcharacter:
        floodFill(mapobj,x,y+1,oldcharacter, newcharacter) # call down

    if y > 0  and getValue(mapobj,x,y-1) == oldcharacter:
        floodFill(mapobj,x,y-1,oldcharacter, newcharacter) # call up

def drawrectangle(surface,color,x,y,width,height):  
    pointlist = [ (x,y),(x+width,y),(x+width,y+height),(x,y+height) ]
    pygame.draw.lines(surface,color,True,pointlist,1)


def terminate():
    pygame.quit(); sys.exit()



#def isBlocked(mapobj,gamestateobj,x,y):


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
        startstate = level.startgamestate
        width = level.width
        height = level.height
        mapobj = level.rawmap
        print startstate
        print width,height
        for row in mapobj:
            print ''.join(row)
        print 
