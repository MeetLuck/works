''' 020 shooting from tank.py
    demo of 2 tanks shooting bullets at the end of it's cannon
    and shooting tracers at the end of it's bow Machine Gun
    and from the turret-machine gun (co-axial with main gun)
    '''
from constants022A import *
from Entity5 import *
import copy

class Tank(pygame.sprite.Sprite):
    size = 100
    recoiltime = 2*0.75 # how many seconds the cannon is busy after firing one time
    MGrecoiltime = 0.25 # how many seconds the bow(machine gun) is idel
    turretTurnSpeed = 1
    tankTurnSpeed = 1 # degrees
    speed = 25.0 * 3
    book = {} # a book of tanks to store all tanks
    number = 0
    color = ((200,200,0),(0,0,200) )

    def __init__(self,world,name,startpos=(150,150),angle=0):
        super(Tank,self).__init__(self.groups)
        #pygame.sprite.Sprite.__init__(self,self.groups)
        self.name = name
        self.world = world
        self.color = Tank.color[self.number]
        self.number = Tank.number
        Tank.number += 1
        Tank.book[self.number] = self
        self.setKeys()
        self.makeTank(startpos,angle)
        self.turret = Turret(self) # create a Turret for this thank
        self.getCannonhit = False
        self.getMGhit = False
        self.lifebar = Lifebar(self)

    def makeTank(self,startpos,angle):
        self.width,self.height = Tank.size,Tank.size
        image,MGcenter,Vc = drawTank(self.width,self.height,self.color)
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
        self.speed = Tank.speed
        # tank constants
        self.tankTurnSpeed = Tank.tankTurnSpeed
        self.tankturndirection = 0
        self.ammo = 100 # main gun
        self.MGammo = 500 # machine gun
        self.healthful = 100.0
        self.health    = 100.0
        # turret constants
        self.cooltime = 0.0  # cannon
        self.MGcooltime = 0.0 # Machine Gun
        self.turndirection = 0
        self.turretAngle = angle
        self.turretTurnSpeed = Tank.turretTurnSpeed

    def setKeys(self):
        self.forwardkey     =  pygame.K_k
        self.backwardkey    =  pygame.K_j
        self.tankLeftkey    =  pygame.K_a
        self.tankRightkey   =  pygame.K_s
        self.firekey        =  pygame.K_SPACE
        self.MGfirekey      =  pygame.K_l
        self.turretLeftkey  =  pygame.K_d
        self.turretRightkey =  pygame.K_f

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

    def reduceCooltime(self,seconds): # reloading, firestatus
        self.cooltime     -= seconds
        self.MGcooltime   -= seconds

    def fireCannon(self):
        doFireCannon = self.cooltime <= 0 and self.ammo >0
        if not doFireCannon: return
        # fire Cannon: cooltime == 0
        self.bullet = CannonBall(self)
        self.world.cannonsound.play()
        self.cooltime = Tank.recoiltime # seconds until tank can fire again
        self.ammo -= 1

    def fireMG(self):
        # -- fire bow MG --
        doFireMG = self.MGcooltime <= 0 and self.MGammo > 0
        if not doFireMG: return
        # fire Machine Gun
        self.mgbullet = MGBullet(self)
        self.world.mg2sound.play()
        self.MGcooltime = Tank.MGrecoiltime
        self.MGammo -= 1

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

    def move(self,seconds):
        # delta
        self.delta = self.Vd * self.speed
        self.Vp += self.delta * seconds
        self.rect.center = tuple(self.Vp)

    def checkHit(self):
        if self.getCannonhit:
            print 'getCannonhit'
            self.world.cannonhitsound.play()
            self.health -= 10
        if self.getMGhit:
            print 'getCannonhit'
            self.world.hitsound.play()
            self.health -= 1
        if self.health <= 0:
            self.kill()

    def kill(self):
        print 'get killed =>',self
        self.lifebar.kill()
        self.turret.kill()
        for _ in range(random.randint(20,40)):
            Explosion(self.Vp)
        del Tank.book[self.number]
        pygame.sprite.Sprite.kill(self)

    def update(self,seconds):
        # reduce cooltime
        self.reduceCooltime(seconds)
        # hit check
        self.checkHit()
            #self.world.mg3sound.play()
        # -- process keys --
        pressedkeys = pygame.key.get_pressed()
        # -- rotate turret --
        self.rotateTurret(pressedkeys)
        # -- rotate tank --
        self.rotateTank(pressedkeys)
        # -- fire cannon -- 
        if pressedkeys[self.firekey]:
            self.fireCannon()
        # -- fire MG(bow) --
        if pressedkeys[self.MGfirekey]:
            self.fireMG()
        # --- set direction --
        self.setDirection(pressedkeys)
        # -- move Tank --
        if pressedkeys[self.forwardkey] or pressedkeys[self.backwardkey]:
            self.move(seconds)
        # -- paint sprite at correct position
        #self.rect.center = tuple(self.Vp)
