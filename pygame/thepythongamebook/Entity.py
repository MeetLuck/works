''' 020 shooting from tank.py
    demo of 2 tanks shooting bullets at the end of it's cannon
    and shooting tracers at the end of it's bow Machine Gun
    and from the turret-machine gun (co-axial with main gun)
    '''
from constants022A import *
import copy


class Lifebar(pygame.sprite.Sprite):
    """shows a bar with the health of Tank"""
    def __init__(self, boss):
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.boss = boss
        self.image = pygame.Surface((self.boss.rect.width,7))
        self.image.set_colorkey(black) # black transparent
        pygame.draw.rect(self.image, green, (0,0,self.boss.rect.width,7),1)
        self.rect = self.image.get_rect()
        self.oldpercent = 0
        self.bossnumber = self.boss.number # the unique number (name) of my boss
        
    def update(self, time):
        self.percent = self.boss.health / self.boss.healthful
        if self.percent != self.oldpercent:
            w = int(self.boss.rect.width * self.percent)
            h = 5
            pygame.draw.rect(self.image, red, (1,1,self.boss.rect.width-2,h)) # fill black
            pygame.draw.rect(self.image, green, (1,1,w,h)) # fill green
        self.oldpercent = self.percent
        self.rect.centerx = self.boss.rect.centerx
        self.rect.centery = (self.boss.rect.centery - self.boss.rect.height /2) - 10  # top - 10

class Tank(pygame.sprite.Sprite):
    size = 100
    recoiltime = 1 #0.75 # how many seconds the cannon is busy after firing one time
    MGrecoiltime = 0.1 # how many seconds the bow(machine gun) is idel
    turretTurnSpeed = 1
    tankTurnSpeed = 1 # degrees
    movespeed = 25.0 * 2
    book = {} # a book of tanks to store all tanks
    number = 0
    color = ((200,200,0),(0,0,200) )
    msg = ['wasd LCTRL, ijkl','Keypad: 4852, ENTER, cursor']
    folder = 'data'

    def __init__(self,world,startpos=(150,150),angle=0):
        self.world = world
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.color = Tank.color[self.number]
        self.number = Tank.number
        Tank.number += 1
        Tank.book[self.number] = self
        self.setKeys()
        self.makeTank(startpos,angle)
        self.turret = Turret(self) # create a Turret for this thank
        self.gethit = False
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
        self.movespeed = Tank.movespeed
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
        if abs(diffAngle) < 1: self.turndirection = 0
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
        self.bullet = Bullet(self)
        self.world.cannonsound.play()
        self.cooltime = Tank.recoiltime # seconds until tank can fire again
        self.ammo -= 1

    def fireMG(self,pressedkeys):
        # -- fire bow MG --
        doFireMG = self.MGcooltime <= 0 and self.MGammo > 0 and pressedkeys[self.MGfirekey]
        if not doFireMG: return
        # fire Machine Gun
        self.tracer = Tracer(self)
        self.world.mg2sound.play()
        self.MGcooltime = Tank.MGrecoiltime
        self.MGammo -= 1
        #self.msg = "player%i: ammo: %i/%i keys: %s" % (self.number+1, self.ammo, self.MGammo, Tank.msg[self.number])
        #Text.book[self.number].newMsg(self.msg)

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

    def checkHit(self):
        if self.gethit:
            print 'gethit'
            self.world.hitsound.play()
            self.health -= 10
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
        self.width  = 2 * self.boss.width        
        self.height = 2 * self.boss.height
        self.images = {} # how much recoil after shooting, reverse order of apperance
        for i in range(10):
            self.images[i]= drawCannon(self.width,self.height,i)
        self.images[10] = drawCannon(self.width,self.height,0) # idle position

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
 

class Fragment(pygame.sprite.Sprite):
    """a fragment of an exploding Bird"""
    gravity = True # fragments fall down ?
    def __init__(self, Vp):
        pygame.sprite.Sprite.__init__(self, self.groups)
        r = random.randint(128-100,128+100)
        g = random.randint(128-100,128+100)
        b = random.randint(128-120,128+120)
        randomcolor = g,g,g
        self.makeImage(4,4,randomcolor)
        self.Vp = Vp
        self.setPosition()
        self.setDirection(maxspeed=20)
        self.lifetime = 0.1 + 0.5*random.random() # max 6 seconds
        self.time = 0.0
    def makeImage(self,w,h,randomcolor):
        self.image = pygame.Surface((w,h))
        self.image.set_colorkey(black) # black transparent
        randomradius = random.randint(1,w/2)
        pygame.draw.circle(self.image, randomcolor, (w/2,h/2), randomradius)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
    def setDirection(self,maxspeed):
        self.Vd = Vector()
        self.Vd.x = random.randint(-maxspeed,+maxspeed)
        self.Vd.y = random.randint(-maxspeed,+maxspeed)
    def setPosition(self):
        self.rect.center = tuple(self.Vp)
    def update(self, seconds):
        self.time += seconds
        self.Vp += self.Vd * seconds
        self.setPosition()
        if self.time > self.lifetime:
            self.kill() 

class Explosion(Fragment):
    def __init__(self,Vp):
        Fragment.__init__(self,Vp)
        r = random.randint(128-100,128+100)
        randomcolor = r,0,0
        self.makeImage(40,40,randomcolor)
        self.setDirection(maxspeed=60)
        self.lifetime = 0.5 + 2*random.random() # max 6 seconds

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
    def kill(self):
        for _ in range(random.randint(5,10)):
            Fragment(self.Vp)
        if Bullet.book[self.number]:
            del Bullet.book[self.number]
            #Bullet.number -= 1
        pygame.sprite.Sprite.kill(self)


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
    def __init__(self,world):
        self.world = world
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.image = pygame.Surface( (radarmapwidth,radarmapheight) )
        self.paint()
        self.rect = self.image.get_rect()
        #self.rect.topleft  = screenwidth - radarmapwidth,0
        screenrect = self.world.screen.get_rect()
        self.rect.topleft  = screenrect.left,screenrect.bottom-radarmapheight
        self.factorX = 1.0*radarmapwidth/bigmapwidth
        self.factorY = 1.0*radarmapheight/bigmapheight
        self.Alive = False
        self.hideShow()
    def paint(self):
        self.image.fill(black)
        # draw dark red frame
        pygame.draw.rect(self.image,darkred1,(0,0,radarmapwidth,radarmapheight),1)

    def event(self,event):
        if event.key == pygame.K_m:
            self.Alive = not self.Alive
        self.hideShow()

    def hideShow(self):
        if self.Alive:
            self.add(self.groups)
        else:
            self.kill()

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

        for bullet in Bullet.groups[0]:
            print 'bullet =>',bullet, bullet.number

        for bulletNo in Bullet.book:
            #if Bullet.book[bulletNo]:
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

class Text(pygame.sprite.Sprite):
    number = 0
    book = {}
    def __init__(self,pos,msg):
        self.number = Text.number
        Text.number += 1
        Text.book[self.number] = self
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.pos = Vector(pos)
        self.newMsg(msg)
    def update(self,seconds):
        pass
    def newMsg(self,msg,color=black,fontsize=20):
        self.msg = msg
        self.image = write(msg,color,fontsize)
        self.rect = self.image.get_rect()
        self.rect.center = tuple(self.pos)

class Instruction(pygame.sprite.Sprite):
    number = 0
    book = {}
    def __init__(self,world,color=black,fontsize=20):
        self.world = world
        self.number = Instruction.number
        Instruction.number += 1
        Instruction.book[self.number] = self
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.width,self.height = screenwidth-100, screenheight-100
        self.draw()
        self.setPosition()
        self.F1 = False
        self.kill()
    def setPosition(self):
        screenrect = self.world.screen.get_rect()
        self.rect.center = screenrect.center
    def write(self,msg,color,fontsize):
        # text 
        msgsurf = write(msg,purple,24)
        msgrect = msgsurf.get_rect()
        msgrect.topleft = 20,60
        self.image.blit(msgsurf,msgrect)
    def event(self,e):
        if e.key == pygame.K_F1:
            self.F1 = not self.F1
        if self.F1:
            self.add(self.groups)
        else:
            self.kill()
    def update(self,seconds):
        pass
    def drawText(self,topleft,msg,color=black,fontsize=18):
        # draw text
        textsurf = write(msg,color,fontsize)
        textrect = textsurf.get_rect()
        textrect.topleft = topleft
        self.image.blit(textsurf,textrect)

    def draw(self):
        w,h = self.width,self.height
        #w,h = screenwidth/2,screenheight/2
        self.image = pygame.Surface( (w,h) )
        self.image.fill(bgcolor)
        #self.image.set_colorkey(bgcolor)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        # draw coordinates
        pygame.draw.line(self.image,gridcolor,self.rect.midleft,self.rect.midright,1) # x-coord
        pygame.draw.line(self.image,gridcolor,self.rect.midtop,self.rect.midbottom,1) # y-coord
        # draw circle
        r = int(w/4)
        pygame.draw.circle(self.image,gridcolor,self.rect.center, r, 1)
        # draw angle
        vd = Vector(0,0)
        vd.x = cos(30*GRAD)
        vd.y = -sin(30*GRAD)
        pos1 = Vector(self.rect.center) + vd* r
        pos1 = int(pos1.x),int(pos1.y)
        print pos1
        pygame.draw.line(self.image,blue,self.rect.center,pos1,2)
        # draw frame
        pygame.draw.rect(self.image,gridcolor,self.rect,1)
        # x,y
        xsurf = write('x',blue,26)
        xrect = xsurf.get_rect()
        xrect.center = self.rect.right - 20, self.rect.centery
        self.image.blit(xsurf,xrect)
        ysurf = write('+y',blue,26)
        yrect = ysurf.get_rect()
        yrect.center = self.rect.centerx, self.rect.bottom - 20
        self.image.blit(ysurf,yrect)
        # draw Tank
        tanksurf,a,b = drawTank(w/8,h/8,green)
        tankrect = tanksurf.get_rect()
        tankrect.center = self.rect.center
        self.image.blit(tanksurf,tankrect)
        # draw Cannon
        cannonsurf = drawCannon(self.width/4,self.height/4)
        cannonrect = cannonsurf.get_rect()
        #pygame.draw.rect(cannonsurf,red,cannonrect,2) frame
        cannonrect.center = self.rect.center
        self.image.blit(cannonsurf,cannonrect)
        # Tank Forward direction
        dh=14; dw = dh*6
        drect = self.rect.centerx+r/2, self.rect.centery-dh/2,dw,dh
        drect = pygame.Rect(drect)
        pygame.draw.rect(self.image,red,drect)
        # draw Forward arrow
        endpoint = drect.midright[0]+14,drect.midright[1]
        toppoint = endpoint[0]-20,endpoint[1]- 14
        bottompoint = endpoint[0]-20,endpoint[1]+ 14
        pointlist = endpoint,toppoint,bottompoint
        pygame.draw.polygon(self.image,red,pointlist)
        self.drawText((20,20),'press F1 for Instructions',purple,22)
        self.drawText((20,50),'press M for Mini map',purple,22)
        self.drawText((20,100),'move Forward  : K',black)
        self.drawText((20,120),'move Backward : J',black)
        self.drawText((20,140),'rotate Tank Left: A',black)
        self.drawText((20,160),'rotate Tank Right: S',black)
        self.drawText((20,180),'rotate Cannon Left: D',black)
        self.drawText((20,200),'rotate Cannon Right: F',black)
        self.drawText((20,220),'fire Cannon: SPACE',black)
        self.drawText((20,240),'fire Machine Gun: L',black)
