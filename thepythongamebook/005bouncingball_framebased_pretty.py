from constants import *

def checkQuit(): # event handler
    for e in pygame.event.get():
        if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            return False
    return True

def randomColor():
    return random.randint(0,255),random.randint(0,255), random.randint(0,255)


class PygView(object):

    def __init__(self,width=800,height=600,fps=50):
        pygame.init()
        pygame.display.set_caption('Press ESC to quit')
        self.width,self.height = width,height
        self.screen = pygame.display.set_mode( (self.width,self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill(white)
        self.actsurf = self.screen
        self.actcolor = red

    def drawStatic(self):
        self.actsurf = self.background
    def drawDynamic(self):
        self.actsurf = self.screen
    def setColor(self,color):
        self.actcolor = color
    def drawCircle(self,x,y,radius,width): # allocate surface for blitting and draw circle
        diameter = 2*radius
        surf = pygame.Surface( (diameter, diameter) )
        pygame.draw.circle(surf, self.actcolor, (radius,radius), radius, width)
        surf.set_colorkey(black)
        self.actsurf.blit(surf.convert_alpha(), (x,y) )
    def run(self,animateBalls):
        mainloop = True
        while mainloop:
            mainloop = checkQuit()
            animateBalls()
            pygame.display.flip()
            self.screen.blit( self.background,(0,0) )
        pygame.quit()

class Ball(object):
    # a circle object with no hardcoded dependency on pygame and other libs too
    def __init__(self,x,y,radius,speedX=1,speedpulse=0,color=blue,width=0):
        self.x,self.y = x,y
        self.radius = radius
        self.actradius = radius
        self.speedX = speedX
        self.speedpulse = speedpulse
        self.color = color
        self.width = width
        self.shrinking = True
    @property
    def maxX(self):
        return self.x + 2*self.radius
    def relativeMove(self,deltaX,deltaY):
        self.x += deltaX
        self.y += deltaY
    def pulse(self):
        # shrink or expand ball
        if not self.speedpulse: return
        # balls are shrinking first
        if self.shrinking:
            if self.actradius > self.width:
                self.actradius = max(self.actradius-self.speedpulse, self.width)
            else:
                self.shrinking = False
        else:
            if self.actradius < self.radius:
                self.actradius += self.speedpulse
            else:
                self.shrinking = True
    def draw(self,view): # draw on a device with an appropriate interface
        if self.speedpulse:
            color = randomColor()
        else:
            color = self.color
        view.setColor(color)
        view.drawCircle(self.x,self.y, self.actradius, self.width)

def action(balls, width, view): # return a function for the pygame mainloop
    # balls move to the right first
    rightmoving = [True] * len(balls)
    def animateBalls():
        for i,ball in enumerate(balls):
            if rightmoving[i]:
                if ball.maxX < width:
                    ball.relativeMove(ball.speedX,0)
                else:
                    rightmoving[i] = False
            else:
                if ball.x > 0:
                    ball.relativeMove(-ball.speedX,0)
                else:
                    rightmoving[i] = True
            ball.pulse()
            ball.draw(view)
    return animateBalls

def main(width): 
    view = PygView(width)
    view.drawStatic()
    # args : x,y,radius,speedX,speedpulse,color,border_width
    # border_width <= radius
    ball01 = Ball(50,60,50,0,0,yellow)
    ball01.draw(view)
    ball02 = Ball(250,150,190,0,0,color02)
    ball02.draw(view)

    view.drawDynamic()
    ball1 = Ball(15,130,100,1,0, color1)
    ball2 = Ball(25,200,80, 2,0, color2)
    ball3 = Ball(20,220,110,1,1, color3)
    ball4 = Ball(20,400,70, 3,0, color4)
    ball5 = Ball(90,390,70, 0,1, color5,1)
    loopfunc = action( (ball1,ball2,ball4,ball5), width, view)
    view.run(loopfunc)


if __name__ == '__main__':
    main(900)



            



