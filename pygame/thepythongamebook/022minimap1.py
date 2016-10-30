''' 020 shooting from tank.py
    demo of 2 tanks shooting bullets at the end of it's cannon
    and shooting tracers at the end of it's bow Machine Gun
    and from the turret-machine gun (co-axial with main gun)
    '''
from constants022 import *
import copy

class Tank(pygame.sprite.Sprite):
    size = 100
    recoiltime = 0.5 #0.75 # how many seconds the cannon is busy after firing one time
    MGrecoiltime = 0.1 # how many seconds the bow(machine gun) is idel
    turretTurnSpeed = 1
    tankTurnSpeed = 1 # degrees
    movespeed = 25.0 * 2
    book = {} # a book of tanks to store all tanks
    number = 0
    color = ((200,200,0),(0,0,200) )
    msg = ['wasd LCTRL, ijkl','Keypad: 4852, ENTER, cursor']

    def __init__(self,startpos=(150,150),angle=0):
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.color = Tank.color[self.number]
        self.number = Tank.number
        Tank.number += 1
        Tank.book[self.number] = self
        self.setKeys()
        self.makeTank(startpos,angle)
        self.turret = Turret(self) # create a Turret for this thank
        self.msg =  "player%i: ammo: %i/%i keys: %s" % (self.number+1, self.ammo, self.MGammo, Tank.msg[self.number])
        Text((screenwidth/2, 30+20*self.number), self.msg) # create status line text sprite

    def makeTank(self,startpos,angle):
        width,height = Tank.size,Tank.size
        image,MGcenter,Vc = drawTank(width,height,self.color)
        # rotate Tank for the given angle
        self.tankAngle = angle
        self.image0 = image.convert_alpha()
        self.rect = self.image0.get_rect()
        image = pygame.transform.rotate(self.image0,self.tankAngle)
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect(center=self.rect.center)
        # position Vector Vp
        self.Vp = Vector(startpos)
        self.rect.center = tuple(self.Vp)
        self.MGcenter = MGcenter
        self.Vc = Vc
        self.movespeed = Tank.movespeed
        # tank constants
        self.tankTurnSpeed = Tank.tankTurnSpeed
        self.tankturndirection = 0
        self.ammo = 3000 # main gun
        self.MGammo = 500000 # machine gun
        # turret constants
        self.cooltime = 0.0  # cannon
        self.MGcooltime = 0.0 # Machine Gun
        self.turndirection = 0
        self.turretAngle = angle
        self.turretTurnSpeed = Tank.turretTurnSpeed

    def setKeys(self):
        self.forwardkey     = forwardkey[self.number]
        self.backwardkey    = backwardkey[self.number]
        self.tankLeftkey    = tankLeftkey[self.number]
        self.tankRightkey   = tankRightkey[self.number]
        self.firekey        = firekey[self.number]
        self.MGfirekey      = MGfirekey[self.number]
        self.turretLeftkey  = turretLeftkey[self.number]
        self.turretRightkey = turretRightkey[self.number]

    def rotateTurret(self,pressedkeys):
        doRotateTurret = pressedkeys[self.turretLeftkey] or pressedkeys[self.turretRightkey]
        if not doRotateTurret: return
        self.turndirection = 0 # left/right turret rotation
        if pressedkeys[self.turretLeftkey]:  self.turndirection += 1
        if pressedkeys[self.turretRightkey]: self.turndirection -= 1
        self.turretAngle += self.turndirection * self.turretTurnSpeed  #* seconds

    def rotateTank(self,pressedkeys):
        doRotateTank = pressedkeys[self.tankLeftkey] or pressedkeys[self.tankRightkey]
        if not doRotateTank: return
        self.tankturndirection = 0 # reset left/right rotation
        if pressedkeys[self.tankLeftkey]:  self.tankturndirection += 1
        if pressedkeys[self.tankRightkey]: self.tankturndirection -= 1
        deltaAngle = self.tankturndirection * self.tankTurnSpeed # * seconds
        self.tankAngle   += deltaAngle
        self.turretAngle += deltaAngle # turret autorotate if tank is rotating
        self.image = pygame.transform.rotate(self.image0, self.tankAngle)
        self.rect = self.image.get_rect(center = self.rect.center) #center = oldcenter = self.rect.center

    def autotarget(self,targetNo=0):
        delta = Tank.book[targetNo].Vp - self.Vp
        targetAngle = atan2(-delta.y,delta.x)/pi * 180
        diffAngle = targetAngle - self.turretAngle
        if diffAngle < 0: diffAngle += 360
        diffAngle = diffAngle % 360
        if abs(diffAngle) == 0: self.turndirection = 0
        elif diffAngle < 180:   self.turndirection = +1/4.0
        elif diffAngle > 180:   self.turndirection = -1/4.0
        self.turretAngle += self.turndirection * self.turretTurnSpeed
        #print targetAngle, self.turretAngle, diffAngle
        #print self.turretAngle 

    def reduceCooltime(self,seconds): # reloading, firestatus
        self.cooltime     -= seconds
        self.MGcooltime   -= seconds

    def fireCannon(self,pressedkeys):
        doFireCannon = self.cooltime <= 0 and self.ammo >0 and pressedkeys[self.firekey]
        if not doFireCannon: return
        # fire Cannon: cooltime == 0
        Bullet(self)
        cannonsound.play()
        self.cooltime = Tank.recoiltime # seconds until tank can fire again
        self.ammo -= 1
        self.msg =  "player%i: ammo: %i/%i keys: %s" % (self.number+1, self.ammo, self.MGammo, Tank.msg[self.number])
        Text.book[self.number].newMsg(self.msg)

    def fireMG(self,pressedkeys):
        # -- fire bow MG --
        doFireMG = self.MGcooltime <= 0 and self.MGammo > 0 and pressedkeys[self.MGfirekey]
        if not doFireMG: return
        # fire Machine Gun
        Tracer(self)
        mg2sound.play()
        self.MGcooltime = Tank.MGrecoiltime
        self.MGammo -= 1
        self.msg = "player%i: ammo: %i/%i keys: %s" % (self.number+1, self.ammo, self.MGammo, Tank.msg[self.number])
        Text.book[self.number].newMsg(self.msg)

    def setDirection(self,pressedkeys):
        # tank heading EAST
        # stop Tank by setting direction = 0
        self.Vd = Vector(0,0)
        if pressedkeys[self.forwardkey]: # forward
            self.Vd.x += +cos(self.tankAngle*GRAD)
            self.Vd.y += -sin(self.tankAngle*GRAD)
        if pressedkeys[self.backwardkey]: # backward
            self.Vd.x += -cos(self.tankAngle*GRAD)
            self.Vd.y += +sin(self.tankAngle*GRAD)

    def move(self,pressedkeys,seconds):
        doMoveTank =  pressedkeys[self.forwardkey] or pressedkeys[self.backwardkey]
        if not doMoveTank: return
        # direction
        self.setDirection(pressedkeys)
        # delta
        self.delta = self.Vd * self.movespeed
        self.Vp += self.delta * seconds
        self.rect.center = tuple(self.Vp)

    def update(self,seconds):
        # reduce cooltime
        self.reduceCooltime(seconds)
        # -- process keys --
        pressedkeys = pygame.key.get_pressed()
        # -- rotate turret --
        if self.number == 1:
            self.autotarget()
        else:
            self.rotateTurret(pressedkeys)
        # -- rotate tank --
        self.rotateTank(pressedkeys)
        # -- fire cannon --
        self.fireCannon(pressedkeys)
        # -- fire MG(bow) --
        self.fireMG(pressedkeys)
        # -- move Tank --
        self.move(pressedkeys,seconds)
        # -- paint sprite at correct position
        #self.rect.center = tuple(self.Vp)

class Turret(pygame.sprite.Sprite):
    """turret on top of tank"""
    def __init__(self, boss):
        pygame.sprite.Sprite.__init__(self, self.groups) # THE most important line !
        self.boss = boss
        self.width = self.boss.width        
        self.images = {} # how much recoil after shooting, reverse order of apperance
        for i in range(10):
            self.images[i]= drawCannon(boss,i)
        self.images[10] = drawCannon(boss,0) # idle position
 
    def update(self, seconds):        
        # painting the correct image of cannon
        if self.boss.cooltime > 0:
            index = 10.0 * self.boss.cooltime/Tank.recoiltime
            self.image = self.images[int(index)]
            #print 'cooltime: %.2f   images[%.2f]' %(self.boss.cooltime , index )
        else: # idle position : cooltime == 0
            self.image = self.images[0]
        # --------- rotating -------------  angle etc from Tank (boss)
        self.image  = pygame.transform.rotate(self.image, self.boss.turretAngle) 
        # ---------- move with boss ---------
        self.rect = self.image.get_rect(center =self.boss.rect.center)
        #self.rect.center = self.boss.rect.center
 

class Bullet(pygame.sprite.Sprite):
    ''' a big projectile fired by the thank's main cannon'''
    side = 7  # small side of bullet retangle
    vel = 180.0 # velocity
    mass = 50.0
    maxlifetime = 10.0 # seconds
    book = {}
    number = 0

    def __init__(self,boss):
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.boss = boss
        self.lifetime = 0.0
        self.number = Bullet.number
        Bullet.number += 1
        Bullet.book[self.number] = self
        self.tracer = False
        self.maxlifetime = Bullet.maxlifetime
        self.color = self.boss.color
        self.makeBullet()
        #self.delta = Vector(0,0)
        self.setDirection()
        self.setPosition()

    def setDirection(self):
        self.Vd = Vector(0,0)
        self.Vd.x = cos(self.angle*GRAD)
        self.Vd.y = -sin(self.angle*GRAD)

    def setPosition(self):
        # spawn bullet at the end of turret barrel instead tank center
        # cannon is around Tank.side long, calculate from Tank center
        # later substracted 20 pixel from this distance
        # so that bullet spawns close to thank muzzle
        self.Vp = copy.copy(self.boss.Vp) # copy boss's position
        self.Vp += self.Vd * (Tank.size - 20)

    def makeBullet(self):
        # drawing the bullet and rotating it according to it's launcher
        self.angle = self.boss.turretAngle
        self.radius = Bullet.side  # for collide_circle
        self.mass = Bullet.mass
        self.vel = Bullet.vel
        image = pygame.Surface( (2*Bullet.side,Bullet.side) ) # rect 2 x 1 
        image.fill(gray)
        pygame.draw.rect(image,self.color,(0,0,4,15) )
        pygame.draw.circle(image,self.color,(int(1.5*self.side),self.side//2),self.side//2)
        #pygame.draw.rect(image,self.color,(0,0,int(Bullet.side*1.5), Bullet.side) )
        pygame.draw.circle(image,black,(int(1.5*self.side),self.side//2),self.side//2,2)
        image.set_colorkey(gray)
        self.image0 = image.convert_alpha()
        self.image = pygame.transform.rotate(self.image0,self.angle)
        self.rect = self.image.get_rect()

    def checkLifetime(self,seconds): # kill it if too old
        self.lifetime += seconds
        if self.lifetime > self.maxlifetime:
            self.kill()
    def move(self,seconds):
        self.delta = self.Vd * self.vel
        self.Vp += self.delta * seconds
        self.rect.center = tuple(self.Vp)
#   def checkArea(self):
#       if self.Vp.x < 0 or self.Vp.y < 0:
#           self.kill()
#       elif self.Vp.x > screenwidth or self.Vp.y > screenheight:
#           self.kill()
        #self.rect.center = tuple(self.Vp)
    def update(self,seconds=0.0):
        self.checkLifetime(seconds)
        self.move(seconds)
        #self.checkArea()


class Tracer(Bullet):
    ''' Tracer is nearly the same as Bullet, but smaller and with another origin
        ( bow MG rect, instead cannon) '''
    vel = 200.0
    mass = 10.0
    color = (200,0,100)
    maxlifetime = 10.0
    size = 8
    def __init__(self,boss,turret=False):
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.number = Bullet.number
        Bullet.number += 1
        Bullet.book[self.number] = self
        self.tracer = True
        self.radius = Tracer.size
        self.mass = Tracer.mass
        self.vel = Tracer.vel
        self.lifetime = 0.0
        self.maxlifetime = Tracer.maxlifetime
        self.boss = boss
        self.angle = self.boss.tankAngle# + 90 # tank's forward direction
        self.setPosition()
        self.setDirection()
        self.makeBullet()
    def setPosition(self): # starting pos
        x,y = tuple(self.boss.Vc)
        angle = atan2(-y,x)/pi * 180 # y axis UPSIDE DOWN
        magnitude = self.boss.Vc.get_magnitude()
        Vd = Vector()
        Vd.x = cos( (angle+self.boss.tankAngle)*GRAD )
        Vd.y = -sin( (angle+self.boss.tankAngle)*GRAD )
        self.Vp = self.boss.Vp + Vd*magnitude
        #print self.Vp
    def drawMGBullet(self):
        w = Tracer.size; h = w/2
        color1 = 200,200,0 #yellow
        image = pygame.Surface( (w,h) )
        image.fill(gray)
        r = h/2; c = w-r,r
        rect1 = 1,1,w-h-2,h-2
        pygame.draw.rect(image,color1,rect1)
        pygame.draw.circle(image,black,c,r)
        image.set_colorkey(gray)
        return image
    def makeBullet(self):
        image = self.drawMGBullet()
        self.image0 = image.convert_alpha()
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.rect = self.image.get_rect( center=tuple(self.Vp) ) #self.rect.center = tuple(self.Vp)

class Minimap(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.image = pygame.Surface( (radarmapwidth,radarmapheight) )
        self.paint()
        self.rect = self.image.get_rect()
        #self.rect.topleft  = screenwidth - radarmapwidth,0
        self.rect.topleft  = screenrect.left,screenrect.bottom-radarmapheight
        self.factorX = 1.0*radarmapwidth/bigmapwidth
        self.factorY = 1.0*radarmapheight/bigmapheight
    def paint(self):
        self.image.fill(black)
        # draw dark red frame
        pygame.draw.rect(self.image,darkred1,(0,0,radarmapwidth,radarmapheight),1)
    def update(self,seconds):
        self.paint()
        rect = cornerpoint[0] * self.factorX, cornerpoint[1]*self.factorY,\
               screenwidth*self.factorX,screenheight*self.factorY
        # draw white frame
        pygame.draw.rect(self.image,white,rect,1)
        for tankNo in Tank.book:
            pos = Tank.book[tankNo].Vp
            color = Tank.book[tankNo].color
            center = pos.x*self.factorX, pos.y*self.factorY
            rect = pygame.Rect(0,0,8,8)
            rect.center = center
            pygame.draw.rect(self.image,color,rect)
        for bulletNo in Bullet.book:
            if Bullet.book[bulletNo].tracer:
                dotsize = 2 # tracer
            else:
                dotsize = 4 # cannon
            pos = Bullet.book[bulletNo].Vp
            color = Bullet.book[bulletNo].color
            center2 = pos.x*self.factorX, pos.y*self.factorY
            #topleft = int(topleft[0]),int(topleft[1])
            #rect = topleft[0],topleft[1],dotlength,dotlength
            rect = pygame.Rect(0,0,dotsize,dotsize)
            rect.center = center2
            pygame.draw.rect(self.image,color, rect)

def main():
    # set sprites group
    tankgroup = pygame.sprite.Group()
    bulletgroup = pygame.sprite.Group()
    allgroup = pygame.sprite.LayeredUpdates()
    # set _layer
    Tank._layer = 4   # base layer
    Turret._layer = 6 # above Tank & Tracer
    Bullet._layer = 7 # to prove that Bullet is in top-layer
    Text._layer = 3   # below Tank
    Minimap._layer = 3  # below Tank # better 9 ?
    #assign default groups to each sprite class
    Tank.groups = tankgroup, allgroup
    Turret.groups = allgroup
    Bullet.groups = bulletgroup, allgroup
    Text.groups = allgroup
    Minimap.groups = allgroup

    player1 = Tank((150,250), 90) # create  first tank, looking north
    player2 = Tank((450,250), 90) # create second tank, looking south
    Minimap()
    status3 = Text((screenwidth//2, 10), "Tank Demo. Press ESC to quit")

    playtime = 0
    mainloop = True           
    while mainloop:
        seconds = clock.tick(fps)/1000.0 # seconds passed since last frame (float)
        playtime += seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    mainloop = False # exit game
        pygame.display.set_caption("FPS: %.2f keys: %s" % ( clock.get_fps(), pressedKeysString()))
        allgroup.clear(screen, background) # funny effect if you outcomment this line
        allgroup.update(seconds)
        allgroup.draw(screen)
        pygame.display.flip() # flip the screen 30 times a second
        #pygame.time.wait(100000)
    return 0
 
if __name__ == '__main__':
    main()
