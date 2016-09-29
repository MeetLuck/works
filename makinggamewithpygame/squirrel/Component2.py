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
class Grass:
    grassImages = []
    for i in range(1,5):
        grassImages.append(pygame.image.load('grass%s.png' %i))
    def __init__(self,camerax,cameray):
        self.img = random.choice(self.grassImages)
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x,self.y = getRandomOffCameraPos(camerax,cameray,self.width,self.height)
        self.rect = pygame.Rect( (self.x,self.y,self.width,self.height) )
    def draw(self,surface,camerax,cameray):
        grect = pygame.Rect( (self.x-camerax, self.y-cameray, self.width,self.height) ) 
        surface.blit(self.img, grect)

class Squirrel:
    def __init__(self):
        self.surface = pygame.transform.scale( l_squir_img,(startsize,startsize) )
class Player(Squirrel):
    def __init__(self):
        self.surface = pygame.transform.scale( l_squir_img,(startsize,startsize) )
        self.facing = left
        self.size = startsize
        self.bounce = 0
        self.x,self.y = winwidth/2,winheight/2
        self.centerX,self.centerY = self.x/2+self.size/2, self.y/2+self.size/2
        self.health = maxhealth
    def move(self,moveX=0,moveY=0):
        self.x += moveX
        self.y += moveY
        if moveX or moveY or self.bounce!=0:
            self.bounce += 1
        if self.bounce > bouncerate:
            self.bounce = 0
        if moveX == -moverate and self.facing == right: # change player image
                self.surface = pygame.transform.scale(l_squir_img, (self.size,self.size))
                self.facing = left
        if moveX == +moverate and self.facing == left: # change player image
            self.surface = pygame.transform.scale(r_squir_img, (self.size,self.size))
            self.facing = right

    def draw(self,surface,camerax,cameray):
        self.rect = pygame.Rect(
                    (self.x-camerax,
                     self.y-cameray-getBounceAmount(self.bounce, bouncerate, bounceheight),
                     self.size,
                     self.size) )
        surface.blit( self.surface, self.rect )
class OtherSquirrel(Squirrel):
    def __init__(self,camerax,cameray):
        generalsize = random.randint(5,25)
        multiplier = random.randint(1,3)
        self.width =  (generalsize + random.randint(0,10) ) * multiplier
        self.height = (generalsize + random.randint(0,10) ) * multiplier
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
