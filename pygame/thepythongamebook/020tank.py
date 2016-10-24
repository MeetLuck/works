''' 020 shooting from tank.py
    demo of 2 tanks shooting bullets at the end of it's cannon
    and shooting tracers at the end of it's bow Machine Gun
    and from the turret-machine gun (co-axial with main gun)
    '''
from constants020 import *
import copy

class Bullet(pygame.sprite.Sprite):
    ''' a big projectile fired by the thank's main cannon'''
    side = 7  # small side of bullet retangle
    vel = 180.0 # velocity
    mass = 50.0
    maxlifetime = 10.0 # seconds

    def __init__(self,boss):
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.delta = Vector(0,0)
        self.color = self.boss.color
        self.calculateHeading()
        self.delta += self.boss.delta # add boss's movement
        self.pos = copy.copy(self.boss.pos) # copy boss's position
        self.calculateOrigin()
        self.update()
    def calculateHeading(self):

class Lifebar(pygame.sprite.Sprite):
    def __init__(self,boss):
        self.groups = allgroup,lifebargroup
        self.boss = boss
        self._layer = self.boss._layer
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.oldpercent = 0
        self.paint()
    def paint(self):
        self.image = pygame.Surface( (self.boss.rect.width,7) )
        self.rect = self.image.get_rect()
        self.image.set_colorkey(black)
        pygame.draw.rect(self.image,green,(0,0,self.boss.rect.width,7),1)
    def update(self,seconds):
        self.percent = self.boss.hitpoints/self.boss.hitpointsfull
        if self.percent != self.oldpercent:
            self.paint()
            # fill black
            pygame.draw.rect(self.image,black,(1,1,self.rect.width-2,5) )
            pygame.draw.rect(self.image,green,(1,1,int(self.rect.width*self.percent),5) )
        self.oldpercent = self.percent
        self.rect.centerx = self.boss.rect.centerx
        self.rect.centery = self.boss.rect.top - 10
        if self.boss.hitpoints < 1: self.kill()

class Bird(pygame.sprite.Sprite):
    images = []
    birds = {}  # dictionary for saving bird objects
    number = 0
    waittime = 1.0 # seconds
    def __init__(self,layer=4):
        if getClassName(self) == 'Monster':
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
        self.number = Bird.number
        Bird.number += 1
        Bird.birds[self.number] = self
        self.mass = 100

    def kill(self):
        for a in range(self.frags):
            pass
            #RedFragment(self.pos)
        pygame.sprite.Sprite.kill(self)
    def checkArea(self):
        if self.screen.contains(self.rect): return
        # OUT OF SCREEN
        print 'OUT OF SCREEN',self.rect.center
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
        self.delta = self.direction * self.speed
        self.pos += self.delta * seconds
        self.checkArea()
    def update(self, seconds):
        # move
        self.move(seconds)
        # rotating
        if self.delta.x != 0 or self.delta.y != 0:
            ratio = self.delta.y/self.delta.x
            if self.delta.x > 0: # moving right
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
            self.delta = Vector( random.randint(-100,100), random.randint(-50,50) )
        Bird.update(self,time)

class Player(Bird):
    def __init__(self):
        self.image = Bird.images[0]
        self.image0 = Bird.images[0]
        Bird.__init__(self,layer=5)
        self.hitpoints = 100.0
        self.hitpointsfull = 100.0
        self.rect.center  = screenrect.center
        self.pos = Vector(self.rect.center) # = tuple(self.pos)
        self.angle = 0
        self.speed = 10.0 
        self.rotatespeed = 1.0
        self.frags = 100
        Lifebar(self)
        self.cooldowntime = 0.08 # seconds
        self.cooldown = 0.0
        self.damage = 5
        self.shots = 0
        self.mass = 400.0
        self.direction = Vector(0,0)
    def kill(self):
        bombsound.play()
        Bird.kill(self)
    def update(self, seconds):
        pressedkeys = pygame.key.get_pressed()
        rad = self.angle*GRAD
        if pressedkeys[pygame.K_k]: # go upward(forward)
            self.direction = Vector( -sin(rad),-cos(rad) )
            self.speed *= 1.05 
        if pressedkeys[pygame.K_j]: # go downward(backward)
            #self.direction = Vector( sin(rad),cos(rad) )
            self.speed *= 0.95 
        # move
        self.move(seconds)
        # rotate
        if pressedkeys[pygame.K_a]: # turn left, counterclockwise
            self.angle += self.rotatespeed
        if pressedkeys[pygame.K_d]:
            self.angle += -self.rotatespeed

        self.turn()
        if self.hitpoints <= 0:
            self.kill()
    def turn(self):
        self.oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.rect = self.image.get_rect(center= self.oldcenter)
        self.rect.center = tuple(self.pos) #.x, self.pos.y
        print self.pos, self.rect.center, self.angle

# load images into classes (class variable !). if not possible, draw ugly images
Bird.images.append(pygame.image.load(os.path.join(folder,"babytux.png")))
Bird.images.append(pygame.image.load(os.path.join(folder,"crossmonster.png")))
Bird.images.append(pygame.image.load(os.path.join(folder,"xmonster.png")))
        # ------------
for bird in Bird.images:
    bird = bird.convert_alpha()

def main():
    collision = 'rect'
    screentext = Text()
    screentext2 = Text('collision detection: %s' %collision,(200,0))
    othergroup = []
    mainloop = True
    player = Player()
    #dummy = Monster(Bird.images[1])
    #dummy2 = Monster(Bird.images[2])
    overtime = 15
    gameover = False
    hits = 0
    quota = 0
    gametime = 120
    playtime = 0
    gravity = True

    while mainloop:
        seconds = clock.tick(fps)/1000.0
        playtime += seconds
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    mainloop = False
                if e.key == pygame.K_g:
                    gravity = not gravity
                if e.key == pygame.K_p:
                    printSpritelist()
                if e.key == pygame.K_c:
                    if collision == 'rect':
                        collision = 'circle'
                    elif collision == 'circle':
                        collision = 'mask'
                    elif collision == 'mask':
                        collision = 'rect'
                    screentext2.newMsg('collision detection: %s',collision)

        pygame.display.set_caption("fps: %.2f gravity: %s" % (clock.get_fps(), gravity) )

        for bird in birdgroup:
            if collision =='rect':
                crashgroup = pygame.sprite.spritecollide(bird,bulletgroup,False,pygame.sprite.collide_rect)
            if collision =='circle':
                crashgroup = pygame.sprite.spritecollide(bird,bulletgroup,False,pygame.sprite.collide_circle)
            if collision =='mask':
                crashgroup = pygame.sprite.spritecollide(bird,bulletgroup,False,pygame.sprite.collide_mask)
            # test for collision with bullet
            for bullet in crashgroup:
                if bullet.boss.number != bird.number:
                    hitsound.play()
                    bird.hitpoints -= bullet.boss.damage
                    Wound(bullet.rect.center,bird)
                    bullet.kill()
        if gravity:
            for thing in gravitygroup:
                thing.pos.y += FORCEOFGRAVITY/fps

        # ----------- clear, draw , update, flip -----------------  
        allgroup.clear(screen, background)
        allgroup.update(seconds)
        allgroup.draw(screen)           
        pygame.display.flip()         

if __name__ == "__main__":
    main()
