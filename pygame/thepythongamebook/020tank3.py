''' 020 shooting from tank.py
    demo of 2 tanks shooting bullets at the end of it's cannon
    and shooting tracers at the end of it's bow Machine Gun
    and from the turret-machine gun (co-axial with main gun)
    '''
from constants020 import *
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
        self.number = Tank.number
        Tank.number += 1
        Tank.book[self.number] = self
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.pos = Vector(startpos)
        self.delta = Vector()
        self.Vd = Vector()
        self.ammo = 3000 # main gun
        self.MGammo = 500000 # machine gun
        self.msg =  "player%i: ammo: %i/%i keys: %s" % (self.number+1, self.ammo, self.MGammo, Tank.msg[self.number])
        Text((screenwidth/2, 30+20*self.number), self.msg) # create status line text sprite
        self.color = Tank.color[self.number]
        self.turretAngle = angle #angle+90
        self.tankAngle = angle
        self.setKeys()
        self.width,self.height = Tank.size,Tank.size
        self.makeTank()
        Turret(self) # create a Turret for this thank

    def makeTank(self):
        image = drawTank(self.width,self.height)
        self.image0 = image.convert_alpha()
        self.image = image.convert_alpha()
        self.rect = self.image0.get_rect()
        # ------ turret ------------
        self.cooltime = 0.0
        self.MGcooltime = 0.0
        self.turndirection = 0
        self.tankturndirection = 0
        self.movespeed = Tank.movespeed
        self.turretTurnSpeed = Tank.turretTurnSpeed
        self.tankTurnSpeed = Tank.tankTurnSpeed

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
        self.turndirection = 0 # left/right turret rotation
        if pressedkeys[self.turretLeftkey]:  self.turndirection += 1
        if pressedkeys[self.turretRightkey]: self.turndirection -= 1
        self.turretAngle += self.turndirection * self.turretTurnSpeed  #* seconds

    def rotateTank(self,pressedkeys):
        self.tankturndirection = 0 # reset left/right rotation
        if pressedkeys[self.tankLeftkey]:  self.tankturndirection += 1
        if pressedkeys[self.tankRightkey]: self.tankturndirection -= 1
        deltaAngle = self.tankturndirection * self.tankTurnSpeed # * seconds
        self.tankAngle += deltaAngle
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, self.tankAngle)
        self.rect = self.image.get_rect(center = oldcenter)
        # -- turret autorotate --
        # if tank is rotating, turret is also rotating with tank!
        self.turretAngle += deltaAngle

    def checkCooltime(self,seconds): # reloading, firestatus
        self.cooltime     -= seconds
        self.MGcooltime -= seconds
        if self.cooltime < 0: self.cooltime = 0.0
        if self.MGcooltime < 0: self.MGcooltime = 0.0

    def fireCannon(self,pressedkeys):
        canFireCannon = (self.cooltime == 0 and self.ammo >0 ) and pressedkeys[self.firekey]
        if not canFireCannon: return
        # fire Cannon: firestatus == 0
        cannonsound.play()
        self.cooltime = Tank.recoiltime # seconds until tank can fire again
        self.ammo -= 1
        self.msg =  "player%i: ammo: %i/%i keys: %s" % (self.number+1, self.ammo, self.MGammo, Tank.msg[self.number])
        Text.book[self.number].newMsg(self.msg)

    def fireMG(self,pressedkeys):
        # -- fire bow MG --
        canFireMG = (self.MGcooltime ==0 and self.MGammo >0 ) and pressedkeys[self.MGfirekey]
        if not canFireMG: return
        # fire Machine Gun
        mg2sound.play()
        self.MGcooltime = Tank.MGrecoiltime
        self.MGammo -= 1
        self.msg = "player%i: ammo: %i/%i keys: %s" % (self.number+1, self.ammo, self.MGammo, Tank.msg[self.number])
        Text.book[self.number].newMsg(self.msg)

    def setDirection(self,pressedkeys):
        # we are heading NORTH, tank's forward direction is NORTH 
        # because rotation and movement direction differ, need +90 degrees compensation
        # if heading EAST, no need for adjustment
        moveAngle = self.tankAngle + 90
        isForward  =  pressedkeys[self.forwardkey]
        isBackward =  pressedkeys[self.backwardkey]
        if isForward and not isBackward:   # only forward
            self.Vd.x = +cos(moveAngle*GRAD)
            self.Vd.y = -sin(moveAngle*GRAD)
        elif not isForward and isBackward: # only backward
            self.Vd.x = -cos(moveAngle*GRAD)
            self.Vd.y = +sin(moveAngle*GRAD)
        else: # everything else = both pressed or no keypressed
              # stop Tank by setting direction = 0
            self.Vd = Vector(0,0)

    def move(self,pressedkeys,seconds):
        # direction
        self.setDirection(pressedkeys)
        # reset delta
        self.delta = self.Vd * self.movespeed
        self.pos += self.delta * seconds

    def processKeys(self,pressedkeys):
        self.canFireCannon = False
        self.canFireMG = False
        self.canMoveTank = False
        self.canRotateTank = False
        self.canRotateTurret = False
        # -- process keys --
        if pressedkeys[self.firekey]: self.canFireCannon = True
        if pressedkeys[self.MGfirekey]: self.canFireMG = True
        if pressedkeys[self.forwardkey] or pressedkeys[self.backwardkey]:   self.canMoveTank = True
        if pressedkeys[self.tankLeftkey] or pressedkeys[self.tankRightkey]: self.canRotateTank= True
        if pressedkeys[self.turretLeftkey] or pressedkeys[self.turretRightkey]: self.canRotateTurret= True

    def update(self,seconds):
        self.checkCooltime(seconds)
        # -- process keys --
        pressedkeys = pygame.key.get_pressed()
        self.processKeys(pressedkeys)
        # -- turret manual rotate
        if self.canRotateTurret: self.rotateTurret(pressedkeys)
        # -- tank rotation --
        if self.canRotateTank: self.rotateTank(pressedkeys)
        # -- fire cannon --
        if self.canFireCannon: self.fireCannon(pressedkeys)
        # -- fire MG(bow) --
        if self.canFireMG: self.fireMG(pressedkeys)
        # -- movement --
        if self.canMoveTank: self.move(pressedkeys,seconds)
        # -- paint sprite at correct position
        self.rect.center = tuple(self.pos)
        # test

class Turret(pygame.sprite.Sprite):
    """turret on top of tank"""
    def __init__(self, boss):
        pygame.sprite.Sprite.__init__(self, self.groups) # THE most important line !
        self.boss = boss
        self.width = self.boss.width        
        self.images = {} # how much recoil after shooting, reverse order of apperance
        for i in range(10):
            self.images[i]= draw_cannon(boss,i)
        self.images[10] = draw_cannon(boss,0) # idle position
 
    def update(self, seconds):        
        # painting the correct image of cannon
        if self.boss.cooltime > 0:
            index = 10.0 * self.boss.cooltime/Tank.recoiltime
            self.image = self.images[int(index)]
            print 'cooltime: %.2f   images[%.2f]' %(self.boss.cooltime , index )
        else: # idle position : cooltime == 0
            self.image = self.images[0]
        # --------- rotating -------------  angle etc from Tank (boss)
        self.image  = pygame.transform.rotate(self.image, self.boss.turretAngle) 
        # ---------- move with boss ---------
        self.rect = self.image.get_rect(center =self.boss.rect.center)
        #self.rect.center = self.boss.rect.center
 
def main():

    playtime = 0
    tankgroup = pygame.sprite.Group()
    bulletgroup = pygame.sprite.Group()
    allgroup = pygame.sprite.LayeredUpdates()
 
    Tank._layer = 4   # base layer
    Turret._layer = 6 # above Tank & Tracer
    Text._layer = 3   # below Tank
 
    #assign default groups to each sprite class
    Tank.groups = tankgroup, allgroup
    Turret.groups = allgroup
    Text.groups = allgroup
    player1 = Tank((150,250), 0) # create  first tank, looking north
    #player2 = Tank((450,250), 0) # create second tank, looking south
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
        #pygame.time.wait(100000)
    return 0
 
if __name__ == '__main__':
    main()
