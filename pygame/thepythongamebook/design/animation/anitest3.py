from animation3 import *

class App:
    def __init__(self):
        self.initPygame()
        self.setGroups()
        self.running = True
        self.lion = Lion()

    def initPygame(self):
        pygame.init()
        pygame.mouse.set_visible(True)
        screensize = 800,600
        self.screen = pygame.display.set_mode(screensize)
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(white)
        self.background = self.background.convert()
        # self.drawSpriteSheet()
        self.screen.blit(self.background,(0,0))

    def drawSpriteSheet(self):
        folder = '../../data'
        spritesheet = pygame.image.load( os.path.join(folder,'char9.bmp') )
        rect = spritesheet.get_rect()
        pygame.draw.rect(spritesheet,blue,rect,2)
        spritesheet.set_colorkey(black)
        self.background.blit(spritesheet,(0,0))

    def setGroups(self):
        # set sprites group
        self.liongroup = pygame.sprite.Group()
        self.allgroup = pygame.sprite.LayeredUpdates()
        # set _layer
        Lion._layer = 4 
        Lion.groups = self.liongroup, self.allgroup


    def onEvent(self,event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.running = False

    def render(self,seconds):
        self.allgroup.clear(self.screen,self.background)
        self.allgroup.update(seconds)
        self.allgroup.draw(self.screen)
        pygame.display.set_caption('fps: %.2f picture: %i' %(1/self.seconds, self.picNo) )
        pygame.display.flip()

    def cleanUp(self):
        pygame.quit()

    def mainloop(self):
        fps = 60
        clock = pygame.time.Clock()
        self.picNo = 0
        while self.running:
            self.seconds = clock.tick(fps)/1000.0
            for event in pygame.event.get():
                self.onEvent(event)
            self.render(self.seconds)
        self.cleanUp()

if __name__ == '__main__':
    App().mainloop()


