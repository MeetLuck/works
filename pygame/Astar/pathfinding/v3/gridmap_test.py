import pygame
from gridmap import GridMap
from colors import *
from Astar2 import *
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
        self.Astar = Astar(self.gridmap.getReachables)
        self.path = None
    def onEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F5:
                start_pos,goal_pos = self.gridmap.start_pos, self.gridmap.goal_pos
                self.path = self.Astar.findPath(start_pos,goal_pos)
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
        return  topleft,(self.gridsize,self.gridsize)
    def drawtile(self,coord):
        rect = self.getRect(coord)
        pygame.draw.rect(self.screen,black,rect,1)
    def drawCircle(self,coord,color=black):
        rect = self.getRect(coord)
        rect = pygame.Rect(rect)
        pygame.draw.circle(self.screen,color,rect.center,self.gridsize/4)
    def drawStart(self,coord):
        self.drawCircle(coord,blue)
    def drawGoal(self,coord):
        self.drawCircle(coord,red)
    def drawWall(self,coord):
        rect = self.getRect(coord)
        pygame.draw.rect(self.screen,gray,rect)
    def drawMap(self):
        for row in range(self.Nrows):
            for col in range(self.Ncols):
                coord = row,col
                self.drawtile(coord)
                val = self.gridmap.get(coord)
                if   val == 'S': self.drawStart(coord)
                elif val == 'G': self.drawGoal(coord)
                elif val in [1,True]: self.drawWall(coord)
    def drawPath(self):
        if not self.path: return
        for node in self.path: 
            coord = node.coord
            self.drawCircle(coord,pink)
    def render(self,seconds):
        self.screen.fill(bgcolor)
        self.drawMap()
        self.drawPath()
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

