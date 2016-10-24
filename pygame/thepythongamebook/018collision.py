''' toggle collision dection with C
    shoot on the giant monsters and watch the yellow impact 'wounds'
    '''
from constants18 import *

class Lifebar(pygame.sprite.Sprite):
    def __init__(self,boss):
        self.groups = allgroup,lifebargroup
        self.boss = boss
        self._layer = self.boss._layer
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.oldpercent = 0
        self.paint()
    def paint(self):
        self.image = pygame.Surface( (self.bos.rect.width,7) )
        self.rect = self.image.get_rect()
        self.image.set_colorkey(black)
        pygame.draw.rect(self.image,green,(0,0,self.boss.rect.width,7),1)
    def update(self,time):
        self.percent = self.boss.hitpoint/self.boss.hitpointsfull
        if self.percent != self.oldpercent:
            self.paint()
            # fill black
            pygame.draw.rect(self.image,black,(1,1,self.rect.width-2,5) )
            pygame.draw.rect(self.image,green,int(self.rect.width*self.percent),5)
        self.oldpercent = self.percent
        self.rect.centerx = self.boss.rect.centerx
        self.rect.centery = self.boss.rect.top - 10
        if self.boss.hitpoints < 1: self.kill()

class Bird(pygame.sprite.Sprite):
    images = []
    birds = []
    number = 0
    waittime = 1.0 # seconds
    def __init__(self,layer=4):
        if getclassname(self) == 'Monster':
            self.groups = birdgroup,allgroup
        else:
            self.groups = birdgroup, allgroup, gravitygroup
        self_layer = layer
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.pos = Vector(random.randint(50, screenwidth-50), random.randint(25,screenheight-25) )
        self.screen = screen.get_rect()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width/2
        self.delta = Vector(0,0) #self.dx, self.dy = 0.0, 0.0
        self.frags = 25
        self.number = Birdnumber
        Bird.number += 1
        Bird.birds[self.number] = self
        self.mass = 100

    def kill(self):
        for a in range(self.frags):
            RedFragment(self.pos)
        pygame.sprite.Sprite.kill(self)
    def checkArea(self):
        if self.screen.contains(self.rect): return
        # OUT OF SCREEN
        w,h = self.rect.width, self.rect.height
        if self.rect.right > self.screen.right:
            self.pos.x = self.screen.right - w/2
            self.delta.x *= -0.5
        if self.rect.left < self.screen.left:
            self.pos.x = self.screen.left + w/2
            self.delta.x *= -0.5
        if self.rect.top < self.screen.top:
            self.pos.y = self.screen.top + h/2
            self.delta.y *= -0.5
        if self.rect.bottom > self.screen.bottom:
            self.pos.y = self.screen.bottom - h/2
            self.delta.y *= -0.5
    def move(self,seconds):
        #self.x += self.dx * seconds
        #self.y += self.dy * seconds
        self.pos = self.delta * seconds
        self.checkArea()
    def update(self, seconds):
        # move
        self.move(seconds)
        # rotating
        if self.delta.x != 0 or self.delta.y != 0:
            ratio = self.delta.y/self.delta.x
            if self.dx > 0: # moving right
                self.angle = -90 - atan(ratio)/pi * 180 
            else: # moving left
                self.angle = 90 - atan(ratio)/pi * 180
        self.rect.center = self.pos.x, self.pos.y
        # check health
        if self.hitpoints <= 0: self.kill()

class Monster(Bird):
    def __init__(self,image):
        self.image = image
        Bird.__init__(self)
        self.mask = pygame.mask.from_surface(self.image)
        self.hitpoints = 1000.0
        self.hitpointsfull = 1000.0
        Lifebar(self)
    def update(self,time):
        if random.randint(1,60) == 1:
            self.delta = Vector(
            self.dx = random.randint(-100,100)
            self.dy = random.randint(-50,50)
        Bird.update(self,time)

class Player(Bird):
    def __init__(self):
        self.image = Bird.images[0]
        self.image0 = Bird.images[0]
        Bird.__init__(self,layer=5)
        self.hitpoints = 100.0
        self.hitpointsfull = 100.0
        self.pos = screenwidth/2, screeneheight/2
        self.angle = 0
        self.speed = 20.0 
        self.rotatespeed = 1.0
        self.frags = 100
        Lifebar(self)
        self.cooldowntime = 0.08 # seconds
        self.cooldown = 0.0
        self.damage = 5
        self.shots = 0
        self.mass = 400.0
    def kill(self):
        bombsound.play()
        Bird.kill(self)
    def update(self,time):
        pressedkeys = pygame.key.get_pressed()
        self.direction = Vector(0,0)
        rad = self.angle*GRAD
        if pressedkeys[pygame.K_k]: # go upward(forward)
            self.direction = Vector( -sin(rad),-cos(rad) )
        if pressedkeys[pygame.K_j]: # go downward(backward)
            self.direction = Vector( sin(rad),cos(rad) )

        if self.cooldown > 0:
            self.cooldown -= time
        else:
            if pressedkeys[pygame.K_SPACE]:
                lasersound.play()
                self.shots += 1
                Bellet(self, -sin(rad), -cos(rad) )
            self.cooldown = self.cooldowntime
        # move
        self.delta = self.direction * self.speed
        self.pos  += self.delta * seconds
        self.checkArea()
        # rotate
        if pressedkeys[pygame.K_a]: # turn left, counterclockwise
            self.angle += self.rotatespeed
        if pressedkeys[pygame.K_d]:
            self.angle += -self.rotatespeed
        self.oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.rect = self.image.get_rect(center= self.oldcenter)
        self.rect.center = self.pos[0], self.pos[1]
        if self.hitpoints <= 0:
            self.kill()





