import pygame,random,os
from math import pi,sin,cos,atan,atan2
from colors import *
from vector import Vector
# game constants
#fps = 1
# config
fps = 60
xtiles,ytiles = 15,15
folder = 'data'
GRAD = 2*pi/360
bgcolor = lightgray
gridcolor = gray
bigmapwidth = 1024
bigmapheight = 800
title = "Esc: quit"
scrollstepx = 3 # how many pixels to scroll when pressing cursor key
scrollstepy = 3 # how many pixels to scroll when pressing cursor key
cornerpoint = [0,0] # left upper edge of visible screen rect inside bigmap
radarmapwidth = 200
radarmapheight = 150


# initialize pygame
pygame.mixer.pre_init(44100,-16,2,2048)
pygame.init()
screensize = screenwidth,screenheight = 640,480
screensize = screenwidth,screenheight = 800,600
screen = pygame.display.set_mode( screensize )
screenrect = screen.get_rect()
background = pygame.Surface((screen.get_size()))
background.fill(bgcolor) # fill grey light blue:(128,128,255) 
background = background.convert()
# paint a grid of white lines
for x in range(0,screenwidth,screenwidth/xtiles): #start, stop, step
    pygame.draw.line(background,gridcolor, (x,0), (x,screenheight))
for y in range(0,screenheight,screenheight/ytiles): #start, stop, step
    pygame.draw.line(background,gridcolor, (0,y), (screenwidth,y))
# paint upper rectangle to have background for text
pygame.draw.rect(background,lightgray, (0,0,screenwidth, 70))
screen.blit(background, (0,0)) # delete all
clock = pygame.time.Clock()    # create pygame clock object

# KEYs for tank control
MGfirekey   = (pygame.K_l, pygame.K_KP_ENTER)
firekey     = (pygame.K_SPACE,pygame.K_DOWN)
tankLeftkey     = (pygame.K_a, pygame.K_KP4)
tankRightkey    = (pygame.K_s, pygame.K_KP6)
turretLeftkey  = (pygame.K_d, pygame.K_LEFT)
turretRightkey = (pygame.K_f, pygame.K_RIGHT)
forwardkey      = (pygame.K_k, pygame.K_KP8)
backwardkey     = (pygame.K_j, pygame.K_KP5)
#TankKeys = [firekey,MGfirekey,turrectLeft,turretRightkey,forwardkey,backwardkey,tankLeftkey,tankRightkey]

#self.drawText((20,60),'move Forward  : K',black)
#self.drawText((20,80),'move Backward : J',black)
#self.drawText((20,100),'rotate Tank Left: A',black)
#self.drawText((20,120),'rotate Tank Right: S',black)
#self.drawText((20,140),'rotate Cannon Left: D',black)
#self.drawText((20,160),'rotate Cannon Right: F',black)
#self.drawText((20,180),'fire Cannon: SPACE',black)
#self.drawText((20,200),'fire Machine Gun: L',black)

# ---------- load sound -----------
cannonsound = pygame.mixer.Sound(os.path.join(folder,'cannon.ogg'))
mg1sound = pygame.mixer.Sound(os.path.join(folder,'mg1.ogg'))
mg2sound = pygame.mixer.Sound(os.path.join(folder,'mg2.ogg'))
mg3sound = pygame.mixer.Sound(os.path.join(folder,'mg3.ogg'))
#hitsound = pygame.mixer.Sound(os.path.join(folder,'beep.ogg'))

# game constants
BIRDSPEEDMAX = 200
FRAGMENTMAXSPEED = 200
FRICTION = 0.999
FORCEOFGRAVITY = 2.81 # in pixel per seconds

def drawTank(width,height,color):
    w,h = width,height
    image = pygame.Surface( (w,h) )
    image.fill(gray)
    color1 = (90,90,190)
    # tank decoration
    rect = image.get_rect()
    bodyrect  = (rect.left+5,rect.top+5),(w-10,h-10)
    toprect   = rect.topleft,(w,h/6)
    bottomrect = (rect.left,rect.bottom-h/6), (w,h/6)
    # draw body
    pygame.draw.rect(image,color,bodyrect) # tank body, margin 5
    # draw topside
    pygame.draw.rect(image,color1,toprect) # tank left
    # draw bottomside
    pygame.draw.rect(image,color1,bottomrect) # right track
    # draw Machine Gun
    r = 8
    ir = 5
    MGcenter = rect.right - w/6, rect.top + h/6 + r
    MGrect = (MGcenter[0],MGcenter[1]-ir/2), (3*ir,ir)
    MGrect = pygame.Rect(MGrect)
    pygame.draw.circle(image,blue,MGcenter,r,2)    # outer circle for MG
    pygame.draw.circle(image,darkblue,MGcenter,ir) # inner circle for MG
    pygame.draw.rect(image,darkblue,MGrect)        # blue rect for MG
    # draw rec Circle for turret
    center = (w/2,h/2)
    cr = w/3
    pygame.draw.circle(image,red,center,cr,2) # red circle for turret
    #image = pygame.transform.rotate(image,-90) # rotate so as to look EAST
    Vc = Vector(MGcenter) - Vector(rect.center)
    print 'MGcenter:',MGcenter, rect.center
    return image,MGcenter,Vc

#def drawCannon(boss, offset):
     #width,height = 2*boss.width,2*boss.height
def drawCannon(width,height, offset=0):
     # painting facing right, offset is the recoil
     image = pygame.Surface((width,height)) # created on the fly
     rect = image.get_rect()
     image.fill(gray) # fill grey
     image.set_colorkey(gray)
     #pygame.draw.rect(image, green,  (1,1,width-2,height-2),1)
     pygame.draw.circle(image, red,   rect.center, 22) # red circle
     pygame.draw.circle(image, green, rect.center, 18) # green circle
     # turrect MG rectangle
     pygame.draw.rect(image, blue, (rect.centerx-10,rect.centery+10,25,4) ) # (width/2-10,height/2+10, 15,2))
     # green cannon
     h = 12
     cannonrect = rect.centerx-20-offset,rect.centery-h/2, width/2-offset,h
     pygame.draw.rect(image,green,cannonrect)
     # red rect
     pygame.draw.rect(image,red,cannonrect,2)
     #(width-20-offset,height-5, width-offset,10),1)
     return image

def toRadian(degree):
    return degree * 2*pi/360
 
def pressedKeysString():
    """returns the pressed keys (for the player1 tank) to be displayd in the status line"""
    pressedkeys = pygame.key.get_pressed()
    line = ""
    if pressedkeys[pygame.K_a]: line += "a "
    if pressedkeys[pygame.K_d]: line += "d "
    if pressedkeys[pygame.K_j]: line += "j "
    if pressedkeys[pygame.K_k]: line += "k "
    if pressedkeys[pygame.K_LCTRL]: line += "LCTRL"
    if pressedkeys[pygame.K_SPACE]: line += "SPACE"
    return line

def write(msg='pygame is cool',color=black,fontsize=20):
    font = pygame.font.SysFont('Arial',fontsize)
    textsurf = font.render(msg,True,color)
    textsurf = textsurf.convert_alpha()
    return textsurf
def getClassName(classinstance):
    # this function extract the class name of a instance of the class
    text = str(classinstance.__class__) # like <class '__main__.XWing'>
    parts = text.split('.') # [ <class '__main__, XWing'> ]
    return parts[-1][0:-2]  # take all except the last 2 charactors('>)

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
    def __init__(self,msg,color=black,fontsize=20):
        self.number = Instruction.number
        Instruction.number += 1
        Instruction.book[self.number] = self
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.width,self.height = screenwidth-100, screenheight-100
        self.draw()
        self.setPosition()
        self.write(msg,color,fontsize)
        self.F1 = False
        self.kill()
    def setPosition(self):
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
    def drawText(self,topleft,msg,color=black,fontsize=20):
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
        self.drawText((20,20),'Instructions',black,32)
        self.drawText((20,80),'move Forward  : K',black)
        self.drawText((20,100),'move Backward : J',black)
        self.drawText((20,120),'rotate Tank Left: A',black)
        self.drawText((20,140),'rotate Tank Right: S',black)
        self.drawText((20,160),'rotate Cannon Left: D',black)
        self.drawText((20,180),'rotate Cannon Right: F',black)
        self.drawText((20,200),'fire Cannon: SPACE',black)
        self.drawText((20,220),'fire Machine Gun: L',black)

if __name__ == '__main__':

    mainloop = True
    tanksurf,mgcenter,vc = drawTank(100,100,green)
    tanksurf = tanksurf.convert_alpha()
    tankrect = tanksurf.get_rect()
    tankrect.center = screenrect.center
    instsurf = drawInstruction(screenwidth-100,screenheight-100)
    instrect = instsurf.get_rect()
    instrect.center = screenrect.center
    #cannonsurf = drawCannon(None
    needhelp = False
    while mainloop:
        background.fill(bgcolor)
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    mainloop = False
                elif e.key == pygame.K_F1:
                    needhelp = not needhelp
        #background.fill(bgcolor)
        if needhelp:
            background.blit(instsurf,instrect)
        background.blit(tanksurf,tankrect)
        screen.blit(background,(0,0) )
        pygame.display.flip()
        clock.tick(fps)

