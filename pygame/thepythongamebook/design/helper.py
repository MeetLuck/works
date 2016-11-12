from constants import *
from Tank import *

radarmapwidth = 200
radarmapheight = 150

class Minimap(pygame.sprite.Sprite):
    def __init__(self,world):
        self.world = world
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.image = pygame.Surface( (radarmapwidth,radarmapheight) )
        self.paint()
        self.rect = self.image.get_rect()
        #self.rect.topleft  = screenwidth - radarmapwidth,0
        self.setPosition()
        self.factorX = 1.0*radarmapwidth/bigmapwidth
        self.factorY = 1.0*radarmapheight/bigmapheight
        self.Alive = False
        self.hideShow()

    def setPosition(self):
        dy = int(self.world.screenheight/10)
        screenrect = self.world.screen.get_rect()
        self.rect.topleft  = screenrect.left, screenrect.bottom-radarmapheight-dy-10 

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

        for ballNo in CannonBall.book:
            pos = CannonBall.book[ballNo].Vp
            color = CannonBall.book[ballNo].color
            center2 = pos.x*self.factorX, pos.y*self.factorY
            dotsize = 6
            rect = pygame.Rect(0,0,dotsize,dotsize/2)
            rect.center = center2
            pygame.draw.rect(self.image,color, rect)

        for bulletNo in MGBullet.book:
            pos = MGBullet.book[bulletNo].Vp
            color = MGBullet.book[bulletNo].color
            center2 = pos.x*self.factorX, pos.y*self.factorY
            dotsize = 4
            rect = pygame.Rect(0,0,dotsize,dotsize/2)
            rect.center = center2
            pygame.draw.rect(self.image,color, rect)

class Status(pygame.sprite.Sprite):

    def __init__(self,world):
        self.world = world
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.width,self.height = world.screenwidth, world.screenheight/10
        self.drawImage()
        self.setPosition()

    def setPosition(self):
        self.rect.topleft = 0, self.world.screenheight - self.height

    def drawImage(self):
        w,h = self.width, self.height
        self.image = pygame.Surface((w,h))
        self.image.fill(bgcolor)
        self.image.set_colorkey(bgcolor)
        self.image = self.image.convert_alpha()
        self.rect  = self.image.get_rect()
        self.drawAIState()
        self.drawPlayerState()

    def drawPlayerState(self):
        player = self.world.getPlayer()
        x,y = 50,0
        if player:
            self.drawText((x,y),'Cannon: %s' %player.ammo,darkgreen)
            self.drawText((x,y+20),'Machine Gun: %s' %player.MGammo,limegreen)
        else:
            self.drawText((x,y+10),'You are killed')

    def drawAIState(self):
        x,y = self.width/2,0
        ai = self.world.getAi()
        if ai is None:
            self.drawText((x,y+10),'You Win')
            return
        player = self.world.getPlayer()
        if player:
            diffAngle = int( ai.getdiffAngle(player) )
            distance = int( ai.getDistanceToPlayer(player) )
        else:
            diffAngle,distance = 'nA','nA'
        activestate = ai.brain.activestate.name
        self.drawText((x,y),    'activestate: %s' %activestate,red)
        self.drawText((x,y+20), 'diffAngle: %s'   %diffAngle,darkgreen)
        self.drawText((x,y+40), 'distance: %s'    %distance,blue)
        self.drawText((x+300,y),'Cannon: %s'      %ai.ammo,pink)
        self.drawText((x+300,y+20),'Machine Gun: %s' %ai.MGammo,purple)

    def write(self,msg='pygame is cool',color=black,fontsize=20):
        font = pygame.font.SysFont('Arial Black',fontsize)
        textsurf = font.render(msg,True,color)
        textsurf = textsurf.convert_alpha()
        return textsurf

    def drawText(self,topleft,msg,color=black,fontsize=18):
        # draw text
        textsurf = self.write(msg,color,fontsize)
        textrect = textsurf.get_rect()
        textrect.topleft = topleft
        self.image.blit(textsurf,textrect)
    def update(self,seconds):
        self.image.fill(bgcolor)
        self.drawPlayerState()
        self.drawAIState()
        self.image.set_colorkey(bgcolor)
        self.image = self.image.convert_alpha()


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
        self.drawImage()
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

    def drawImage(self):
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

