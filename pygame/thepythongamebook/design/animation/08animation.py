import pygame,random,os
from colors import *

class App:
    def __init__(self):
        self.initPygame()
        self.makeLions()
        self.running = True

    def initPygame(self):
        pygame.init()
        screensize = 800,600
        self.screen = pygame.display.set_mode(screensize)
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(white)
        self.background = self.background.convert()
        self.screen.blit(self.background,(0,0))

    def makeLions(self):
        folder = '../../data'
        spritesheet = pygame.image.load(os.path.join(folder,'char9.bmp') )
        self.lions = list()
        for nbr in range(1,5,1): # first line contains 4 pictures of lions
            self.lions.append( spritesheet.subsurface( (127*(nbr-1),64,127,127) ) )
        for nbr in range(5,7,1): # second line contains 2 pictures of lions
            self.lions.append( spritesheet.subsurface( (127*(nbr-5),262-64,127,127) ) )
        for lion in self.lions:
            lion.set_colorkey(black)
            lion = lion.convert_alpha()

    def onEvent(self,event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.running = False

    def render(self):
        #self.screen.blit( self.background.subsurface( (300,300,128,66)),(300,300))
        #self.screen.blit( self.lions[self.picNo],(300,300) )
        self.background.fill(white)
        self.background.blit( self.lions[self.picNo],(300,300) )
        self.screen.blit(self.background,(0,0))
        self.picNo += 1
        self.picNo %= 6
        #if self.picNo > 5: self.picNo = 0
        pygame.display.set_caption('fps: %.2f picture: %i' %(1/self.seconds, self.picNo) )
        pygame.display.flip()

    def cleanUp(self):
        pygame.quit()

    def mainloop(self):
        fps = 30
        clock = pygame.time.Clock()
        self.picNo = 0
        while self.running:
            self.seconds = clock.tick(fps)/1000.0
            for event in pygame.event.get():
                self.onEvent(event)
            self.render()
        self.cleanUp()

if __name__ == '__main__':
    App().mainloop()


