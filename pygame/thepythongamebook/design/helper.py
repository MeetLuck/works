''' Minimap and Status '''
from constants import *
from Tank import *

radarmapwidth = 200
radarmapheight = 150

bigmapwidth = 1024
bigmapheight = 800

cornerpoint = [0,0] # left upper edge of visible screen rect inside bigmap

class Minimap(pygame.sprite.Sprite):
    def __init__(self,world):
        self.world = world
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.image = pygame.Surface( (radarmapwidth,radarmapheight) )
        self.paint()
        self.factorX = 1.0*radarmapwidth/bigmapwidth
        self.factorY = 1.0*radarmapheight/bigmapheight
        self.Show = False
        self.hideShow()

    def setPosition(self):
        dy = int(self.world.screenheight/10)
        screenrect = self.world.screen.get_rect()
        self.rect.topleft  = screenrect.left, screenrect.bottom-radarmapheight-dy-10 

    def paint(self):
        self.image.fill(black)
        # draw dark red frame
        pygame.draw.rect(self.image,darkred1,(0,0,radarmapwidth,radarmapheight),1)
        self.rect = self.image.get_rect()
        self.setPosition()

    def event(self,event):
        if event.key == pygame.K_m:
            self.Show = not self.Show
        self.hideShow()

    def hideShow(self):
        if self.Show:
            self.add(self.groups)
        else:
            self.kill()

    def update(self,seconds):
        self.paint()
        screenwidth,screenheight = self.world.screensize
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
