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
        self.boss = boss
        self.delta = Vector(0,0)
        self.angle = 0
        self.lifetime = 0.0
        self.color = self.boss.color
        self.turretAngle = self.boss.turretAngle
        self.calculateHeading()
        self.delta += self.boss.delta # add boss's movement
        self.pos = copy.copy(self.boss.pos) # copy boss's position
        self.calculateOrigin()
        self.update()
    def calculateHeading(self):
        # drawing the bullet and rotating it according to it's launcher
        self.radius = Bullet.side  # for collide_circle
        self.angle += self.boss.turretAngle
        self.mass = Bullet.mass
        self.vel = Bullet.vel
        image = pygame.Surface( (2*Bullet.side,Bullet.side) ) # rect 2 x 1 
        image.fill(gray)
        pygame.draw.rect(image,self.color,(0,0,int(Bullet.side*1.5), Bullet.side) )
        pygame.draw.circle(image,self.color,(int(1.5*self.side),self.side//2),self.side//2)
        image.set_colorkey(gray)
        self.image0 = image.convert_alpha()
        self.image = pygame.transform.rotate(self.image0,self.angle)
        self.rect = self.image.get_rect()
        Vd = Vector() # direction Vector
        Vd.x =  cos(self.turretAngle*GRAD)
        Vd.y =  sin(-self.turretAngle*GRAD)
        self.delta = Vd * self.vel
    def calculateOrigin(self):
        # spawn bullet at the end of turret barrel instead tank center
        # cannon is around Tank.side long, calculate from Tank center
        # later substracted 20 pixel from this distance
        # so that bullet spawns close to thank muzzle
        Vd = Vector() # direction Vector
        Vd.x = cos(self.turretAngle*GRAD)
        Vd.y = sin(-self.turretAngle*GRAD)
        self.pos += Vd * (Tank.side - 20)
    def checkLifetime(self,seconds):
        # kill it if too old
        self.lifetime += seconds
        if self.lifetime > Bullet.maxlifetime:
            self.kill()
    def move(self,seconds):
        self.pos += self.delta * seconds
    def checkArea(self):
        if self.pos.x < 0 or self.pos.y < 0:
            self.kill()
        elif self.pos.x > screenwidth or self.pos.y > screenheight:
            self.kill()
    def update(self,seconds=0.0):
        self.checkLifetime(seconds)
        self.move(seconds)
        self.checkArea()
        self.rect.center = tuple(self.pos)


class Tracer(Bullet):
    ''' Tracer is nearly the same as Bullet, but smaller and with another origin
        ( bow MG rect, instead cannon) '''
    side = 15 # long side of bullet rectangle
    vel = 200.0
    mass = 10.0
    color = (200,0,100)
    maxlifetime = 10.0

    def __init__(self,boss,turret=False):
        self.turret = turret
        Bullet.__init__(self, boss) 
    def calculateHeading(self):
        self.radius = Tracer.side
        self.angle = 0
        self.angle += self.boss.tankAngle
        if self.turret:
            self.angle = self.boss.turretAngle
        self.mass = Tracer.mass
        self.vel = Tracer.vel
        image = pygame.Surface( (Tracer.side, Tracer.side/4) ) # a line
        image.fill(self.boss.color)
        rect1 = Tracer.side*3/4, 0, Tracer.side, Tracer.side/4
        pygame.draw.rect(image,black,rect1) # red dot in front
        image.set_colorkey(gray)
        self.image0 = image.convert_alpha()
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.rect = self.image.get_rect()
        Vd = Vector()
        if self.turret:
            Vd.x = cos(self.boss.turretAngle*GRAD)
            Vd.y = sin(-self.boss.turretAngle*GRAD)
        else:
            Vd.x = cos(self.boss.tankAngle*GRAD)
            Vd.y = sin(-self.boss.tankAngle*GRAD)
        self.delta = Vd * self.vel
    def calculateOrigin(self):
        Vd = Vector()
        if self.turret:
            Vd.x = cos( (-90 + self.boss.turretAngle)*GRAD )
            Vd.y = sin( (+90 - self.boss.turretAngle)*GRAD )
            self.pos += Vd * 15
        else:
            Vd.x = cos( (30 + self.boss.tankAngle)*GRAD )
            Vd.y = sin( (-30 - self.boss.tankAngle)*GRAD )
            self.pos += Vd * (Tank.side/2.0)

class Tank(pygame.sprite.Sprite):
    ''' A Tank controlled by the Player
        this Tank draws its own Turret(including main gun) and its bow rectangle
        (slit for Tracer Machine Gun) '''
    side = 100
    recoiltime = 0.75 # how many seconds the cannon is busy after firing one time
    MGrecoiltime = 0.2 # how many seconds the bow(machine gun) is idel
    turretTurnSpeed = 25
    tankTurnSpeed = 8
    movespeed = 25
    maxrotate = 360
    book = {} # a book of tanks to store all tanks
    number = 0
    # KEYs for tank control
    #    player1, player2
    firekey     = (pygame.K_k,pygame.K_DOWN)
    MGfirekey   = (pygame.K_LCTRL, pygame.K_KP_ENTER)
    MG2firekey  = (pygame.K_i, pygame.K_UP)
    turretLeftkey  = (pygame.K_j, pygame.K_LEFT)
    turretRightkey = (pygame.K_l, pygame.K_RIGHT)
    forwardkey      = (pygame.K_w, pygame.K_KP8)
    backwardkey     = (pygame.K_s, pygame.K_KP5)
    tankLeftkey     = (pygame.K_a, pygame.K_KP4)
    tankRightkey    = (pygame.K_d, pygame.K_KP6)
    color = ((200,200,0),(0,0,200) )
    msg = ['wasd LCTRL, ijkl','Keypad: 4852, ENTER, cursor']

    def __init__(self,startpos=(150,150),angle=0):
        self.number = Tank.number
        Tank.number += 1
        Tank.book[self.number] = self
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.pos = Vector(startpos)
        self.delta = Vector()
        self.ammo = 30 # main gun
        self.MGammo = 500 # machine gun
        self.msg =  "player%i: ammo: %i/%i keys: %s" % (self.number+1, self.ammo, self.MGammo, Tank.msg[self.number])
        Text((screenwidth/2, 30+20*self.number), self.msg) # create status line text sprite
        self.color = Tank.color[self.number]
        self.turretAngle = angle
        self.tankAngle = angle
        self.setKeys()
        self.makeTank()

    def makeTank(self):
        image = pygame.Surface( (Tank.side,Tank.side) )
        image.fill(gray)
        color1 = (90,90,90)
        pygame.draw.rect(image,self.color,(5,5,self.side-10,self.side-10)) # tank body, margin 5
        pygame.draw.rect(image,color1,(0,0,self.side//6,self.side)) # tank left
        pygame.draw.rect(image,color1,(self.side-self.side//6,0,self.side,self.side)) # right track
        pygame.draw.rect(image,red,(self.side//6+5,10,10,5)) # red bow rect left
        pygame.draw.circle(image,red,(self.side//2,self.side//2),self.side//3,2) # red circle for turret
        image = pygame.transform.rotate(image,-90) # rotate so as to look EAST
        self.image0 = image.convert_alpha()
        self.image = image.convert_alpha()
        self.rect = self.image0.get_rect()
        # ------ turret ------------
        self.firestatus = 0.0
        self.MGfirestatus = 0.0
        self.MG2firestatus = 0.0
        self.turndirection = 0
        self.tankturndirection = 0
        self.movespeed = Tank.movespeed
        self.turretTurnSpeed = Tank.turretTurnSpeed
        self.tankTurnSpeed = Tank.tankTurnSpeed
        Turret(self) # create a Turret for this thank

    def setKeys(self):
        self.firekey    = Tank.firekey[self.number]
        self.MGfirekey  = Tank.MGfirekey[self.number]
        self.MG2firekey = Tank.MG2firekey[self.number]
        self.turretLeftkey  = Tank.turretLeftkey[self.number]
        self.turretRightkey = Tank.turretRightkey[self.number]
        self.forwardkey      = Tank.forwardkey[self.number]
        self.backwardkey    = Tank.backwardkey[self.number]
        self.tankLeftkey    = Tank.tankLeftkey[self.number]
        self.tankRightkey   = Tank.tankRightkey[self.number]
    def checkFirestatus(self,seconds): # reloading, firestatus
        if self.firestatus > 0:
            self.firestatus -= seconds
            if self.firestatus < 0: self.firestatus = 0
        if self.MGfirestatus > 0:
            self.MGfirestatus -= seconds
            if self.MGfirestatus < 0: self.MGfirestatus = 0
        if self.MG2firestatus > 0:
            self.MG2firestatus -= seconds
            if self.MG2firestatus < 0: self.MG2firestatus = 0
    def rotateTurret(self,pressedkeys):
        if  pressedkeys[self.turretLeftkey]:   self.turndirection = +1
        elif pressedkeys[self.turretRightkey]: self.turndirection = -1
        else: self.turndirection = 0 # left/right turret rotation
    def rotateTank(self,pressedkeys):
        if   pressedkeys[self.tankLeftkey]:  self.tankturndirection = +1
        elif pressedkeys[self.tankRightkey]: self.tankturndirection = -1
        else: self.tankturndirection = 0 # reset left/right rotation
    def fireCannon(self,pressedkeys):
        isFireCannon = (self.firestatus ==0 and self.ammo >0 ) and pressedkeys[self.firekey]
        if not isFireCannon: return
        # fire Cannon
        cannonsound.play()
        self.firestatus = Tank.recoiltime # seconds until tank can fire again
        Bullet(self)
        self.ammo -= 1
        self.msg =  "player%i: ammo: %i/%i keys: %s" % (self.number+1, self.ammo, self.MGammo, Tank.msg[self.number])
        Text.book[self.number].newMsg(self.msg)
    def fireMG(self,pressedkeys):
        # -- fire bow MG --
        isFireMG = (self.MGfirestatus ==0 and self.MGammo >0 ) and pressedkeys[self.MGfirekey]
        if not isFireMG: return
        # fire Machine Gun
        mg2sound.play()
        self.MGfirestatus = Tank.MGrecoiltime
        Tracer(self, False) # turret mg = False
        self.MGammo -= 1
        self.msg = "player%i: ammo: %i/%i keys: %s" % (self.number+1, self.ammo, self.MGammo, Tank.msg[self.number])
        Text.book[self.number].newMsg(self.msg)

    def fireMG2(self,pressedkeys):
        # -- fire bow MG --
        isFireMG2 = (self.MG2firestatus ==0 and self.MGammo >0 ) and pressedkeys[self.MG2firekey]
        if not isFireMG2: return
        # -------- fire turret MG ---------------
        mg2sound.play()
        self.MG2firestatus = Tank.MGrecoiltime # same recoiltime for both mg's
        Tracer(self, True) # turret mg = True
        self.MGammo -= 1
        self.msg =  "player%i: ammo: %i/%i keys: %s" % (self.number+1, self.ammo, self.MGammo, Tank.msg[self.number])
        Text.book[self.number].newMsg(self.msg)
    def move(self,pressedkeys,seconds):
        self.forward = 0 # movement calculator
        # if both pressed, self.forward becomes 0
        if pressedkeys[self.forwardkey]:
            self.forward += 1
        if pressedkeys[self.backwardkey]:
            self.forward -= 1
        self.delta = Vector()
        Vd = Vector()
        if self.forward == 1:
            Vd.x = +cos(self.tankAngle*GRAD)
            Vd.y = -sin(self.tankAngle*GRAD)
            self.delta = Vd * self.movespeed
        if self.forward == -1:
            Vd.x = -cos(self.tankAngle*GRAD)
            Vd.y = +sin(self.tankAngle*GRAD)
            self.delta = Vd * self.movespeed
        self.pos += self.delta * seconds

    def update(self,seconds):
        self.checkFirestatus(seconds)
        # -- process keys --
        pressedkeys = pygame.key.get_pressed()
        # -- turret manual rotate
        self.rotateTurret(pressedkeys)
        # -- tank rotation --
        self.rotateTank(pressedkeys)
        # -- turn tank --
        self.tankAngle += self.tankturndirection * self.tankTurnSpeed * seconds
        # angle etc from Tank(boss)
        oldcenter = self.rect.center
        oldrect = self.image.get_rect()
        self.image = pygame.transform.rotate(self.image0, self.tankAngle)
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter
        # if tank is rotating, turret is also rotating with tank!
        # -- turret autorotate --
        self.turretAngle += self.tankturndirection * self.tankTurnSpeed * seconds
        self.turretAngle += self.turndirection * self.turretTurnSpeed * seconds
        # -- fire cannon --
        self.fireCannon(pressedkeys)
        # -- fire MG(bow) --
        self.fireMG(pressedkeys)
        # -- fire MG2(turret) --
        self.fireMG2(pressedkeys)
        # -- movement --
        self.move(pressedkeys,seconds)
        # -- border collision --
        if self.pos.y + self.side/2 >= screenheight:
            self.pos.y = screenheight - self.side/2
            self.delta.y = 0
        elif self.pos.y - self.side/2 <= 0:
            self.pos.y = 0 + self.side/2
            self.delta.y = 0
        # -- paint sprite at correct position
        self.rect.center = tuple(self.pos)


class Turret(pygame.sprite.Sprite):
    """turret on top of tank"""
    def __init__(self, boss):
        pygame.sprite.Sprite.__init__(self, self.groups) # THE most important line !
        self.boss = boss
        self.side = self.boss.side        
        self.images = {} # how much recoil after shooting, reverse order of apperance
        self.images[0] = self.draw_cannon(0)  # idle position
        self.images[1] = self.draw_cannon(1)
        self.images[2] = self.draw_cannon(2)
        self.images[3] = self.draw_cannon(3)
        self.images[4] = self.draw_cannon(4)
        self.images[5] = self.draw_cannon(5)
        self.images[6] = self.draw_cannon(6)
        self.images[7] = self.draw_cannon(7)
        self.images[8] = self.draw_cannon(8)  # position of max recoil
        self.images[9] = self.draw_cannon(4)
        self.images[10] = self.draw_cannon(0) # idle position
 
    def update(self, seconds):        
        # painting the correct image of cannon
        if self.boss.firestatus > 0:
            self.image = self.images[int(self.boss.firestatus // (Tank.recoiltime / 10.0))]
        else:
            self.image = self.images[0]
        # --------- rotating -------------
        # angle etc from Tank (boss)
        oldrect = self.image.get_rect() # store current surface rect
        self.image  = pygame.transform.rotate(self.image, self.boss.turretAngle) 
        self.rect = self.image.get_rect()
        # ---------- move with boss ---------
        self.rect = self.image.get_rect()
        self.rect.center = self.boss.rect.center
 
    def draw_cannon(self, offset):
         # painting facing right, offset is the recoil
         image = pygame.Surface((self.boss.side * 2,self.boss.side * 2)) # created on the fly
         image.fill((128,128,128)) # fill grey
         pygame.draw.circle(image, (255,0,0), (self.side,self.side), 22, 0) # red circle
         pygame.draw.circle(image, (0,255,0), (self.side,self.side), 18, 0) # green circle
         pygame.draw.rect(image, (255,0,0), (self.side-10, self.side + 10, 15,2)) # turret mg rectangle
         pygame.draw.rect(image, (0,255,0), (self.side-20 - offset,self.side - 5, self.side - offset,10)) # green cannon
         pygame.draw.rect(image, (255,0,0), (self.side-20 - offset,self.side - 5, self.side - offset,10),1) # red rect 
         image.set_colorkey((128,128,128))
         return image
# ---------------- End of classes --------------------
#------------ defs ------------------
def radians_to_degrees(radians):
    return (radians / math.pi) * 180.0
 
def degrees_to_radians(degrees):
    return degrees * (math.pi / 180.0)
 
def write(msg="pygame is cool"):
    """helper function for the Text sprite"""
    myfont = pygame.font.SysFont("None", 28)
    mytext = myfont.render(msg, True, (255,0,0))
    mytext = mytext.convert_alpha()
    return mytext        
 
def pressedKeysString():
    """returns the pressed keys (for the player1 tank) to be displayd in the status line"""
    pressedkeys = pygame.key.get_pressed()
    line = ""
    if pressedkeys[pygame.K_a]:
        line += "a "
    if pressedkeys[pygame.K_d]:
        line += "d "
    if pressedkeys[pygame.K_w]:
        line += "w "
    if pressedkeys[pygame.K_s]:
        line += "s "
    if pressedkeys[pygame.K_LCTRL]:
        line += "LCTRL"
    return line
 
def main():

    playtime = 0
    tankgroup = pygame.sprite.Group()
    bulletgroup = pygame.sprite.Group()
    allgroup = pygame.sprite.LayeredUpdates()
 
    Tank._layer = 4   # base layer
    Bullet._layer = 7 # to prove that Bullet is in top-layer
    Tracer._layer = 5 # above Tank, but below Turret
    Turret._layer = 6 # above Tank & Tracer
    Text._layer = 3   # below Tank
 
    #assign default groups to each sprite class
    Tank.groups = tankgroup, allgroup
    Turret.groups = allgroup
    Bullet.groups = bulletgroup, allgroup
    Text.groups = allgroup
    player1 = Tank((150,250), 90) # create  first tank, looking north
    player2 = Tank((450,250), -90) # create second tank, looking south
    status3 = Text((screenwidth//2, 10), "Tank Demo. Press ESC to quit")
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
    return 0
 
if __name__ == '__main__':
    main()
