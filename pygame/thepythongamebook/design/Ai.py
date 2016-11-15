from Tank import *
from StateMachine import *

class Player(Tank):
    def __init__(self,world,name,startpos=(150,150),angle=0):
        Tank.__init__(self,world,name,startpos,angle)
        self.speed = Tank.speed * 1.0 #25.0 * 2
        self.tankTurnSpeed   = Tank.tankTurnSpeed * 2.0

class AI(Tank):
    def __init__(self,world,name,startpos=(150,150),angle=0):
        Tank.__init__(self,world,name,startpos,angle)
        self.nestposition = Vector(self.world.nestposition)
        self.nestsize = self.world.nestsize
        self.resetSpeed()
        self.makeBrain()
        # logging
        logging.debug('nestposition %s' %self.nestposition)
        logging.debug('nestsize %d' %self.nestsize)

    def makeBrain(self):
        # make brain
        self.brain = Brain()
        # define states
        exploring   = AIStateExploring(self)
        home        = AIStateHome(self)
        hunting     = AIStateHunting(self)
        # add State to brain
        self.brain.addState(exploring)
        self.brain.addState(home)
        self.brain.addState(hunting)
        # set activeState as Exploring
        self.brain.setActiveState('exploring')

    def resetSpeed(self):
        self.turretTurnSpeed = Tank.turretTurnSpeed 
        self.tankTurnSpeed   = Tank.tankTurnSpeed
        self.tankturndirection = 0
        self.turndirection = 0
        self.speed = 0.5*Tank.speed

    def getdiffAngle(self,player):
        if player is None: return
        delta = player.Vp - self.Vp
        targetAngle = atan2(-delta.y,delta.x)/pi * 180
        diffAngle = targetAngle - self.tankAngle
        if diffAngle < 0: diffAngle += 360
        diffAngle %= 360
        return diffAngle

    def autorotateTank(self,player):
        diffAngle = self.getdiffAngle(player)
        if abs(diffAngle) <= 6:
            self.tankturndirection = 0
            #self.fireMG()
        elif diffAngle < 180:   self.tankturndirection = +2
        elif diffAngle > 180:   self.tankturndirection = -2

        deltaAngle = self.tankturndirection * self.tankTurnSpeed
        self.tankAngle += deltaAngle
        self.turretAngle += deltaAngle
        print diffAngle,deltaAngle

    def fireCannon(self):
        doFireCannon = self.cooltime <= 0 and self.ammo >0
        if not doFireCannon: return
        # fire Cannon: cooltime == 0
        self.bullet = CannonBall(self)
        self.world.cannonsound.play()
        self.cooltime = Tank.recoiltime # seconds until tank can fire again
        self.ammo -= 1
    def autotarget(self,player):
        diffAngle = self.getdiffAngle(player)
        # auto targeting
        if abs(diffAngle) <= 1:
            self.turndirection = 0
            self.fireCannon()
        elif diffAngle < 180:   self.turndirection = +1.0
        elif diffAngle > 180:   self.turndirection = -1.0
        self.tankAngle   += self.turndirection# * self.tankTurnSpeed
        self.turretAngle += self.turndirection# * self.tankTurnSpeed

    def calculateDirection(self):
        self.Vd = Vector(0,0)
        self.Vd.x += +cos(self.tankAngle*GRAD)
        self.Vd.y += -sin(self.tankAngle*GRAD)

    def rotateTank(self):
        self.image = pygame.transform.rotate(self.image0, self.tankAngle)
        self.rect = self.image.get_rect(center = self.rect.center) #center = oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, self.tankAngle)
        self.rect = self.image.get_rect(center = self.rect.center) #center = oldcenter = self.rect.center

    def getDistanceToPlayer(self,player):
        if player is None: return
        return self.Vp.get_distance_to(player.Vp)

    def IsOutOfNest(self):
        distance = self.Vp.get_distance_to(self.nestposition)
        print 'distance: ', distance
        if abs(self.Vp.get_distance_to(self.nestposition) ) >= self.nestsize:
            return True

    def move(self,seconds):
        # direction
        self.rotateTank()
        self.calculateDirection()
        self.delta = self.Vd * self.speed
        self.Vp += self.delta * seconds
        self.rect.center = tuple(self.Vp)

    def update(self,seconds):
        # reduce cooltime
        self.reduceCooltime(seconds)
        # brain
        self.brain.think()
        # hit check
        self.checkHit()
        # -- move Tank --
        self.move(seconds)
