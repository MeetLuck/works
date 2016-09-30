from constants import *

def getBounceAmount(currentBounce,bouncerate,bounceHeight):
    return int( math.sin( (math.pi/float(bouncerate)) * currentBounce ) * bounceHeight )
def getRandomVelocity():
    speed = random.randint( squirrelminspeed,squirrelmaxspeed )
    if random.randint(0,1)==0: return speed
    else: return -speed
def getRandomOffCameraPos(camerax,cameray,objWidth,objHeight):
    # create a Rect of the camera view
    cameraRect = pygame.Rect( camerax, cameray, winwidth, winheight)
    while True:
        x = random.randint(camerax - winwidth, camerax+2*winwidth)
        y = random.randint(cameray - winheight, cameray+2*winheight)
        objRect = pygame.Rect(x,y,objWidth,objHeight)
        if not objRect.colliderect(cameraRect):
            return x,y
class Direction:
    def __init__(self):
        self.left = self.right = self.up = self.down = False
class Grass:
    def __init__(self,camerax,cameray):
        grassImages = []
        for i in range(1,5):
            grassImages.append(pygame.image.load('grass%s.png' %i))
        self.img = random.choice(grassImages)
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x,self.y = getRandomOffCameraPos(camerax,cameray,self.width,self.height)
        self.rect = pygame.Rect( (self.x,self.y,self.width,self.height) )
    def draw(self,surface,camerax=0,cameray=0):
        grect = pygame.Rect( (self.x-camerax, self.y-cameray, self.width,self.height) ) 
        surface.blit(self.img, grect)

class Squirrel:
    def draw(self,surface,camerax=0,cameray=0):
        pyrect = pygame.Rect(
                    (self.x-camerax,
                     self.y-cameray-getBounceAmount(self.bounce, bouncerate, bounceheight),
                     self.width,
                     self.height) )
        surface.blit( self.surface, pyrect )
    def getRect(self):
        return pygame.Rect( (self.x,self.y,self.width,self.height) )
    def getArea(self):
        return self.width * self.height

class Player(Squirrel):
    def __init__(self):
        #self.size = startsize
        self.x,self.y = winwidth/2,winheight/2
        self.width,self.height = startsize,startsize
        self.facing = left
        self.bounce = 0
        self.health = maxhealth +20
        self.surface = pygame.transform.scale( l_player_img,(self.width,self.height) )
        self.setCenter()
        self.invulnerable = False
        self.invulnerableStartTime = 0
    def setCenter(self):
        self.centerX,self.centerY = self.x+self.width/2, self.y+self.height/2
    def draw(self,surface,camerax=0,cameray=0):
        #print self.x,camerax,self.centerX
        Squirrel.draw(self,surface,camerax,cameray)
    def move(self,direction):
        if direction.left:  self.x += -moverate
        if direction.right: self.x += +moverate
        if direction.up:    self.y += -moverate
        if direction.down:  self.y += +moverate
        if direction.left or direction.right or direction.up or direction.down or self.bounce != 0:
           self.bounce += 1
        if self.bounce > bouncerate:
            self.bounce = 0
        if direction.left and self.facing == right:
           self.surface = pygame.transform.scale(l_player_img, (self.width,self.height))
           self.facing = left
        if direction.right and self.facing == left:
           self.surface = pygame.transform.scale(r_player_img, (self.width,self.height))
           self.facing = right
        self.setCenter()
    def isLargerThan(self,other):
         return self.getArea() >= other.getArea()
    def makeLarge(self,other):
        self.width += int(1 + other.getArea()**0.2)
        self.height = self.width
        print 'size: ',self.width, 'enermy: ', int(other.getArea())
        if self.facing == left:
            self.surface = pygame.transform.scale(l_player_img,(self.width,self.height))
        elif self.facing == right:
            self.surface = pygame.transform.scale(r_player_img,(self.width,self.height))
    def isCollideWith(self,other):
        #return self.surface.get_rect().colliderect(other.surface.get_rect())
        return self.getRect().colliderect( other.getRect() )
    def setDamage(self):
        if not self.invulnerable:
            self.invulnerable = True
            self.invulnerableStartTime = time.time()
            self.health += -1


class otherSquirrel(Squirrel):
    def __init__(self,camerax,cameray):
        generalsize = random.randint(5,25) # 5,25
        multiplier = random.randint(1,3)
        self.width =  (generalsize + random.randint(0,5) ) * multiplier
        self.height = (generalsize + random.randint(0,5) ) * multiplier
        self.x,self.y = getRandomOffCameraPos(camerax,cameray,self.width,self.height)
        self.movex = getRandomVelocity()
        self.movey = getRandomVelocity()
        if self.movex < 0: # facing LEFT
            self.surface = pygame.transform.scale( l_squir_img,(self.width,self.height) )
        else:
            self.surface = pygame.transform.scale( r_squir_img,(self.width,self.height) )
        self.bounce = 0
        self.bouncerate = random.randint(10,18)
        self.bounceheight = random.randint(10,50)
    def move(self):
        # move the squirrel, and adjust for their bounce
        self.x += self.movex
        self.y += self.movey
        self.bounce += 1
        if self.bounce > self.bouncerate:
            self.bounce = 0 # reset bounce amount
        # random chance they change direction
        if random.randint(0,99) < dirchangefreq:
            self.movex = getRandomVelocity()
            self.movey = getRandomVelocity()
            if self.movex > 0: # faces right
                self.surface = pygame.transform.scale(r_squir_img, (self.width, self.height))
            else: # faces left
                self.surface = pygame.transform.scale(l_squir_img, (self.width, self.height))
