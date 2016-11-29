from Graph2 import *

class App:
    def __init__(self,grid):
        self.running = True
        self.OnInit()
        g = Graph(grid)
        self.search = Search(g,'A','T')
        self.search.reset()
    def OnInit(self):
        pygame.init()
        resolution = 640,480
        self.screen = pygame.display.set_mode(resolution)
        self.screen.fill(bgcolor)
        self.clock = pygame.time.Clock()
    def onEvent(self,event):
        if event.type == pygame.QUIT or event.type==pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.running = False
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.search.step()
            if event.key == pygame.K_r:
                self.search.reset()
            if event.key == pygame.K_RETURN:
                print 'return Pressed'
                self.search.run()
    def cleanUp(self):
        pygame.quit()
    def render(self,seconds):
        #self.screen.fill(bgcolor)
        self.search.draw(self.screen)
        pygame.display.flip()
    def mainloop(self):
        fps = 60
        while self.running:
            seconds = self.clock.tick(fps)
            for event in pygame.event.get():
                self.onEvent(event)
            self.render(seconds)
        self.cleanUp()

if __name__ == '__main__':
    App(grid).mainloop()
#g = Graph(grid)
#search = Search(g,'A','T')
#search.reset()
#search.render()
#for i in range(40):
#    search.step()
#    search.draw(screen)
#    pygame.display.flip()
#    pygame.time.wait(200)
#   search.step()
#   print g.labels
#   for node in g.nodes:
#       print node
