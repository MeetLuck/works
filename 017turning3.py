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
        # store self into birds={} dict.
        self.number = Bird.number
        Bird.number += 1
        Bird.birds[self.number] = self 
        print("my number %i Bird number %i and i am a %s " %(self.number,Bird.number,getClassName(self)))
        warpsound.play()
    def isInsideScreen(self):
        return screenrect.contains(self.rect)
    def checkArea(self):
        if self.isInsideScreen(): return
        # bird OUT OF screen
        self.crashing = False
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
            #self.boostime = self.boostmin + random.random() * (self.boostmax - self.boostmin)
        if self.rect.top < screenrect.top:
            self.rect.centery = screenrect.top + self.rect.height/2
            self.dy = 0 # stop when reaching the sky
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

class BigBird(Bird):
    # A Big bird controlled by the player
    def __init__(self):
        # small sprites have the value 0 -> important for Bird.image
        self.big = 2 
        Bird.__init__(self)
        self.pos = screenwidth/2, screenheight/2
        self.setupImage()
        self.setConstants()
    def setupImage(self):
        self.image = Bird.images[2] # BIG bird image
        self.rect = self.image.get_rect()
        self.radius = self.rect.width/2.0
        #pygame.draw.rect(self.image,darkgreen,self.rect,2)
        rect1 = self.rect
        rect2 = 0,0,self.rect.width,self.rect.height/2
        rect3 = self.rect.midtop,(self.rect.width,self.rect.height)
        pygame.draw.rect(self.image,red,rect1,2)
        pygame.draw.rect(self.image,red,rect2,1)
        pygame.draw.rect(self.image,red,rect3,1)
        self.rect.center = -100,-100 # out of screen
    def setConstants(self):
        self.dx,self.dy = 0.0, 0.0  # not moving at the beginning
        self.waittime = Bird.waittime
        self.lifetime = 0.0
        self.waiting = True
        self.crashing = False
        self.angle = 0.0
        self.speed = 10.0
        self.rotatespeed = 1.0
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
        #self.image = Bird.images[self.crashing + self.big] # 0 for not crashing, 2 for big
        self.image = Bird.images[2]
        pressedkeys = pygame.key.get_pressed()
        self.ddx,self.ddy = 0.0, 0.0
        if pressedkeys[pygame.K_k]: # forward
            self.ddx = -sin(self.angle*GRAD)
            self.ddy = -cos(self.angle*GRAD)
        if pressedkeys[pygame.K_j]: # backward
            self.ddx = +sin(self.angle*GRAD)
            self.ddy = +cos(self.angle*GRAD)
        if pressedkeys[pygame.K_l]: # right side
            self.ddx = +cos(self.angle*GRAD)
            self.ddy = -sin(self.angle*GRAD)
        if pressedkeys[pygame.K_h]: # left side
            self.ddx = -cos(self.angle*GRAD)
            self.ddy = +sin(self.angle*GRAD)
        # --- move ----------------
        self.dx += self.ddx * self.speed
        self.dy += self.ddy * self.speed
        self.move(seconds)
        # check if Bird out of screen
        self.checkArea()
        self.oldcenter = self.rect.center
        # ---- rotate -------------
        if pressedkeys[pygame.K_a]: # turn left, counter-clockwise
            self.angle += +self.rotatespeed
        if pressedkeys[pygame.K_d]: # turn right, clockwise
            self.angle += -self.rotatespeed
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.oldcenter
        #print self.rect.center

def main():
    #-------------loading files from data subdirectory -------------------------------
    Bird.images.append(pygame.image.load(os.path.join(folder,"babytux.png")))
    Bird.images.append(pygame.image.load(os.path.join(folder,"babytux_neg.png")))
    Bird.images.append(pygame.transform.scale2x(Bird.images[0])) # copy of first image, big bird
    Bird.images.append(pygame.transform.scale2x(Bird.images[1])) # copy of blue image, big bird
#   for image in Bird.images:
#       image = image.convert_alpha()
    for i in range(3):
        Bird.images[i] = Bird.images[i].convert_alpha()
    screentext = Text()
    player = BigBird()
    overtime = 15 # to admire the explosion of player before game ends
    gravity = True
    mainloop = True

    while mainloop:
        seconds = clock.tick(fps)/1000.0
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                mainloop = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_g:     gravity = not gravity
                elif e.key == pygame.K_p:   printSpritelist()
        pygame.display.set_caption("fps: %.2f  gravity: %s  angle: %d center:%s"  % (clock.get_fps(), gravity, player.angle,player.rect.center) ) 
        if gravity: # ---- gravity check ---
            for thing in gravitygroup:
                thing.dy += FORCEOFGRAVITY # gravity suck down all kind of things
        # ----------- clear, draw , update, flip -----------------  
        allgroup.clear(screen, background)
        allgroup.update(seconds)
        allgroup.draw(screen)           
        pygame.display.flip()         

def printSpritelist():
    print("=========================")
    print( "-----Spritelist---------")
    spritelist = allgroup.get_sprites_at(pygame.mouse.get_pos())
    for sprite in spritelist:
        print(sprite, "Layer:",allgroup.get_layer_of_sprite(sprite))
    print("------------------------")

if __name__ == "__main__":
    main()





