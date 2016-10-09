''' 004 per-pixel alphademo.py
Experiments with alpha values
use mouse and scrollwheel
'''

import pygame,os,itertools

white = pygame.Color('white')
red = pygame.Color('red')
black = pygame.Color('black')
yellow = pygame.Color('yellow')

def loadimage(name,path='data'):
    img = pygame.image.load(os.path.join(path,name)) 
    if img.get_alpha():
        return img.conver_alpha()
    return img.convert()

def check(x, minval=0, maxval=255):
    return min(maxval, max(minval,x))

def offset(len1,len2):
    # for picture centering
    return max( 0, (len1-len2)//2 )
    

class PeepDemo(object):
    def __init__(self, **opts):
        pygame.init()
        self.width,self.height = opts['width'],opts['height']
        self.clock = pygame.time.Clock()
        self.fps = opts['fps']
        self.screen = pygame.display.set_mode( (self.width,self.height), pygame.DOUBLEBUF)
        pygame.display.set_caption('Move mouse and scroll mouse wheel')
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill( opts['bgcolor'] )
        self.ppasurface = pygame.Surface(self.screen.get_size(), flags=pygame.SRCALPHA)

        self.image = loadimage( opts['image'] )
        self.imageoffset = offset( self.width, self.image.get_width() ),\
                           offset( self.height, self.image.get_height())
        # init for circles with alpha
        self.center = self.width/2, self.height/2
        self.maxradius = min(self.width,self.height)
        self.holecount = opts['holes']
        self.calCenters( self.center, self.center, self.holecount )
        self.calRadAlphas( self.maxradius, self.holecount )

    def calRadAlphas(self, radius, n):
        # calculate linear radius and alpha values
        assert 0<n<256, 'Invalid number of holes'
        radstep = radius/n
        alphastep = 256/n
        self.radalphas = [ (radius - i*radstep, 255 - i*alphastep) for i in xrange(n) ]

    def calCenters(self,center,pos,holes):
        # calculate center points from center of window to move position
        centerX,centerY = center
        moveX,moveY = pos
        vx,vy = moveX - centerX, moveY - centerY
        xs,ys = vx/holes, vy/holes
        self.centers = [ (centerX + i*xs, centerY + i*ys) for i in xrange(holes) ]

    def run(self): 
        mainloop = True
        while mainloop:
            self.flip()
            # event handler
            for e in pygame.event.get():
                if e.type == pygame.QUIT or \
                   e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    mainloop = False
                elif e.type == pygame.MOUSEMOTION:
                    self.calCenters(self.center, pygame.mouse.get_pos(), self.holecount)
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    # check mouse wheel
                    if e.button in (4,5):
                        self.holecount = check(self.holecount+[-1,1][e.button-4], 2, 64)
                        self.calRadAlphas(self.maxradius, self.holecount)
                        self.calCenters(self.center, pygame.mouse.get_pos(), self.holecount)
            self.show()
        pygame.quit()

    def show(self): # draw all
        # picture on screen
        self.screen.blit(self.image,self.imageoffset)
        # circles on alpha surface
        for (radius,alpha), center in zip(self.radalphas,self.centers):
            pygame.draw.circle( self.ppasurface, (0,0,0,alpha), center, radius)
        # alpha surface on screen
        self.screen.blit( self.ppasurface,(0,0))
        # ease alpha surface for new circles
        self.ppasurface.fill(black)

    def flip(self): # show drawing and erase
        pygame.display.flip()
        self.screen.blit(self.background,(0,0))
        self.clock.tick(self.fps)

# ----------- opts ---------------
opts = {'width':800, 'height':600, 'bgcolor': red, 'fps':100,
        'fontsize': 18, 'image':'ente.jpg', 'holes': 7 }

if __name__ == '__main__':
    PeepDemo(**opts).run()


                 






