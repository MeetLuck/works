# 017 turning and physics.py
# move the BIG bird around with W,A,S,D and Q and E
# fire with SPACE, toggle gravity with G

from constants017 import *

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
    def __init__(self,boss):
        self.groups = allgroup
        self.boss = boss
        self._layer = self.boss._layer
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.width = self.boss.rect.width
        self.paint()
        self.move()
    def paint(self):
        self.width = self.boss.rect.width
        self.image = pygame.Surface( (self.width,7) )
        self.rect = self.image.get_rect()
        self.image.set_colorkey(black)
        pygame.draw.rect(self.image, green, (0,0,self.width,7),1)
        self.percent = self.boss.hitpoints/self.boss.hitpointsfull
        health = self.boss.rect.width * self.percent   #health = self.boss.rect.width * self.percent
        pygame.draw.rect(self.image,red, (1,1,self.width-2,5))  # fill red
        pygame.draw.rect(self.image,green,(1,1,health,5))     # fill green
    def move(self):
        self.rect.centerx = self.boss.rect.centerx
        self.rect.centery = self.boss.rect.centery - self.boss.rect.height/2 - 10 
    def update(self,seconds):
        self.paint() # important! boss.rect.width may have changed because of rotating
        self.move()
        if self.boss.hitpoints < 1: 
            self.kill() # kill the hitbar

class Bird(pygame.sprite.Sprite):
    # generic Bird class, to be called from Small Bird and Big Bird
    images = []
    birds = {} # a dictionary of all Birds, each Bird has its own number
    number = 0
    waittime = 1.0 #/fps/10.0 
    def __init__(self,layer=4, bigbird = False):
        self.groups = birdgroup, gravitygroup, allgroup
        self._layer = layer
        pygame.sprite.Sprite.__init__(self,self.groups)
        # setup image, speed, constants
        self.setConstants()
        self.setImage()
        # store self into birds={} dict.
        self.number = Bird.number
        Bird.number += 1
        Bird.birds[self.number] = self 
        print("my number %i Bird number %i and i am a %s " %(self.number,Bird.number,getClassName(self)))
        warpsound.play()
    def setImage(self):
        self.image = Bird.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = -100,-100 # out of screen
        self.radius = max(self.rect.width, self.rect.height)/2.0
    def setConstants(self):
        self.dx,self.dy = 0.0, 0.0  # not moving at the beginning
        self.hitpointsfull = 30.0
        self.hitpoints     = 30.0
        self.waittime = Bird.waittime
        self.lifetime = 0.0
        self.waiting = True
        self.crashing = False
        self.frags = 25  # number of fragments if killed
        self.mass = 100.0
        self.angle = 0.0
        self.boostspeed = 10.0 # speed to fly upwards
        self.boostmax = 0.9  # max seconds of fuel for flying upwards
        self.boostmin = 0.4  # min seconds of fuel for flying upwards
        self.boostime = 0.0 # time fuel remaining
    def isInsideScreen(self):
        return screenrect.contains(self.rect)
    def checkArea(self):
        if self.isInsideScreen(): return
        # bird OUT OF screen
        self.crashing = True
        # compare self.rect and screenrect
        if self.rect.right > screenrect.right: # outside right of screen
            self.rect.centerx = screenrect.right - self.rect.width/2
            self.dx *= -0.5 # bouncing off but loosing speed
        if self.rect.left < screenrect.left:  # outside left of screen 
            self.rect.centerx = screenrect.left + self.rect.width/2
            self.dx *= -0.5
        if self.rect.bottom > screenrect.bottom: # outside bottom of screen
            self.rect.centery = screenrect.bottom - self.rect.height/2
            self.dy = 0 # break at the bottom
            self.dx *= 0.3 # x speed is reduced at the ground
            self.boostime = self.boostmin + random.random() * (self.boostmax - self.boostmin)
        if self.rect.top < screenrect.top:
            self.rect.centery = screenrect.top + self.rect.height/2
            self.dy = 0 # stop when reaching the sky
            self.hitpoints -= 1 # reaching the sky cost 1 hitpoint
    def move(self,seconds):
        self.rect.centerx += self.dx * seconds
        self.rect.centery += self.dy * seconds
    def kill(self):
        for _ in range(self.frags): # a shower of red fragments, exploding
            RedFragment(self.rect.center)
        pygame.sprite.Sprite.kill(self) # kill the actual Bird
    def checkSpeed(self):
        if abs(self.dx) > 0: self.dx *= FRICTION # make slower
        if abs(self.dy) > 0: self.dy *= FRICTION # make slower
    def isWaiting(self,seconds):
        # make Bird only visible after waiting time
        self.lifetime += seconds
        if self.lifetime < self.waittime:
            return True
        else: #if self.lifetime > self.waittime:
            if self.waiting: # True at creating instance
                self.rect.center = random.randint(50,screenwidth-50), random.randint(25,screenheight-25)
                self.waiting = not self.waiting
            return False

    def update(self,seconds):
        if self.isWaiting(seconds): return 
        # not isWaiting
        if self.boostime > 0: 
            self.boostime += -seconds 
            self.dy +=  -self.boostspeed # upward is negative y !
            self.ddx = -sin(self.angle*GRAD)
            self.ddy = -cos(self.angle*GRAD)

        self.checkSpeed()
        self.move(seconds)
        self.checkArea()

        # --- calculate actual image
        self.image = Bird.images[self.crashing + self.big]
        self.image0 = Bird.images[self.crashing + self.big] # 0 for not crashing, 1 for crashing
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
        self.image = Bird.images[2] # BIG bird image
        self.rect = self.image.get_rect()
        self.pos = screenwidth/2, screenheight/2
        self.angle = 0
        self.hitpoints = 100.0
        self.hitpointsfull = 100.0
        self.speed = 20.0
        self.rotatespeed = 1.0
        self.frags = 100
        self.cooldowntime = 0.008 # seconds
        self.cooldown = 0.0
        self.damage = 5 # how many damage on bullet inflict
        self.shots = 0
        self.radius = self.rect.width/2.0
        self.mass = 400.0
        Lifebar(self)
    def kill(self):
        bombsound.play()
        Bird.kill(self)
    def isWaiting(self,seconds):
        # make Bird only visible after waiting time
        self.lifetime += seconds
        if self.lifetime < self.waittime:
            return True
        else: #if self.lifetime > self.waittime:
            if self.waiting: # True at creating instance
                self.rect.center = screenwidth/2, screenheight/2 
                self.waiting = not self.waiting
            return False
    def update(self,seconds):
        if self.isWaiting(seconds): return
        # not waiting,  calculate actual image
        self.image = Bird.images[self.crashing + self.big] # 0 for not crashing, 2 for big
        pressedkeys = pygame.key.get_pressed()
        self.ddx,self.ddy = 0.0, 0.0
        if pressedkeys[pygame.K_w]: # forward
            self.ddx = -sin(self.angle*GRAD)
            self.ddy = -cos(self.angle*GRAD)
        if pressedkeys[pygame.K_s]: # backward
            self.ddx = +sin(self.angle*GRAD)
            self.ddy = +cos(self.angle*GRAD)
        if pressedkeys[pygame.K_l]: # right side
            self.ddx = +cos(self.angle*GRAD)
            self.ddy = -sin(self.angle*GRAD)
        if pressedkeys[pygame.K_h]: # left side
            self.ddx = -cos(self.angle*GRAD)
            self.ddy = +sin(self.angle*GRAD)
        # ---- shoot -----------
        if self.cooldown > 0:
            self.cooldown += -seconds
        else:
            if pressedkeys[pygame.K_SPACE]: # shoot forward
                self.ddx = sin(self.angle*GRAD)
                self.ddy = cos(self.angle*GRAD)
                lasersound.play()
                self.shots += 1
                Bullet(self,-sin(self.angle*GRAD),-cos(self.angle*GRAD) )
            self.cooldown = self.cooldowntime
        # --- move ----------------
        self.dx += self.ddx * self.speed
        self.dy += self.ddy * self.speed
        self.move(seconds)
        # check if Bird out of screen
        self.checkArea()
        # ---- rotate -------------
        if pressedkeys[pygame.K_a]: # turn left, counter-clockwise
            self.angle += self.rotatespeed
        if pressedkeys[pygame.K_d]: # turn right, clockwise
            self.angle -= self.rotatespeed
        self.oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.oldcenter
        #print self.rect.center
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
        self.init2() 
        self.rect.center = pos
        self.dx = random.randint(-self.maxspeed,self.maxspeed)
        self.dy = random.randint(-self.maxspeed,self.maxspeed)
        self.lifetime = 1 + 3*random.random()
        self.mass = 48.0

class Bullet(Fragment):
    def __init__(self,boss,dx,dy):
        self.color = pink1
        self.boss = boss
        self.groups = bulletgroup,gravitygroup,allgroup
        self.lifetime = 5.0
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
        arc = self.bulletspeed * self.bulletarc
        self.dx = dx * self.bulletspeed + 2*arc*random.random() - arc
        self.dy = dy * self.bulletspeed + 2*arc*random.random() - arc
        self.mass = 25.0
        Fragment.__init__(self,self.rect.center,3) # startpos = pos, layer=3
    def update(self,time):
        Fragment.update(self,time)
        # --- rotate into direction of movement
        self.angle = atan2(-self.dx,-self.dy)/pi * 180
        self.image = pygame.transform.rotozoom(self.image0, self.angle, 1.0)


def main():
    #-------------loading files from data subdirectory -------------------------------
    Bird.images.append(pygame.image.load(os.path.join(folder,"babytux.png")))
    Bird.images.append(pygame.image.load(os.path.join(folder,"babytux_neg.png")))
    Bird.images.append(pygame.transform.scale2x(Bird.images[0])) # copy of first image, big bird
    Bird.images.append(pygame.transform.scale2x(Bird.images[1])) # copy of blue image, big bird
    for image in Bird.images:
        image = image.convert_alpha()
#   for i in range(3):
#       Bird.images[i] = Bird.images[i].convert_alpha()

    screentext = Text()
    minbirds = 7 # amount = 7 # how many small bird should be on the screen
    player = BigBird()
    overtime = 15 # to admire the explosion of player before game ends
    gameover = False
    hits = 0 # how often the player was hitting a small birds
    quota = 0 # hit/miss quota
    gametime = 60  # seconds how long TO PLAY game 
    playtime = 0   # seconds how long the game PLAYED
    gravity = True
    mainloop = True

    while mainloop:
        seconds = clock.tick(fps)/1000.0
        playtime += seconds
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                mainloop = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_x:     player.hitpoints += -1
                elif e.key == pygame.K_y:   player.hitpoints += 1
                elif e.key == pygame.K_g:   gravity = not gravity
                elif e.key == pygame.K_p:   printSpritelist()

        if player.shots > 0: quota = hits/player.shots * 100.0
        pygame.display.set_caption("fps: %.2f gravity: %s hits:%i shots:%i quota:%.2f%%"  % (clock.get_fps(), 
                                     gravity, hits, player.shots, quota))
        # ------ collision detection --------
        for bird in birdgroup:  # test if a bird collides with another bird
            bird.crashing = False # make bird NOT blue

            if bird.waiting: continue # do not check birds outside the screen
            # check the Bird.number to make sure the bird is not crashing with himself
            # ---------- bird collide with another bird ------------------------
            crashgroup = pygame.sprite.spritecollide(bird, birdgroup, False )
            for crashbird in crashgroup:  # test bird with other bird collision
                if crashbird.number == bird.number: continue  # avoid checking twice
                bird.crashing = True # make bird blue
                crashbird.crashing = True # make other bird blue
                if not (bird.waiting or crashbird.waiting):
                    elastic_collision(crashbird, bird) # change dx and dy of both birds
                    #elasticCollision(crashbird, bird) # change dx and dy of both birds

            # ------------- bird collide with bullet -----------------------
            crashgroup = pygame.sprite.spritecollide(bird, bulletgroup, False)
            for bullet in crashgroup:  # test for collision with bullet
                if bullet.boss.number != bird.number:
                    hitsound.play()
                    hits +=1
                    bird.hitpoints += -bullet.boss.damage
                    factor =  (bullet.mass / bird.mass)
                    bird.dx += bullet.dx * factor
                    bird.dy += bullet.dy * factor
                    bullet.kill()
                    
            crashgroup = pygame.sprite.spritecollide(bird, fragmentgroup, False)
            for frag in crashgroup: # test for red fragments
                bird.hitpoints -=1
                factor =  frag.mass / bird.mass
                bird.dx += frag.dx * factor
                bird.dy += frag.dy * factor
                frag.kill()
                    
        if gravity: # ---- gravity check ---
            for thing in gravitygroup:
                thing.dy += FORCEOFGRAVITY # gravity suck down all kind of things
                    
        if len(birdgroup) < minbirds: # create enough SmallBirds
            for _ in range(random.randint(1,3)):
                print 'add small birds'
                SmallBird()
        
        # ------game Over ? -------------
        if (player.hitpoints < 1 or playtime > gametime) and not gameover:
            gameover = True # do those things once when the game ends
            screentext.newMsg("Game Over. hits/shots: %i/%i quota: %.2f%%" % (hits, player.shots, quota), (255,0,0))
            player.hitpoints = 0 # kill the player into a big explosion
        if gameover: # overtime to watch score, explosion etc
            overtime -= seconds
            if overtime < 0:
                mainloop = False
        else: # not yet gameOver
            screentext.newMsg("Time left: %.2f" % (gametime - playtime))
        
        # ----------- clear, draw , update, flip -----------------  
        allgroup.clear(screen, background)
        allgroup.update(seconds)
        allgroup.draw(screen)           
        pygame.display.flip()         

if __name__ == "__main__":
    main()
