from Tank import *
from StateMachine import *

class Player(Tank):
    def __init__(self,world,name,startpos=(150,150),angle=0):
        Tank.__init__(self,world,name,startpos,angle)

class AI(Tank):
    def __init__(self,world,name,startpos=(150,150),angle=0):
        Tank.__init__(self,world,name,startpos,angle)
        self.nestposition = 300,200
        self.nestsize = 200
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
        self.tankAngle += diffAngle
        return diffAngle

    def autotarget(self,player):
        diffAngle = self.autoDirection(player)

        if diffAngle < 0: diffAngle += 360
        diffAngle = diffAngle % 360
        if abs(diffAngle) < 15:
            self.turndirection = 0
            self.fireCannon()
        elif diffAngle < 180:   self.turndirection = +1 #/4.0
        elif diffAngle > 180:   self.turndirection = -1 #/4.0
        self.turretAngle += self.turndirection * self.turretTurnSpeed

    def calculateDirection(self):
        self.Vd = Vector(0,0)
        self.Vd.x += +cos(self.tankAngle*GRAD)
        self.Vd.y += -sin(self.tankAngle*GRAD)

    def rotateTank(self):
        self.image = pygame.transform.rotate(self.image0, self.tankAngle)
        self.rect = self.image.get_rect(center = self.rect.center) #center = oldcenter = self.rect.center

    def move(self,seconds):
        # direction
        self.delta = self.Vd * self.speed
        self.Vp += self.delta * seconds
        self.rect.center = tuple(self.Vp)

    def update(self,seconds):
        # reduce cooltime
        self.reduceCooltime(seconds)
        # brain
        self.brain.think()
        # rotate Tank
        self.rotateTank()
        # hit check
        self.checkHit()
        # calculate Direction
        self.calculateDirection()
        # -- move Tank --
        self.move(seconds)
