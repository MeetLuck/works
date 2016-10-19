# 017 turning and physics.py
# move the BIG bird around with W,A,S,D and Q and E
# fire with SPACE, toggle gravity with G

from constants017 import *

def elasticCollision(sprite1,sprite2):
    # elastic collision between 2 sprites(calculated as disc's)
    # this function alters the dx and dy movement vectors of both sprites
    # the sprites need the property .mass, .radius, .pos[0], .pos[1], .dx, .dy

    # 1st, we get the direction of the push
    # let's assume that the sprites are disk shaped, so the direction of the force
    # is the direction of the distance.
    dirx = sprite1.pos[0] - sprite2.pos[0]
    diry = sprite1.pos[1] - sprite2.pos[1]
    # the velocity of the center of mass
    sumofmasses = sprite1.mass + sprite2.mass
    sx = (sprite1.dx*sprite1.mass + sprite2.dx*sprite2.mass ) / sumofmass
    sy = (sprite1.dy*sprite1.mass + sprite2.dy*sprite2.mass ) / sumofmass
    # if we substract the velocity of the center of mass from the velocity of the sprite
    # we get its velocity relative to the center of mass
    # and relative to the center of mass, it looks just like the sprite is hitting a mirror.
    bdxs = sprite2.dx - sx
    bdys = sprite2.dy - sy
    cbdxs = sprite1.dx - sx
    cbdys = sprite1.dy - sy

    # dirx,diry is perpendicular to the mirror surface
    # we use the dot product to project to that direction
    distancesquare = dirx**2 + diry**2
    if distancesquare == 0:
        # no distance? this should not happen
        # just in case, we choose a random direction
        dirx = random.randint(0,11) - 5.5
        diry = random.randint(0,11) - 5.5
        distancesquare = dirx**2 + diry**2
    dp = bdxs*dirx + bdys*diry # scalar product
    dp /= distancesquare # divide by distance**2
    cdp = cbdxs*dirx + cbdys*diry
    cdp /= distancesquare 
    # dirx*dp, diry*dp is the projection of the velocity perpendicular to the virtual mirror
    # surface. Substract it twice to get the new direction
    # only collide if the sprites are moving towards each other: dp > 0
    if dp > 0:
        sprite2.dx -= 2*dirx*dp
        sprite2.dy -= 2*diry*dp
        sprite1.dx -= 2*dirx*dp
        sprite1.dy -= 2*diry*dp

class Text(pygame.sprite.Sprite):
    # a pygame Sprite to display text
    def __init__(self,msg='the Pygame Text Sprite',color=black):
        self.groups = allgroup
        self._layer = 1
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.newMsg(msg,color)
    def newMsg(self,msg,color=black):
        self.image = write(msg,color)
        self.rect = self.image.get_rect()
    def update(self,time):
        pass  # allgroup sprites need update method that accept time

class Lifebar(pygame.sprite.Sprite):
    # show a bar with the hitpoints of a Bird sprite with a given bossnumber
    # the Lifebar class can identify the boss(Bird sprite) with this codeline
    # Bird.birds[bossnumber]
    def __init__(self,boss):
        self.groups = allgroup
        self.boss = boss
        self._layer = self.boss._layer
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.oldpercent = 0
        self.paint()
    def paint(self):
        self.image = pygame.Surface( (self.boss.rect.width,7) )
        self.image.set_colorkey(black)
        pygame.draw.rect(self.image, greeen, (0,0,self.boss.rect.width,7),1)
        self.rect = self.image.get_rect()
    def update(self,time):
        self.percent = self.boss.hitpoints/self.boss.hitpointsfull
        if self.percent != self.oldpercent:
            self.paint() # important! boss.rect.width may have changed because of rotating
            pygame.draw.rect(self.image,black,(1,1,self.boss.rect.width-2,5)) # fill black
            # fill green
            health = self.boss.rect.width * self.percent
            pygame.draw.rect(self.image,green,(1,1,health,5),0)
            self.oldpercent = self.percent
            self.rect.centerx = self.boss.rect.centerx
            self.rect.centery = self.boss.rect.centery - self.boss.rect.height/2 - 10 
            if self.boss.hitpoints < 1: 
                self.kill() # kill the hitbar

class Bird(pygame.sprite.Sprite):
    # generic Bird class, to be called from Small Bird and Big Bird
    images = []
    birds = {} # a dictionary of all Birds, each Bird has its own number
    number = 0
    waittime = 1.0
    def __init__(self,layer=4, bigbird = False):
        self.groups = birdgroup, gravitygroup, allgroup
        self._layer = layer
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.pos = random.randint(50,screenwidth-50), random.randint(25,screenheight-25)
        self.image = Bird.images[2]
        self.image = Bird.images[0]
        self.hitpointsfull = 30.0
        self.hitpoints     = 30.0
        self.rect = self.image.get_rect()
        self.radius = max(self.rect.width, self.rect.height)/2.0
        self.dx,self.dy = 0,0  # not moving at the beginning
        self.waittime = Bird.waittime
        self.lifetime = 0.0
        self.waiting = True
        self.rect.center = -100,-100 # out of screen
        self.crashing = False
        self.frags = 25  # number of fragments if killed
        self.number = Bird.number
        Bird.number += 1
        Bird.birds[self.number] = self # store self into {birds} dict.
        print("my number %i Bird number %i and i am a %s " %(self.number,Bird.number,getClassName(self)))
        self.mass = 100.0
        self.angle = 0.0
        self.boostspeed = 10 # speed to fly upwards
        self.boostmax = 0.9  # max seconds of fuel for flying upwards
        self.boostmin = 0.4  # min seconds of fuel for flying upwards
        self.boosttime = 0.0 # time fuel remaining
        warpsould.play()
        for _ in range(8):
            BlueFragment(self.pos) 
    def kill(self):
        # a shower of red fragments, exploding
        for _ in range(self.frags):
            RedFragment(self.pos)
        pygame.sprite.Sprite.kill(self) # kill the actual Bird
    def speedCheck(self):
        if abs(self.dx) > 0:
            self.dx *= FRICTION # make slower
        if abs(self.dy) > 0:
            self.dy *= FRICTION # make slower
    def areaCheck(self):
        if not screenrect.contains(self.rect): # outside screen
            self.crashing = True
        # compare self.rect and screenrect
        if self.rect.right > screenrect.right: # outside right of screen
            self.centerx = screenrect.right - self.rect.width/2
            self.dx *= -0.5 # bouncing off but loosing speed
        if self.rect.left < screenrect.left:  # outside left of screen 
            self.centerx = screen.left + self.rect.width/2
            self.dx *= -0.5
        if self.rect.bottom > screenrect.bottom: # outside bottom of screen
            self.centery = screenbottom - self.rect.height/2
            # self.dy *= -1  bouncing off the ground
            # if reaching the bottom, the birds get a boost and fly upward to the sky
            # at the bottom, the bird 'refuel' a random amount of fuel(the boostime)
            self.dy = 0 # break at the bottom
            self.dx *= 0.3 # x speed is reduced at the ground
            self.boostime = self.bootmin + random.random() * (self.boostmax - self.boostmin)
        if self.rect.top < screenrect.top:
            self.centery = screentop + self.rect.height/2
            self.dy = 0 # stop when reaching the sky
            self.hitpoints -= 1 # reaching the sky cost 1 hitpoint
    def update(self,seconds):
        # make Bird only visible after waiting time
        self.lieftime += seconds
        if self.lifetime > self.waittime:
            self.waiting = False
        if self.waiting:
            self.rect.center = -100,-100
            return
        # the waiting time(Blue Fragments) is OVER
        if self.boostime > 0: 
            self.boostime -= seconds 
            self.ddx = -sin(self.angle*GRAD)
            self.ddy = -cos(self.angel*GRAD)
            Smoke(self.rect.center, -self.ddx, self.ddy)
        self.speedCheck()
        self.centerx += self.dx * seconds
        self.centery += self.dy * seconds
        self.areaCheck()
        # --- calculate actual image
        self.image = Bird.image[self.crashing + self.big]
        self.image0 = Bird.image[self.crashing + self.big] # 0 for not crashing, 1 for crashing
        # --- rotate into direction of movement -----
        self.angle = atan2(-self.dx,-self.dy)/pi * 180
        self.image = pygame.transform.rotozoom(self.image0, self.angle, 1.0)
        if self.hitpoints <= 0:
            self.kill()

class SmallBird(Bird):
    # A bird that get pushed around by shots; red fragments and other birds
    def __init__(self):
        self.big = 0
        Bird.__init__(self)
        Lifebar(self)
    def kill(self):
        crysound.play()
        Bird.kill(self)

class BigBird(Bird):
    # A Big bird controlled by the player
    def __init__(self):
        # small sprites have the value 0 -> important for Bird.image
        self.big = 2 
        Bird.__init__(self)
        self.hitpoints = 100.0
        self.hitpointsfull = 100.0
        self.image = Bird.images[2] # BIG bird image
        self.pos = screenwidth/2, screenheight/2
        self.rect = self.image.get_rect()
        self.angle = 0
        self.speed = 20.0
        self.rotatespeed = 1.0
        self.frags = 100
        Lifebar(self)
        self.cooldowntime = 0.08 # seconds
        self.cooldown = 0.0
        self.damage = 5 # how many damage on bullet inflict
        self.shots = 0
        self.radius = self.rect.width/2.0
        self.mass = 400.0
    def kill(self):
        bombsound.play()
        Bird.kill(self)
    def update(self,time):
        self.lifetime += seconds
        if self.lifetime > self.waittime:
            self.waiting = False
        if self.waiting:
            self.rect.center = -100,-100
            return
        # not waiting
        # calculate actual image
        self.image = Bird.images[self.crashing + self.big] # 0 for not crashing, 2 for big
        pressedkeys = pygame.key.get_pressed()
        self.ddx,self.ddy = 0.0, 0.0
        if pressedkeys[pygame.K_w]: # forward
            self.ddx = -sin(self.angel*GRAD)
            self.ddy = -cos(self.angel*GRAD)
            Smoke(self.rect.center, -self.ddx, -self.ddy)
        if pressedkeys[pygame.K_s]: # backward
            self.ddx = +sin(self.angel*GRAD)
            self.ddy = +cos(self.angel*GRAD)
            Smoke(self.rect.center, -self.ddx, -self.ddy)
        if pressedkeys[pygame.K_e]: # right side
            self.ddx = +cos(self.angel*GRAD)
            self.ddy = -sin(self.angel*GRAD)
            Smoke(self.rect.center, -self.ddx, -self.ddy)
        if pressedkeys[pygame.K_q]: # left side
            self.ddx = -cos(self.angel*GRAD)
            self.ddy = +sin(self.angel*GRAD)
            Smoke(self.rect.center, -self.ddx, -self.ddy)
        # ---- shoot -----------
        if self.cooldown > 0:
            self.cooldown -= time
        else:
            if pressedkeys[pygame.K_SPACE]: # shoot forward
                self.ddx = +sin(self.angel*GRAD)
                self.ddy = +cos(self.angel*GRAD)
                lasersound.play()
                self.shots += 1
                Bullet(self,-sin(self.angle*GRAD),-cos(self.angle*GRAD) )
            self.cooldown = self.cooldowntime
        # --- move ----------------
        self.dx += self.ddx * self.speed
        self.dy += self.ddy * self.speed
        self.centerx += self.dx * seconds
        self.centery += self.dy * seconds
        # check if Bird out of screen
        self.areaCheck()
        # ---- rotate -------------
        if pressedkyes[pygame.K_a]: # turn left, counter-clockwise
            self.angle += self.rotatespeed
        if pressedkyes[pygame.K_d]: # turn right, clockwise
            self.angle -= self.rotatespeed
        self.oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.oldcenter
        if self.hitpoints <= 0:
            self.kill()


class Fragment(pygame.sprite.Sprite):
    # implosion -> blue Fragment
    # explosion -> red Fragement, smoke(black), shots(purple)
    def __init__(self,pos,layer=9):
        self._layer = layer
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.pos = 0,0
        self.maxspeed = FRAGMENTMAXSPEED
    def init2(self):
        self.image = pygame.Surface((10,10))
        self.image.set_colorkey(black)
        r = random.randint(2,5)
        pygame.draw.circle(self.image,self.color,(5,5),r)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.time = 0.0
    def update(self,seconds):
        self.time += seconds
        if self.time > self.lifetime:
            self.kill()
        self.rect.centerx += self.dx * seconds
        self.rect.centery += self.dy * seconds

class RedFragment(Fragment):
    # when killed, explode outward
    def __init__(self,pos):
        self.groups = fragmentgroup,gravitygroup,allgroup
        Fragment.__init__(self,pos)
        # red only
        self.color = randomred
        self.rect.center = pos
        self.dx = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
        self.dy = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
        self.lifetime = 1 + 3*random.random()
        self.init2() 
        self.mass = 48.0
class BlueFragment(Fragment):
    def __init__(self,pos):
        self.groups = allgroup
        Fragment.__init__(self,pos)
        self.target = pos
        self.color = randomblue
        self.side = random.randint(1,4)
        if self.side == 1: # left side
            self.rect.centerx = 0
            self.rect.centery = random.randint(0,screenheight)
        if self.side == 2: # top side
            self.rect.centerx = random.randint(0,screenwidth)
            self.rect.centery = 0
        if self.side == 3: # right side
            self.rect.centerx = screenwidth
            self.rect.centery = random.randint(0,screenheight)
        if self.side == 4: # bottom side
            self.rect.centerx = random.randint(0,screenwidth)
            self.rect.centery = screenheight
        # calculate flytime for one seconds.. Bird waittime should be 1.0
        self.dx = (self.target[0] - self.rect.centerx)/Bird.waittime
        self.dy = (self.target[1] - self.rect.centery)/Bird.waittime
        self.lifetime = Bird.waittime + random.random()/2.0
        self.init2()

class Smoke(Fragment):
    # black exhaust indicating that the BigBird sprite is moved by
    # the player. Exhaust direction is inverse of players movement direction
    def __init__(self,pos,dx,dy):
        self.color = randomdark
        self.groups = allgroup
        Fragment.__init__(self,pos,3) # startpos = pos, layer=3
        self.rect.center = pos
        self.lifetime = 1 + 2*random.random()
        Fragment.init2(self)
        self.smokespeed = 120.0 # how fast the smoke leaves the Bird
        self.smokearc = 0.3     # 0: think smoke, 1 = 180 degrees
        arc = self.smokespeed * self.smokearc
        self.dx = dx * self.smokespeed + 2*arc*random.random() - arc
        self.dy = dy * self.smokespeed + 2*arc*random.random() - arc

class Bullet(Fragment):
    def __init__(self,boss,dx,dy):
        self.color = pink1
        self.boss = boss
        self.groups = bulletgroup,gravitygroup,allgroup
        self.image = pygame.Surface( (4,20) )
        self.image.set_colorkey(black)
        pygame.draw.rect(self.image, self.color,(0,0,4,20) )
        pygame.draw.rect(self.image, (10,0,0),(0,0,4,4)) # point
        self.image = self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = self.boss.rect.center
        self.time = 0.0
        self.bulletspeed = 250.0 # pixel per second
        self.bulletarc = 0.05
        self.dx = dx * self.bulletspeed + 2*arc*random.random() - arc
        self.dy = dy * self.bulletspeed + 2*arc*random.random() - arc
        self.mass = 25.0
        Fragment.__init__(self,self.rect.center,3) # startpos = pos, layer=3
    def update(self.time):
        Fragment.update(self,time)
        # --- rotate into direction of movement
        self.angle = atan2(-self.dx,-self.dy)/pi * 180
        self.image = pygame.transfrom.rotozoom(self.image0, self.angle, 1.0)

# ----------------- background artwork -------------  
background = pygame.Surface((screen.get_width(), screen.get_height()))
background.fill((255,255,255))     # fill white
background.blit(write("navigate with w,a,s,d and q and e "),(50,40))
background.blit(write("press SPACE to fire bullets"),(50,70))
background.blit(write("press g to toggle gravity"), (50, 100))
background.blit(write("Press ESC to quit "), (50,130))
background = background.convert()  # jpg can not have transparency
screen.blit(background, (0,0))     # blit background on screen (overwriting all)
#-----------------define sprite groups------------------------
birdgroup = pygame.sprite.Group() 
bulletgroup = pygame.sprite.Group()
fragmentgroup = pygame.sprite.Group()
gravitygroup = pygame.sprite.Group()
# only the allgroup draws the sprite, so i use LayeredUpdates() instead Group()
allgroup = pygame.sprite.LayeredUpdates() # more sophisticated, can draw sprites in layers 

#-------------loading files from data subdirectory -------------------------------
Bird.image.append(pygame.image.load(os.path.join(folder,"babytux.png")))
Bird.image.append(pygame.image.load(os.path.join(folder,"babytux_neg.png")))
Bird.image.append(pygame.transform.scale2x(Bird.image[0])) # copy of first image, big bird
Bird.image.append(pygame.transform.scale2x(Bird.image[1])) # copy of blue image, big bird
Bird.image[0] = Bird.image[0].convert_alpha()
Bird.image[1] = Bird.image[1].convert_alpha()
Bird.image[2] = Bird.image[2].convert_alpha()
Bird.image[3] = Bird.image[3].convert_alpha()






