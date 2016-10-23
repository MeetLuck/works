import pygame, sys
from colors import *

def write(msg='pygame is cool',color=darkblue):
    font = pygame.font.SysFont('Anonymous Pro',14)
    textsurf = font.render(msg,True,color)
    textsurf = textsurf.convert_alpha()
    return textsurf

class Test:
    def __init__(self,screen):
        self.screen = screen
        self.width,self.height = 200,100
        self.surf = pygame.Surface( (self.width,self.height))
        # make black transparent
        self.surf.set_colorkey(black)
        self.rect = self.surf.get_rect()
    def draw(self):
        outer_rect = 1,1,self.width-2, self.height-2
        # draw outer frame
        pygame.draw.rect(self.surf,green,outer_rect,2)
        # draw origin 
        pygame.draw.circle(self.surf,red,self.rect.center,5,2)
        self.rect.center = self.screen.get_rect().center
        self.screen.blit(self.surf,self.rect)


def main():
    pygame.init()
    screensize = screenwidth,screenheight = 640,480
    screen = pygame.display.set_mode(screensize)
    screenrect = screen.get_rect()
    clock = pygame.time.Clock()
    fps = 60

    # test object
    test = Test(screen)

    mainloop = True

    while mainloop:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                mainloop = False #pygame.quit(); sys.exit()

        screen.fill(white)
        pygame.draw.line(screen,darkgray,screenrect.midleft, screenrect.midright,1)
        pygame.draw.line(screen,darkgray,screenrect.midtop, screenrect.midbottom,1)
        # top,bottom,left,right, midtop
        screen.blit( write('top',red),(test.rect.centerx-15,test.rect.top-20) )
        screen.blit( write('bottom',red),(test.rect.centerx-25,test.rect.bottom+5) )
        screen.blit( write('left',red),(test.rect.left-40,test.rect.centery-20) )
        screen.blit( write('right',red),(test.rect.right+10,test.rect.centery-20) )
        # topleft,topright,bottomleft,bottomright
        screen.blit( write('topleft',red),(test.rect.left-20,test.rect.top-20) )
        screen.blit( write('topright',red),(test.rect.right,test.rect.top-20) )
        screen.blit( write('bottomleft',red),(test.rect.left-20,test.rect.bottom) )
        screen.blit( write('bottomright',red),(test.rect.right,test.rect.bottom) )

        # screen.get_rect(), top, bottom, right, left, center
        x = 20
        screen.blit( write('rect = '    + str(test.rect)),          (x,20) )
        screen.blit( write('top = '     + str(test.rect.top)),      (x,40) )
        screen.blit( write('bottom = '  + str(test.rect.bottom)),   (x,60) )
        screen.blit( write('left = '    + str(test.rect.left)),     (x,80) )
        screen.blit( write('right = '   + str(test.rect.right)),    (x,100) )
        screen.blit( write('center = '  + str(test.rect.center)),   (x,120) )
        screen.blit( write('centerx,centery = '+str(test.rect.centerx)+','+str(test.rect.centery)), (x,140) )
        # x,y,w,h,width,height,size
        x,y = 40+screenwidth/2,20
        screen.blit( write('x = '     + str(test.rect.x)),      (x,y) )
        screen.blit( write('y = '     + str(test.rect.y)),      (x,y+20) )
        screen.blit( write('w = '     + str(test.rect.w)),      (x,y+40) )
        screen.blit( write('h = '     + str(test.rect.h)),      (x,y+60) )
        screen.blit( write('width = ' + str(test.rect.width)),  (x,y+80) )
        screen.blit( write('height = '+ str(test.rect.height)), (x,y+100) )
        screen.blit( write('size = '+ str(test.rect.size)),     (x,y+120) )
        # topleft,topright,bottomleft,bottomright
        x,y = 40,360
        screen.blit( write('topleft = '     + str(test.rect.topleft)),      (x,y) )
        screen.blit( write('topright = '    + str(test.rect.topright)),     (x,y+20) )
        screen.blit( write('bottomleft = '  + str(test.rect.bottomleft)),   (x,y+40) )
        screen.blit( write('bottomright = ' + str(test.rect.bottomright)),  (x,y+60) )
        # midtop, midbottom,midleft,midright
        x,y = 40,360
        screen.blit( write('midtop = '     + str(test.rect.midtop)),      (x+screenwidth/2,y) )
        screen.blit( write('midbottom = '  + str(test.rect.midbottom)),   (x+screenwidth/2,y+20) )
        screen.blit( write('midleft = '    + str(test.rect.midleft)),     (x+screenwidth/2,y+40) )
        screen.blit( write('midright = '   + str(test.rect.midright)),    (x+screenwidth/2,y+60) )

        test.draw()
        pygame.display.flip()
        clock.tick(fps)

if __name__ == '__main__':
    main()
