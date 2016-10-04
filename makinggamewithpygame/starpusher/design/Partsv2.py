from constants import *
class Level:
    def __init__(self,rawmap):
        self.rawmap = rawmap # keep original
        self.setupMap() # get goals position
        self.setupSurface()
        self.lastmaps = []
        self.laststeps= []
        self.steps = 0
    def setupSurface(self):
        surfwidth  = self.width * tilewidth      # tileheight
        #surfheight = self.height * tileheight    #(self.height-1)*tilefloorheight + tileheight
        surfheight = (self.height-1)*tilefloorheight + tileheight
        self.surface = pygame.Surface( (surfwidth,surfheight) )
    def setupMap(self):
        ''' get goals position and process star map '''
        self.starmap = copy.deepcopy(self.rawmap)
        self.goals = []
        for y,row in enumerate(self.starmap):
            for x,char in enumerate(row):
                if char not in ['+','*','.']: continue
                if char == '+':     # goal & player
                    self.starmap[y][x] = '@'
                elif char == '*':   # goal & star
                    self.starmap[y][x] = '$'
                elif char == '.':   # only goal
                    self.starmap[y][x] = ' '
                self.goals.append((x,y))
        # get starmap's width & height
        self.width = len(self.starmap[0])
        self.height = len(self.starmap)
    def reset(self):
        self.setupMap()
        self.steps = 0
    def restoreLastGameState(self):
        if not self.lastmaps : return
        self.starmap = self.lastmaps.pop() #self.printMap()
        self.steps = self.laststeps.pop()
    def printMap(self,themap=None):
        if themap == None: themap = self.starmap
        for row in themap:
            print ''.join(row)
    def getPlayer(self):
        for y,row in enumerate(self.starmap):
            for x,char in enumerate(row):
                if char != '@': continue
                return (x,y)
        return None
    def getChar(self,x,y):
        return self.starmap[y][x]
    def setChar(self,tu,val):
        x,y = tu; self.starmap[y][x] = val
    def isWall(self,x,y):  return self.getChar(x,y) == '#'
    def isStar(self,x,y):  return self.getChar(x,y) == '$'
    def isSpace(self,x,y): return self.getChar(x,y) == ' '
    def isGoal(self,x,y):  return (x,y) in self.goals
    def isFinished(self):
        for pos in self.goals:
            if self.getChar(*pos) != '$': return False
        return True
    def makeMove(self,moveTo):
        lastmap = copy.deepcopy(self.starmap)
        laststep = self.steps
        oldPlayer = playerX,playerY = self.getPlayer()
        if moveTo == left:  xoffset,yoffset = -1,0
        if moveTo == right: xoffset,yoffset = +1,0
        if moveTo == up:    xoffset,yoffset = 0,-1
        if moveTo == down:  xoffset,yoffset = 0,+1
        # move player if possible
        playerX += xoffset
        playerY += yoffset
        newPlayer = (playerX,playerY)
        if self.isWall(*newPlayer): return False
        if self.isStar(*newPlayer):
            newStar = playerX+xoffset,playerY+yoffset
            if self.isWall(*newStar) or self.isStar(*newStar):
                return False
            #assert self.isSpace(*newStar), '%s position occupied ' %newStar
            self.setChar(newStar,'$')
            self.setChar(newPlayer,'@')
            self.setChar(oldPlayer,' ')
        elif self.isSpace(*newPlayer):
            self.setChar(newPlayer,'@')
            self.setChar(oldPlayer,' ')
        # it is valid move, save last star map
        self.steps += 1
        self.laststeps.append(laststep)
        self.lastmaps.append(lastmap) 
        return True
    def decorateMap(self):
        # walls that are cornders turned into corner walls => 'x'
        # inside/outside dictiontion made by floodfill function  => 'o': inside, ' ': outside
        # tree/rock decorations are randomly added to the outside tiles

        # copy starmap
        self.decomap = copy.deepcopy(self.starmap)

        # flood fill to determine inside/outside floor tiles
        floodFill(self.decomap, startx,starty,' ', 'o')

        # convert the adjoined walls into corner tiles
        #      #          #        x #       # x
        #      x #      # x        #           #


    def drawrectangle(self,surface,color,x,y,width=tilewidth,height=tileheight):  
        x,y = x*tilewidth,y*tileheight
        pygame.draw.rect(surface,color,(x,y,width,height),1)
    def drawWall(self,surface,x,y):
        surf = images.wall
        surface.blit(surf,self.spacerect)
    def drawSpace(self,surface,x,y):
        surf = images.insidefloor
        surface.blit(surf,self.spacerect)
    def drawStar(self,surface,x,y):
        self.drawSpace(surface,x,y)
        surf = images.star
        surface.blit(surf,self.spacerect)
    def drawGoal(self,surface,x,y):
        surf = images.uncoveredgoal
        surface.blit(surf,self.spacerect)
    def drawPlayer(self,surface,x,y):
        self.drawSpace(surface,x,y)
        surf = images.boy
        surface.blit(surf,self.spacerect)
    def drawMap(self):
        surface = self.surface
        surface.fill(bgcolor)
        for y,row in enumerate(self.starmap):
            for x,char in enumerate(row):
                self.spacerect = pygame.Rect( (x*tilewidth,y*tilefloorheight,tilewidth,tileheight) )
                if char == '#': self.drawWall(surface,x,y)
                if char == ' ': self.drawSpace(surface,x,y)
                if self.isGoal(x,y): self.drawGoal(surface,x,y)
                if char == '$': self.drawStar(surface,x,y)
                if char == '@': self.drawPlayer(surface,x,y)
                #self.drawrectangle(surface,gray,x,y)
        return self.surface


def readLevelsFile(filename):
    assert os.path.exists(filename),'Not found %s' %filename

    mapfile = open(filename,'r')
    lines = mapfile.readlines() + ['\r\n']
    mapfile.close()
    levels = []
    rawmap = []
    for line in lines: # [ ' ### ','###### ','## $ ##', ... ]
        line = line.rstrip('\r\n')
        if ';' in line:
            line = line[:line.find(';')]
        if line != '': # this line is part of map, not blank line
            rawmap.append(line)
        elif line == '' and len(rawmap) > 0: # End of single Level reached
            maxwidth = max( map(len,rawmap) ) # find the longest row in the map
            # make line width same
            for lineno,line in enumerate(rawmap):
                rawmap[lineno] += ' ' * (maxwidth - len(line))
            # convert string to list
            # [ [' ','#','#','#',...], [' ','#',...], ... ]
            rawmap = map(list,rawmap)
            # create level
            level = Level(rawmap) 
            levels.append(level)
            # reset the variable for reading the next map
            rawmap = []
    return levels

def floodfill(amap,pos,old,new):
    x,y = pos
    width,height = len(amap[0]),len(amap)
    if x<0 or y<0 or x>width-1 or y>height-1: return
    if amap[y][x] == old: ampa[y][x] = new # x,y pos
    # check left
    if x > 0 and amap[y][x-1] == old : floodfill(amap,(x-1,y),old,new)
    # check right
    if x < width-1 and amap[y][x+1] == old: floodfill(amap,(x+1,y),old,new)
    # check up
    if y > 0 : floodfill(ampa,(x,y-1),old,new)
    # check down
    if y < height-1: floodfill(amap,(x,y+1),old,new)


if __name__ == '__main__':
    os.system('cls')
    levels = readLevelsFile('..\\starPusherLevels.txt')
    print 'Levels\n'
    for level in levels[:3]:
        level.printMap(level.rawmap)
        level.printMap()
