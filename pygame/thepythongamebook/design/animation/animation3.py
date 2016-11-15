import pygame,os
from colors import *
from vector import Vector

class Lion(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.speed = 25 * 4
        self.makeImages()
        self.index = 0
        self.image = self.lions[self.index] 
        self.rect = self.image.get_rect()
        self.Vp = Vector(300,500)
        self.setPosition()

    def setPosition(self):
        self.rect.center = tuple(self.Vp)

    def makeImages(self):
        folder = '../../data'
        spritesheet = pygame.image.load( os.path.join(folder,'char9.bmp') )
        self.lions = list()
        w,h = 127,127
        for no in range(4): # first line contains 4 lions
            self.lions.append( spritesheet.subsurface( (127*no,64,w,h)) )
        for no in range(2):
            self.lions.append( spritesheet.subsurface( (127*no,262-64,w,h) ) )
        self.lions1= list()
        for lion in self.lions:
            lion1 = pygame.transform.scale(lion,(100,100))
            lion1.set_colorkey(black)
            lion1 = lion1.convert_alpha()
            self.lions1.append(lion1)
        self.lions = self.lions1[:]


    def getdiffAngle(self,player):
        if player is None: return
        delta = player.Vp - self.Vp
        targetAngle = atan2(-delta.y,delta.x)/pi * 180
        diffAngle = targetAngle - self.tankAngle
        if diffAngle < 0: diffAngle += 360
        diffAngle %= 360
        return diffAngle

    def calculateDirection(self):
        mousepos = pygame.mouse.get_pos()
        self.Vd = Vector(mousepos) - self.Vp
        self.Vd.normalize()

    def move(self,seconds):
        self.calculateDirection()
        self.Vp += self.Vd * self.speed * seconds
        self.index += 1
        self.index %= 6
        self.image = self.lions[self.index]
        self.setPosition()
    def stop(self):
        self.index = 0
        self.image = self.lions[self.index]
        self.setPosition()

    def update(self,seconds):
        left_mouse_pressed = pygame.mouse.get_pressed()[0]
        if left_mouse_pressed:
            self.move(seconds)
