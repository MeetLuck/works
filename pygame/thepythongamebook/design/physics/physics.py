import pygame,random,os,sys
import sys
sys.path.insert(0,'..')
from vector import Vector
from colors import *

def write(msg='Message'):
    font = pygame.font.SysFont('None',32)
    text = font.render(msg,True,black)
    return text

def getClassname(instance):
    text = str(instance.__class__)  # "<class '__main__.XWing'>"
    parts = text.split('.')         # [ "<class '__main__",  "XWing'>"  ]
    return parts[-1][0:-2]          # from the last(-1) part, take all but the last 2 chars

def elasticCollision(sprite1, sprite2):
    # first we get the direction of the push
    # assume that the sprites are disk shaped, so the direction of the force is
    # the direction of the distance
    direction = sprite1.Vp - sprite2.Vp
    # the velocity of the center of mass
    sumOfMasses = sprite1.mass + sprite2.mass
    velocity = ( sprite1.delta * sprite1.mass + sprite2.delta * sprite2.mass ) / sumOfMasses

class Text(pygame.sprite.Sprite):
    def __init__(self,app,msg):
        self.groups = app.allgroup, app.textgroup
        self._layer = 99
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.app = app
        self.newMsg(msg)
    def newMsg(self, msg='New message'):
        self.image = write(msg)
        self.rect = self.image.get_rect()
        self.rect.center = self.app.screen.get_width()/2,10
    def update(self,seconds):
        pass


class Lifebar(pygame.sprite.Sprite):
    def __init__(self,master):
        self.app = self.master.app
        self.groups = self.app.allgroup
        self._layer = self.master._layer
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.Vp = Vector()
        self.paint()
    def paint(self):
        self.width, self.height = self.master.rect.width, 7
        self.image = pygame.Surface((self.width, self.height))
        self.image.set_colorkey(black)
        pygame.draw.rect(self.image,green,(0,0,self.width,self.height),1)
        self.rect = self.image.get_rect()
    def setPosition(self):
        self.Vp.x = self.master.rect.centerx
        self.Vp.y = self.master.rect.centery - self.master.rect.height/2.0 - 10
        self.rect.center = tuple(self.Vp)
    def update(self,seconds):
        self.percent = self.master.health/self.master.healthful
        self.paint()
        pygame.draw.rect(self.image,black, (1,1,self.width-2,5))
        pygame.draw.rect(self.image,green,(1,1,int(self.width*self.percent),5) )
        self.setPosition()
        if self.master.health < 1:
            self.kill()

class Bird(pygame.sprite.Sprite):
    image = list()
    birds = dict()
    number = 0
    def __init__(self,app,layer=4):
        self.groups = app.birdgroup, app.allgroup, app.gravitygroup
        self._layer = layer
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.health = 30.0
        self.healthful = 30.0
        self.lifetime = 0.0
        self.crashing = False
        self.frags = 25
        self.number = Bird.number
        Bird.number += 1
        Bird.birds[self.number] = self
        self.paint()
        self.delta = Vector()
        self.Vp = Vector( random.randint(50, app.screen.get_width() - 50),
                          random.randint(25, app.screen.get_height()-25 ) )
        Lifebar(self)
        self.app.warsound.play()
    def paint(self):
        self.image = Bird.image[2]
        self.image = Bird.image[0]
        self.rect = self.image.get_rect()
        self.radius = max(self.rect.width, self.rect.height) / 2.0
    def kill(self):
        for i in range(self.frags):
            Fragment(self.Vp)
        pygame.sprite.Sprite.kill(self)
    def checkArea(self):
        area = self.app.screen.get_rect()
        if not area.contains(self.rect):
            self.crashing = True
            if self.Vp.x + self.rect.width/2 > area.right:
                self.Vp.x = area.right - self.rect.width/2
                self.delta.x *= -0.5
            if self.Vp.x - self.rect.width/2 < area.left:
                self.Vp.x = area.left + self.rect.width/2
                self.delta.x *= -0.5
            if self.Vp.y + self.rect.height/2 > area.bottom:
                self.Vp.y = area.bottom - self.rect.height/2
                self.delta.y *= -0.5
            if self.Vp.y - self.rect.height/2 < area.top:
                self.Vp.y = area.top + self.rect.height/2
                self.delta.y *= -0.5
    def update(self,seconds):
        self.lifetime += seconds
        self.Vp  += self.delta * seconds
        self.checkArea()
        self.image = Bird.image[self.crashing]
        self.image = self.image.copy()
        self.angle = math.atan2(-self.delta.y,self.delta.x)/math.pi * 180
        self.image = pygame.transform.rotozoom(self.image0, self.angle,1.0)
        self.rect.center = tupe(self.Vp)
        if self.health <= 0:
            self.kill()

