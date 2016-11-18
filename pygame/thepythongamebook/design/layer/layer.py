import pygame,random,os
from vector import Vector
from colors import *

def write(msg='Message'):
    font = pygame.font.SysFont('None',32)
    text = font.render(msg,True,black)
    return text

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

class Mountain(pygame.sprite.Sprite):
    def __init__(self,app,atype):
        self.app = app
        self.delta = Vector()
        self.type = atype
        if self.type == 1:
            self._layer = -1
            self.delta.x = -100
            self.color = blue
        elif self.type == 2:
            self._layer = -2
            self.delta.x = -75
            self.color = pink
        else:
            self._layer = -3
            self.delta.x = -35
            self.color = red
        self.groups = app.allgroup,app.mountaingroup
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.setupImage()
        self.setPosition()
        self.parent = False

    def setupImage(self):
        w = 100 * self.type * 1.5
        h = self.app.screen.get_height()/2 + 50*(self.type-1)
        self.image = pygame.Surface( (w,h) )
        self.image.set_colorkey(black)
        pointlist = (0,h),(0,h-10*self.type),(w/2, int(random.random()*h/2)),\
                    (w,h),(9,h)
        pygame.draw.polygon(self.image, self.color, pointlist)
        self.rect = self.image.get_rect()
        self.Vp = Vector()
        self.Vp.x = self.app.screen.get_width() + self.rect.width/2
        self.Vp.y = self.app.screen.get_height() - self.rect.height/2
    def setPosition(self):
        self.rect.center = tuple(self.Vp)
    def move(self,seconds):
        self.Vp += self.delta * seconds
        self.setPosition()
    def update(self,seconds):
        self.move(seconds)
        if self.rect.centerx + self.rect.width/2 + 10 < 0:
            self.kill()
        if not self.parent:
            if self.rect.centerx < self.app.screen.get_width():
                self.parent = True
                Mountain(self.app,self.type)
class Block(pygame.sprite.Sprite):
    def __init__(self,app,blocknumber = 1):
        self.app = app
        self.blocknumber = blocknumber
        self.color = random.randint(10,255),random.randint(10,255),random.randint(10,255)
        self._layer = self.blocknumber
        self.groups = app.allgroup, app.blockgroup
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.setupImage()
        self.setPosition()
    def setupImage(self):
        self.image = pygame.Surface( (100,100))
        self.image.fill(self.color)
        self.image.blit( write(str(self.blocknumber)), (40,40) )
        self.image  = self.image.convert()
        self.rect = self.image.get_rect()
        self.Vp = Vector()
        self.Vp.x = 100 * self.blocknumber + 50
        self.Vp.y = self.app.screen.get_height()/2.0
        self.delta = Vector()
        self.delta.y = random.randint(50,100) * random.choice([-1,1])
    def setPosition(self):
        self.rect.center = tuple(self.Vp)
    def move(self,seconds):
        self.Vp += self.delta * seconds
        self.setPosition()
    def update(self,seconds):
        screenrect = self.app.screen.get_rect()
        if not screenrect.contains(self.rect):
            if self.Vp.y < screenrect.top:
                self.Vp.y = screenrect.top
                self.delta.y *= -1
            elif self.Vp.y > screenrect.bottom:
                self.Vp.y = screenrect.bottom
                self.delta.y *= -1
        self.move(seconds)

class BirdCatcher(pygame.sprite.Sprite):
    def __init__(self,app):
        self._layer = 9
        self.groups = app.allgroup, app.catchergroup
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.setupImage()
    def setupImage(self):
        self.image = pygame.Surface((100,100))
        self.image.set_colorkey(black)
        pygame.draw.circle(self.image,red,(50,50),50,2)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = 50
    def update(self,seconds):
        self.rect.center = pygame.mouse.get_pos()

class Lifebar(pygame.sprite.Sprite):
    def __init__(self,master):
        self.master = master
        self.app = self.master.app
        self.groups = self.app.allgroup, self.app.bargroup
        self._layer = self.master._layer
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.setupImage()
        self.oldpercent = 0
        self.Vp = Vector()
    def setupImage(self):
        self.width, self.height = self.master.rect.width,7
        self.image = pygame.Surface((self.width,self.height))
        self.image.set_colorkey(black)
        pygame.draw.rect(self.image, green, (0,0,self.width,self.height),1)
        self.rect = self.image.get_rect()
    def update(self,seconds):
        if self.master.health < 1:
            self.kill()
        self.percent = self.master.health/self.master.healthful
        pygame.draw.rect(self.image,black,(1,1,self.width-2,5))
        pygame.draw.rect(self.image,green,(1,1,int(self.width*self.percent),5))
        self.setPosition()
    def setPosition(self):
        self.Vp.x = self.master.rect.centerx
        self.Vp.y = self.master.rect.centery - self.master.rect.height/2 - 10
        self.rect.center = tuple(self.Vp)

class Bird(pygame.sprite.Sprite):
    image = []
    birds = {}
    number = 0
    def __init__(self,app,layer=4):
        self.app = app
        self.groups = app.birdgroup, app.allgroup
        self._layer = layer
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.delta = Vector()
        self.Vp = Vector()
        self.Vp.x = random.randint(50,app.screen.get_width()-50 )
        self.Vp.y = random.randint(50,app.screen.get_height()-25)
        self.image = Bird.image[0]
        self.rect = self.image.get_rect()
        self.health = 100.0
        self.healthful = 100.0
        self.speedmin = 10
        self.speedmax = 50
        self.radius = max(self.rect.width,self.rect.height)/2.0
        self.delta = Vector()
        self.lifetime = 0.0
        self.resetStatus()
        self.number = Bird.number
        Bird.number += 1
        Bird.birds[self.number] = self
        Lifebar(self)
        for _ in range(8):
            Fragment(self,self.Vp)
    def newSpeed(self):
        randomspeed = random.choice([-1,1])
        self.delta.x = random.randint(self.speedmin,self.speedmax)
        self.delta.y = random.randint(self.speedmin,self.speedmax)

    def resetStatus(self):
        self.catched = self.crashing = False

    def kill(self):
        for _ in range(15):
            Fragment(self,self.Vp)
        pygame.sprite.Sprite.kill(self)

    def move(self,seconds):
        self.newSpeed()
        self.Vp += self.delta * seconds
        self.rect.center = tuple(self.Vp)
    def check(self):
        screenrect = self.app.screen.get_rect()
        if not screenrect.contains(self.rect):
            self.kill()
        elif self.health <= 0:
            self.kill()

    def update(self,seconds):
        if self.crashing:
            self.health -= 1
        self.check()
        self.lifetime += seconds
        if abs(self.delta.x) > self.speedmax:
            self.delta.x = self.speedmax 
        if abs(self.delta.y) > self.speedmax:
            self.delta.y = self.speedmax 
        self.image = Bird.image[self.crashing + 2*self.catched]
        self.move(seconds)

class Fragment(pygame.sprite.Sprite):
    def __init__(self,master,pos):
        self._layer = 9
        self.groups = master.app.allgroup, master.app.fragmentgroup
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.target = pos
        self.Vp = pos
        self.maxspeed = 2.0*master.speedmax
        self.setupImage()
    def setupImage(self):
        self.color = random.randint(50,255),0,0
        self.delta = Vector()
        self.delta.x = random.randint(-self.maxspeed,self.maxspeed)
        self.delta.y = random.randint(-self.maxspeed,self.maxspeed)
        self.lifetime = 1 + 3*random.random()
        self.image = pygame.Surface((10,10))
        self.image.set_colorkey(black)
        pygame.draw.circle(self.image, self.color, (5,5), random.randint(2,5))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = tuple(self.Vp)
        self.time = 0.0
    def move(self,seconds):
        self.Vp += self.delta * seconds
        self.rect.center = tuple(self.Vp)
    def update(self,seconds):
        self.time += seconds
        if self.time > self.lifetime:
            self.kill()
        self.move(seconds)

