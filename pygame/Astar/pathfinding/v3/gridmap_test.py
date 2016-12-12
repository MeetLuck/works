import pygame
from gridmap import GridMap
from colors import *
from Astar3 import *
bgcolor = lightgray

class App:
    def __init__(self,gridsize=20):
        self.running = True
        self.initPygame()
        self.initGridMap(gridsize)
    def initPygame(self):
        pygame.init()
        resolution = 640,480
        self.screen = pygame.display.set_mode(resolution)
        self.screen.fill(bgcolor)
        self.rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()

    def initGridMap(self,gridsize):
        self.gridsize = gridsize
        self.Nrows = self.rect.height/gridsize
        self.Ncols = self.rect.width/gridsize
        self.gridmap = GridMap(self.Nrows,self.Ncols)
        self.Astar = Astar(self)#,start_pos,goal_pos)
        self.path = None

    def onEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F5:
                self.path = self.Astar.findPath()
            elif event.key == pygame.K_SPACE:
                self.Astar.step()
            elif event.key == pygame.K_RETURN:
                self.Astar.reset()
                self.path = None
            elif event.key == pygame.K_ESCAPE:
                self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.onMouseClick(event)

    def onMouseClick(self,event):
        if not self.rect.collidepoint(event.pos): return
        row = (event.pos[1] - self.rect.top) /self.gridsize
        col = (event.pos[0] - self.rect.left)/self.gridsize
        coord = (row,col)
        if event.button   == 1: self.gridmap.setStart(coord)
        elif event.button == 2: self.gridmap.setWall(coord)
        elif event.button == 3: self.gridmap.setGoal(coord)

    def getRect(self,coord):
        row,col = coord
        topleft = col*self.gridsize,row*self.gridsize
        rect =   topleft,(self.gridsize,self.gridsize)
        return pygame.Rect(rect)

    def drawTile(self,coord,color=darkgray,thinkness=1):
        rect = self.getRect(coord)
        rect = rect.x + 1, rect.y + 1, rect.w - 1, rect.h - 1
        pygame.draw.rect(self.screen,color,rect,thinkness)

    def drawCircle(self,coord,color=black):
        rect = self.getRect(coord)
        pygame.draw.circle(self.screen,color,rect.center,self.gridsize/4)

    def drawStart(self,coord):
        self.drawCircle(coord,blue)
    def drawGoal(self,coord):
        self.drawCircle(coord,red)
    def drawWall(self,coord):
        rect = self.getRect(coord)
        pygame.draw.rect(self.screen,gray,rect)

    def drawExplored(self): #,explored):
#       print 'draw Explored => %s' %explored
        for node in self.Astar.explored:
            self.drawTile(node.coord,darkgreen,1)

    def drawMap(self):
        for row in range(self.Nrows):
            for col in range(self.Ncols):
                coord = row,col
                self.drawTile(coord)
                val = self.gridmap.get(coord)
                if   val == 'S': self.drawStart(coord)
                elif val == 'G': self.drawGoal(coord)
                elif val in [1,True]: self.drawWall(coord)
    def drawCurrent(self):
        current = self.Astar.current
        if current is None: return
        camefrom = current.camefrom
        if camefrom is None: return
        r,c = current.coord
        N  = r-1, c
        S  = r+1, c
        W  = r+0, c-1
        E  = r+0, c+1
        NE = r-1, c+1
        NW = r-1, c-1
        SW = r+1, c-1
        NW = r-1, c-1
#       if camefrom.coord == N: # from N
        print 'current, camefrom', current.coord,camefrom.coord
        pygame.draw.line(self.screen, red, current.coord, camefrom.coord,1)


    def drawPath(self):
        if not self.path: return
        #print "============> found path <============="
        for node in self.path: 
            self.drawTile(node.coord,red,1)
    def render(self,seconds):
        self.screen.fill(bgcolor)
        self.drawMap()
        self.drawExplored()
        self.drawPath()
        self.drawCurrent()
        pygame.display.flip()
        #self.gridmap.printme()

    def exit(self):
        pygame.quit()

    def mainloop(self):
        fps = 60
        while self.running:
            seconds = self.clock.tick(fps)/1000.0
            for event in pygame.event.get():
                self.onEvent(event)
            self.render(seconds)
        self.exit()

if __name__ == '__main__':
    App(40).mainloop()

