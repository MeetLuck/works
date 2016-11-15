import pygame,os
from colors import *

class Lion(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.makeImages()
        self.index = 0
        self.image = self.lions[self.index] 
        self.rect = self.image.get_rect()
        self.setPosition()

    def setPosition(self):
        self.rect.center = 300,300

    def makeImages(self):
        folder = '../../data'
        spritesheet = pygame.image.load( os.path.join(folder,'char9.bmp') )
        self.lions = list()
        w,h = 127,127
        for no in range(5): # first line contains 4 lions
            self.lions.append( spritesheet.subsurface( (127*no,64,w,h)) )
        for no in range(2):
            self.lions.append( spritesheet.subsurface( (127*no,262-64,w,h) ) )
        for lion in self.lions:
            lion.set_colorkey(black)
            lion = lion.convert_alpha()

    def update(self,seconds):
        self.index += 1
        self.index %= 6
        self.image = self.lions[self.index]
        self.setPosition()
