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
        self.turretTurnSpeed = Tank.turretTurnSpeed / 2.0
        self.tankTurnSpeed   = Tank.tankTurnSpeed / 2.0
        self.speed = Tank.speed * 1.5 #25.0 * 2
        # logging
        logging.debug('nestposition %s' %self.nestposition)
        logging.debug('nestsize %d' %self.nestsize)
        # define states
        exploringstate = AIStateExploring(self)
        huntingstate   = AIStateHunting(self)
        # add State to brain
        self.brain = Brain()
        self.brain.addState(exploringstate)
        self.brain.addState(huntingstate)
        # set ant's State as Exploring
        self.brain.setActiveState('exploring')

    def fireCannon(self):
        doFireCannon = self.cooltime <= 0 and self.ammo >0
        if not doFireCannon: return
        # fire Cannon: cooltime == 0
        self.bullet = CannonBall(self)
        self.world.cannonsound.play()
        self.cooltime = Tank.recoiltime # seconds until tank can fire again
        self.ammo -= 1


    def autoDirection(self,player):
        delta = player.Vp - self.Vp
        targetAngle = atan2(-delta.y,delta.x)/pi * 180
        diffAngle = targetAngle - self.turretAngle
        return diffAngle

    def autotarget(self,player):
        diffAngle = self.autoDirection(player)
        # auto turn tank,turret 
        self.tankAngle   += diffAngle # * 4/10.0
        self.turretAngle += diffAngle # * 4/10.0
        # auto targeting
        if diffAngle < 0: diffAngle += 360
        diffAngle = diffAngle % 360
        if abs(diffAngle) < 15:
            self.turndirection = 0
            self.fireCannon()
        elif diffAngle < 180:   self.turndirection = +1/4.0
        elif diffAngle > 180:   self.turndirection = -1/4.0
        self.turretAngle += self.turndirection * self.turretTurnSpeed

    def calculateDirection(self):
        self.Vd = Vector(0,0)
        self.Vd.x += +cos(self.tankAngle*GRAD)
        self.Vd.y += -sin(self.tankAngle*GRAD)

    def rotateTank(self):
        self.image = pygame.transform.rotate(self.image0, self.tankAngle)
        self.rect = self.image.get_rect(center = self.rect.center) #center = oldcenter = self.rect.center

    def IsOutOfNest(self):
        distance = self.Vp.get_distance_to(self.nestposition)
        print 'distance: ', distance
        if abs(self.Vp.get_distance_to(self.nestposition) ) > self.nestsize/2:
            print 'nest size/2',int(self.nestsize/2)
            print 'out of nest',self.Vp, self.nestposition
            return True

    def move(self,seconds):
        if self.IsOutOfNest():
            self.tankAngle += 180 ###
            self.turretAngle += 180
        # direction
        self.calculateDirection()
        self.rotateTank()
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
