import pygame,random,os
from math import pi,sin,cos,atan,atan2
from random import randint
from colors import *
from vector import Vector
import logging

# logging
LOG_FILENAME = 'ai.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG,)

# game constants
GRAD = 2*pi/360
bgcolor = lightgray
gridcolor = gray
#scrollstepx = 3 # how many pixels to scroll when pressing cursor key
#scrollstepy = 3 # how many pixels to scroll when pressing cursor key
#cornerpoint = [0,0] # left upper edge of visible screen rect inside bigmap

# game constants
FRAGMENTMAXSPEED = 200
FRICTION = 0.999
FORCEOFGRAVITY = 2.81 # in pixel per seconds

def drawTank(width,height,color):
    w,h = width,height
    image = pygame.Surface( (w,h) )
    image.fill(bgcolor)
    # Tank color: blue for player, red for Ai
    if len(color)==4:
        r,g,b,a = color
    elif len(color)==3:
        r,g,b = color
    darkness = 0.6
    bodycolor = color
    if b>0: # player
        b = int(b*darkness)
        topcolor = 0,0,b
        bottomcolor = topcolor
        MGoutercolor = 255*0.8,32*2,0
        MGcolor = red
        MGinnercolor = MGcolor
        turretcolor = red
    else:  # ai
        r = int(r*darkness)
        topcolor = r,0,0
        bottomcolor = topcolor
        MGoutercolor = 0,32*2,255*0.8
        MGcolor = blue
        MGinnercolor = MGcolor
        turretcolor = blue
    # tank decoration
    rect = image.get_rect()
    bodyrect  = (rect.left+5,rect.top+5),(w-10,h-10)
    toprect   = rect.topleft,(w,h/6)
    bottomrect = (rect.left,rect.bottom-h/6), (w,h/6)
    # draw body
    pygame.draw.rect(image,bodycolor,bodyrect) # tank body, margin 5
    # draw topside
    pygame.draw.rect(image,topcolor,toprect) # tank left
    # draw bottomside
    pygame.draw.rect(image,bottomcolor,bottomrect) # right track
    # draw Machine Gun
    r = 8
    ir = 4
    MGcenter = rect.right - w/6, rect.top + h/6 + r
    MGrect = (MGcenter[0],MGcenter[1]-ir/2), (12*ir,ir)
    MGrect = pygame.Rect(MGrect)
    pygame.draw.circle(image,MGoutercolor,MGcenter,r,4)    # outer circle for MG
    pygame.draw.circle(image,MGinnercolor,MGcenter,ir) # inner circle for MG
    pygame.draw.rect(image,MGcolor,MGrect)        # blue rect for MG
    # draw rec Circle for turret
    center = (w/2,h/2)
    cr = w/3
    pygame.draw.circle(image,turretcolor,center,cr,2) # red circle for turret
    #image = pygame.transform.rotate(image,-90) # rotate so as to look EAST
    Vc = Vector(MGcenter) - Vector(rect.center)
    print 'MGcenter:',MGcenter, rect.center
    return image,MGcenter,Vc

def drawCannon(color,width,height,offset=0):

    # painting facing right, offset is the recoil
    image = pygame.Surface((width,height)) # created on the fly
    rect = image.get_rect()
    image.fill(bgcolor) # fill grey
    image.set_colorkey(bgcolor)
    #pygame.draw.rect(image, green,  (1,1,width-2,height-2),1)
    print color
    r,g,b,a = color
    if r>0:
        innercolor = int(r*0.7), 0, 32*2
    else:
        innercolor = 32*2, 0, int(b*0.7)

    pygame.draw.circle(image, green,   rect.center, 18) # red circle
    pygame.draw.circle(image, innercolor, rect.center, 16) # green circle
    # turrect MG rectangle
    pygame.draw.rect(image, color, (rect.centerx-10,rect.centery+10,25,4) ) # (width/2-10,height/2+10, 15,2))
    # green cannon
    h = 12
    cannonrect = rect.centerx-20-offset,rect.centery-h/2, width/2-offset,h
    pygame.draw.rect(image,color,cannonrect)
    # red rect
    pygame.draw.rect(image,innercolor,cannonrect,2)
    #(width-20-offset,height-5, width-offset,10),1)
    return image

def toRadian(degree):
    return degree * 2*pi/360
 
def pressedKeysString():
    """returns the pressed keys (for the player1 tank) to be displayd in the status line"""
    pressedkeys = pygame.key.get_pressed()
    line = ""
    if pressedkeys[pygame.K_a]: line += "a "
    if pressedkeys[pygame.K_s]: line += "d "
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

if __name__ == '__main__':
    screensize = screenwidth,screenheight = 1024,768
    mainloop = True
    pygame.init()
    screen = pygame.display.set_mode( screensize )
    screenrect = screen.get_rect()
    background = pygame.Surface((screen.get_size()))
    background.fill(bgcolor) # fill grey light blue:(128,128,255) 
    background = background.convert()
    clock = pygame.time.Clock()    # create pygame clock object
    # draw tank
    tanksurf,mgcenter,vc = drawTank(100,100,blue)
    tanksurf = tanksurf.convert_alpha()
    tankrect = tanksurf.get_rect()
    tankrect.center = (screenwidth/2)/2, screenheight/2
    # draw Ai
    aisurf,mgcenter,vc = drawTank(100,100,red)
    aisurf = aisurf.convert_alpha()
    airect = aisurf.get_rect()
    airect.center = (screenwidth/2)*3/2, screenheight/2
    #instsurf = drawInstruction(screenwidth-100,screenheight-100)
    #instrect = instsurf.get_rect()
    #instrect.center = screenrect.center
    #cannonsurf = drawCannon(None
    needhelp = False
    fps = 60
    while mainloop:
        background.fill(bgcolor)
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    mainloop = False
                elif e.key == pygame.K_F1:
                    needhelp = not needhelp
        #background.fill(bgcolor)
#       if needhelp:
#           background.blit(instsurf,instrect)
        background.blit(tanksurf,tankrect)
        background.blit(aisurf,airect)
        screen.blit(background,(0,0) )
        pygame.display.flip()
        clock.tick(fps)

