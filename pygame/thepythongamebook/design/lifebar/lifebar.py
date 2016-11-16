import pygame,random
import sys
# add the 'design' folder path to the sys.path list
sys.path.append('../../design')
from ..vector import Vector
from .. colors import *

class BirdCatcher(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.makeImage()

    def setupImage(self):
        r = 50
        self.image = pygame.Surface( (2*r,2*r) )
        self.image.set_colorkey(black)
        pygame.draw.circle(self.image, red, (r,r),r,2)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = r

    def update(self,seconds):
        self.rect.center = pygame.mouse.get_pos()

class Fragment(pygame.sprite.Sprite):
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.Vp = Vector(pos)
        self.setupImage()
        self.lifetime = 1 + 5*random.random() 
        self.time = 0
        self.maxspeed = birdspeedmax

    def setupImage(self):
        self.image = pygame.Surface((10,10))
        self.image.set_colorkey(black)
        randomred = random.randint(1,64),0,0
        pygame.draw.circle(self.image, randomred, (5,5), random.randint(2,5) )
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.setPosition()

    def setPosition(self):
        self.rect.center = tuple(self.Vp)

    def move(self,seconds):
        self.delta = Vector()
        self.delta.x = random.randint(-self.maxspeed,self.maxspeed)
        self.delta.y = random.randint(-self.maxspeed,self.maxspeed)
        self.Vp += self.delta * seconds
        self.setPosition()

    def update(self,seconds):
        self.time += seconds
        if self.time > self.lifetime:
            self.kill()
        else:
            self.move(seconds)


class Lifebar(pygame.sprite.Sprite):

    def __init__(self,master):
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.master = master
        self.width,self.height = self.master.rect.width,7

    def setupImage(self):
        self.image = pygame.Surface( (self.width,self.height) )
        self.image.set_colorkey(black)
        # draw green rect
        pygame.draw.rect(self.image,green,(0,0,self.width,self.height),1)
        self.rect = self.image.get_rect()
        self.oldpercent = 0

    def setPosition(self):
        self.rect.centerx = self.master.rect.centerx
        self.rect.centery = self.master.rect.centery - self.master.rect.height/2 - 10

    def isMasterAlive(self):
        return Bird.birds[self.master.number]

    def update(self,seconds):
        if not self.isMasterAlive():
            self.kill()
            return
        self.percent = self.master.health/self.master.healthful
        if self.percent != self.oldpercent:
            # filled black rect
            pygame.draw.rect(self.image,black,(1,1,self.width-2,5))
            # filled green rect
            w = int(self.width*self.percent)
            pygame.draw.rect(self.image,green,(1,1,w,5) )
        self.oldpercent = self.percent
        self.setPosition()


class Bird(pygame.sprite.Sprite):
    image = []
    birds = {}
    number = 0
    def __init__(self, startpos):
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.Vp = Vector(startpos)
        self.healthful = 100.0
        self.health    = 100.0
        self.image = Bird.image[0]
        self.rect = self.image.get_rect()
        self.radius = max(self.rect.width,self.rect.height)/2.0
        self.resetStatus()
        self.number = Bird.number
        Bird.number += 1
        Bird.birds[self.number] = self
        Lifebar(self)
    def setPosition(self):
        self.rect.center = tuple(self.Vp)
    def move(self,seconds):
        randomdirection = random.choice([-1,1])
        self.delta = Vector()
        self.delta.x = random.random() * speedmax * randomdirection + randomdirection
        self.delta.y = random.random() * speedmax * randomdirection + randomdirection
        self.Vp += self.delta * seconds
        self.setPosition()
    def resetStatus(self):
        self.catched = self.crashing = False
    def kill(self):
        crysound.play()
        for t in range(random.randint(3,15)):
            Fragment(self.Vp)
        Bird.birds[self.number] = None
        pygame.sprite.Sprite.kill(self)
    def checkHealth(self):
        if self.health <= 0:
            self.kill()
            return None
        if self.crashing:
            self.health -= 1

    def update(self,seconds):
        if not self.checkHealth(): return
        self.image = Bird.image[self.crashing + 2*self.catched]
        self.move(seconds)


