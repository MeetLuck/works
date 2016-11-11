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
        self.nestposition = Vector(self.world.ainestposition)
        self.nestsize = self.world.ainestsize
        self.resetSpeed()
        # logging
        logging.debug('nestposition %s' %self.nestposition)
        logging.debug('nestsize %d' %self.nestsize)
        # define states
        exploringstate = AIStateExploring(self)
        homestate = AIStateHome(self)
        huntingstate   = AIStateHunting(self)
        # add State to brain
        self.brain = Brain()
        self.brain.addState(exploringstate)
        self.brain.addState(homestate)
        self.brain.addState(huntingstate)
        # set ant's State as Exploring
        self.brain.setActiveState('exploring')

    def resetSpeed(self):
        self.turretTurnSpeed = 2*Tank.turretTurnSpeed 
        self.tankTurnSpeed   = Tank.tankTurnSpeed
        self.tankturndirection = 0
        self.turndirection = 0
        self.speed = Tank.speed / 2.0

    def getdiffAngle(self,player):
        if player is None: return
        delta = player.Vp - self.Vp
        targetAngle = atan2(-delta.y,delta.x)/pi * 180
        diffAngle = targetAngle - self.turretAngle
        if diffAngle < 0: diffAngle += 360
        diffAngle %= 360
        return diffAngle

    def autorotateTank(self,player):
        diffAngle = self.getdiffAngle(player)
        #self.tankAngle   += diffAngle # * 4/10.0
        #self.turretAngle += diffAngle # * 4/10.0
        if abs(diffAngle) <= 15:
            self.tankturndirection = 0
            self.fireMG()
        elif diffAngle < 180:   self.tankturndirection = +15
        elif diffAngle > 180:   self.tankturndirection = -15

#       deltaAngle = self.tankturndirection * self.tankTurnSpeed

#       self.tankAngle += deltaAngle
#       self.turretAngle += deltaAngle
        print diffAngle,deltaAngle

    def autotarget(self,player):
        diffAngle = self.getdiffAngle(player)
        # auto targeting
        if abs(diffAngle) < 15:
            self.turndirection = 0
            self.fireCannon()
        elif diffAngle < 180:   self.turndirection = +1
        elif diffAngle > 180:   self.turndirection = -1
        #self.tankturndirection = self.turndirection
        self.tankAngle += self.turndirection * self.tankTurnSpeed
        self.turretAngle += self.turndirection * self.turretTurnSpeed

    def calculateDirection(self):
        self.Vd = Vector(0,0)
        self.Vd.x += +cos(self.tankAngle*GRAD)
        self.Vd.y += -sin(self.tankAngle*GRAD)

    def rotateTank(self):
        self.image = pygame.transform.rotate(self.image0, self.tankAngle)
        self.rect = self.image.get_rect(center = self.rect.center) #center = oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, self.tankAngle)
        self.rect = self.image.get_rect(center = self.rect.center) #center = oldcenter = self.rect.center

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
