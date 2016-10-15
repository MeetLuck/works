from constants import *

class LevelView(object):
#   def __init__(self):
#       print 'LevelView => ',self
#       self.a =1
    def drawWall(self,x,y):
        surf = images.wall
        self.surface.blit(surf,self.spacerect)
    def drawCorner(self,x,y):
        surf = images.corner
        self.surface.blit(surf,self.spacerect)
    def drawInsideFloor(self,x,y):
        surf = images.insidefloor
        self.surface.blit(surf,self.spacerect)
    def drawOutsideFloor(self,x,y):
        surf = images.outsidefloor
        self.surface.blit(surf,self.spacerect)
    def drawStar(self,x,y):
        surf = images.star
        self.surface.blit(surf,self.spacerect)
    def drawGoal(self,x,y):
        surf = images.uncoveredgoal
        self.surface.blit(surf,self.spacerect)
    def drawPlayer(self,x,y):
        surf = images.boy
        self.surface.blit(surf,self.spacerect)
    def draw(self):
        self.drawDecoMap()
        self.drawPlayers()
        return self.surface
    def drawPlayers(self):
        for y,row in enumerate(self.starmap):
            for x,char in enumerate(row):
                self.spacerect = pygame.Rect( (x*tilewidth,y*tilefloorheight,tilewidth,tileheight) )
                if char == '@': self.drawPlayer(x,y)
                if char == '$': self.drawStar(x,y)
                if (x,y) in self.goals: self.drawGoal(x,y)
    def drawDecoMap(self):
        surface = self.surface
        surface.fill(bgcolor)
        for y,row in enumerate(self.decomap):
            for x,char in enumerate(row):
                self.spacerect = pygame.Rect( (x*tilewidth,y*tilefloorheight,tilewidth,tileheight) )
                if char == '#': self.drawWall(x,y)
                if char == 'x': self.drawCorner(x,y)
                if char == 'o': self.drawInsideFloor(x,y)
                if char == ' ': self.drawOutsideFloor(x,y)
                #self.drawrectangle(surface,gray,x,y)

class LevelModel(object):
    def __init__(self,rawmap):
        self.rawmap = rawmap # keep original
        self.width, self.height = len(self.rawmap[0]), len(self.rawmap)
        self.setupSurface()
        # initialize level
        self.reset()
    def setupSurface(self):
        surfwidth  = self.width * tilewidth      
        surfheight = (self.height-1)*tilefloorheight + tileheight
        self.surface = pygame.Surface( (surfwidth,surfheight) )
        self.surface = self.surface.convert()
    def setupMap(self):
        # get goals position and make starmap
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
    def reset(self):
        self.steps = 0
        self.lastmaps = []
        self.laststeps= []
        self.setupMap()
        self.decorateMap() # only for drawing 
    def restoreLastGameState(self):
        if not self.lastmaps : return
        self.starmap = self.lastmaps.pop()
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
    def setChar(self,pos,val):
        x,y = pos; self.starmap[y][x] = val
    def isWall(self,x,y):
        if x<0 or y<0 or x>self.width-1 or y>self.height-1: return False
        return self.getChar(x,y) == '#'
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
        # oldPlayer = player's old position
        # newPlayer = player's new position
        oldPlayer= playerX,playerY = self.getPlayer()
        if moveTo == left:  xoffset,yoffset = -1,0
        if moveTo == right: xoffset,yoffset = +1,0
        if moveTo == up:    xoffset,yoffset = 0,-1
        if moveTo == down:  xoffset,yoffset = 0,+1
        # move player if possible
        playerX += xoffset   # '@' -> '$' ->' '  ==>  ' ' -> '@' ->'$'
        playerY += yoffset
        newPlayer = (playerX, playerY)
        newStar   = (playerX+xoffset, playerY+yoffset)
        # if it is valid move, move star & player
        if self.isWall(*newPlayer): return False
        if self.isSpace(*newPlayer):
            # move player
            self.setChar(newPlayer,'@')
            self.setChar(oldPlayer,' ')
        elif self.isStar(*newPlayer):
            if self.isWall(*newStar) or self.isStar(*newStar):
                return False
            # push star and move player 
            self.setChar(newStar,'$')
            self.setChar(newPlayer,'@')
            self.setChar(oldPlayer,' ')
        # save last starmap
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
        # find player position
        playerpos = self.getPlayer()
        # remove player,stars,golas
        for y,row in enumerate(self.decomap):
            for x,char in enumerate(row):
                if char in ('@','$'): self.decomap[y][x] = ' '
        # flood fill to determine inside/outside floor tiles
        floodfill(self.decomap, playerpos,' ', 'o')
        # convert the adjoined walls into corner tiles
        #      #          #        x #       # x
        #      x #      # x        #           #
        for y,row in enumerate(self.decomap):
            for x,char in enumerate(row):
                if char != '#': continue
                # convert into corner tiles
                if self.isWall(x+1,y) and self.isWall(x,y-1) or\
                   self.isWall(x-1,y) and self.isWall(x,y-1) or\
                   self.isWall(x+1,y) and self.isWall(x,y+1) or\
                   self.isWall(x-1,y) and self.isWall(x,y+1):
                    self.decomap[y][x] = 'x'

class Level(LevelModel,LevelView):
    movesound1 = pygame.mixer.Sound('drippy.wav')
    movesound2 = pygame.mixer.Sound('move.wav')

    def __init__(self,rawmap):
        LevelModel.__init__(self,rawmap)
        LevelView.__init__(self)
        self.levelIsComplete = False
        #self.printMap()
        self.reset()

    def processKeyEvent(self):
        for event in pygame.event.get(QUIT): #if event.type == QUIT: 
            pygame.quit(); sys.exit()
        for event in pygame.event.get(KEYDOWN): #elif event.type == KEYDOWN:
            self.keypressed = True
            if event.key == K_ESCAPE:       pygame.quit(); sys.exit()
            elif event.key == K_LEFT:       self.playermoveTo = left
            elif event.key == K_RIGHT:      self.playermoveTo = right
            elif event.key == K_UP:         self.playermoveTo = up
            elif event.key == K_DOWN:       self.playermoveTo = down
            elif event.key == K_BACKSPACE:  self.reset() 
            elif event.key == K_n:          return 'next'
            elif event.key == K_b:          return 'back'
            elif event.key == K_z:          self.restoreLastGameState()
        for event in pygame.event.get(KEYUP): #elif event.type == KEYDOWN:
            pass
            #self.keypressed = False
        return None

    def runLevel(self):
        while True:
            self.playermoveTo = None
            self.keypressed = False
            result = self.processKeyEvent()
            if result: return result
            if self.playermoveTo != None:
                self.movesound1.play()
                self.makeMove(self.playermoveTo)
                os.system('cls'); self.printMap()
                if self.isFinished():
                    print 'Level Completed'
                    self.levelIsComplete = True
                    self.keypressed = False

            #------------ draw Level -------------------
            displaysurf.fill(bgcolor)
            mapsurf = self.draw()
            maprect = mapsurf.get_rect()
            maprect.center = halfwinwidth,halfwinheight
            displaysurf.blit(mapsurf,maprect)
            #drawStepCounter(displaysurf,level.steps)
            #drawLevelNumber(displaysurf,levelNum,levels)
            # --------- draw solved screen ------------
            if self.levelIsComplete:
                solvedrect = images.solved.get_rect()
                solvedrect.center = wincenter
                displaysurf.blit(images.solved,solvedrect)
                if self.keypressed:
                    return 'solved'
            pygame.display.update()
            fpsclock.tick(fps)
def main():
    levels = readLevelsFile('..\\starPusherLevels.txt')[:30]
    os.system('cls')
    print len(levels)
    levelNo = 0
    #pygame.mixer.music.load('..\\images\\mz_545_3_format0.mid')
    #pygame.mixer.music.play(-1,0.0)
    while True:
        pygame.mixer.music.load(random.choice(midilist))
        pygame.mixer.music.play(-1,0.0)
        level = levels[levelNo]
        result = level.runLevel()
        if result in ('solved','next') and levelNo != len(levels)-1:
            levelNo += 1
        elif result == 'back' and levelNo != 0:
            levelNo += -1
        pygame.mixer.music.stop()

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
            #rawmap = map(list,rawmap)
            rawmap = map(list,rawmap)
            # create level
            level = Level(rawmap)
            levels.append(level)
            # reset the variable for reading the next map
            rawmap = []
            level = []
    return levels

def floodfill(amap,pos,old,new):
    # ' ' ->'o'
    x,y = pos
    width,height = len(amap[0]),len(amap)
    if x<0 or y<0 or x>width-1 or y>height-1: return
    if amap[y][x] == old: amap[y][x] = new # x,y pos
    # check left
    if x > 0 and amap[y][x-1] == old :          floodfill(amap,(x-1,y),old,new)
    # check right
    if x < width-1 and amap[y][x+1] == old:     floodfill(amap,(x+1,y),old,new)
    # check up
    if y > 0 and amap[y-1][x] == old:           floodfill(amap,(x,y-1),old,new)
    # check down
    if y < height-1 and amap[y+1][x] == old:    floodfill(amap,(x,y+1),old,new)

if __name__ == '__main__':
    main()
    '''
    os.system('cls')
    levels = readLevelsFile('..\\starPusherLevels.txt')
    print 'Levels\n'

    for level in levels[:2]:
        level.printMap(level.rawmap)
        level.printMap()
        level.printMap(level.decomap)
        mapsurf = level.draw()
        maprect = mapsurf.get_rect()
        maprect.center = halfwinwidth,halfwinheight
        displaysurf.blit(mapsurf,maprect)
        pygame.display.update()
        pygame.time.wait(5000)
    '''

