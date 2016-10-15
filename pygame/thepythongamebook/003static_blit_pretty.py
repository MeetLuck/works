'''
003static_blit_pretty.py
static blitting and drawing(pretty version)

blitting a surface on a static position
drawing a filled cirucle into ballsurface
blitting this surface once
introducing pygame draw methods
the ball's rectangular surface is black because the background
color of the ball's surface was never defined nor filled
'''
import pygame
# colors 
black = pygame.Color('black')
white = pygame.Color('white')
red = pygame.Color('red')
green = pygame.Color('green')
blue = pygame.Color('blue')
pink = pygame.Color('pink')

class PygView(object):
    def __init__(self,width=640,height=480,fps=30):
        # initialize pygame, window, background, font, ...
        pygame.init()
        pygame.display.set_caption('Press ESC to quit')
        self.width,self.height = width,height
        self.screen = pygame.display.set_mode((self.width,self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill(pygame.Color('white'))
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont('mono',24,bold=True)
    def paint(self):
        import math
        # pygame.draw.line(surface,color,start,end,width)
        pygame.draw.line(self.background,green,(10,10),(50,100))
        # pygame.draw.rect(surface,color, Rect,width=0): return Rect
        pygame.draw.rect(self.background,green,(50,50,100,25) )  # rect = x1,y1,width,height
        # pygame.draw.circle(surface,color,pos,radius,width): return Rect
        pygame.draw.circle(self.background,pink,(200,150), 80,5)
        # pygame.draw.polygon(surface,color,pointlist,width): return Rect
        pygame.draw.polygon(self.background,red,[(250,100),(300,0),(350,50)],3)
        # pygame.draw.arc(surface,color,Rect,start_angle,stop_angle,width=1): return Rect
        pygame.draw.arc(self.background,blue,(400,10,150,100),0, 1.5* math.pi/4) # pi/2
        #--------- blitting a Ball -----------------
        ball = Ball() # create Ball object
        ball.blit(self.background)
    def run(self): # mainloop
        self.paint()
        running = True
        while running:
            # event handler
            for e in pygame.event.get():
                if e.type == pygame.QUIT or \
                   e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    running = False
            miliseconds = self.clock.tick(self.fps)
            self.playtime += miliseconds/1000.0
            self.drawText("FPS : {:6.2f}{}PLAYTIME : {} SECONDS".format(self.clock.get_fps(),' '*5, self.playtime) )
            self.screen.blit(self.background,(0,0))
            pygame.display.flip()
        pygame.quit()
    def drawText(self,text):
        # center text in window
        fw,fh = self.font.size(text) # font width,height
        textSurf = self.font.render( text, True, pygame.Color('white') )
        self.screen.blit(textSurf, (50,150))

class Ball(object):
    def __init__(self, radius=50,color=blue,x=320,y=240):
        # create a black surface and paint a blue ball on it
        self.pos = self.x,self.y = x,y
        # create a rectangular surface for the ball 50x50
        self.surface = pygame.Surface( (2*radius,2*radius) )
        pygame.draw.circle(self.surface,color,(radius,radius),radius) # draw blue filled circle on ball surface
        # to avoid the black background, make black the transparent color
        #self.surface.set_colorkey(black)
        # self.surface = self.surface.convert_alpha() # faster blitting with transparent color
    def blit(self,background):
        # blit the Ball on the background
        background.blit(self.surface, self.pos)

if __name__ == '__main__':
    PygView().run()




