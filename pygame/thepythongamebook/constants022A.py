import pygame,random,os
from math import pi,sin,cos,atan,atan2
from colors import *
from vector import Vector
# game constants
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
screensize = screenwidth,screenheight = 640,480
screensize = screenwidth,screenheight = 800,600

# game constants
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

