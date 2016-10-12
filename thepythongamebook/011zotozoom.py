''' 011rotozoom.py
the snake surface can be moved with the ARROW keys
rotated with A and D key and zoomed with W and S key
'''

import pygame, os

mainloop = True
fps = 60
class Snake:
    # constants
    ZOOMSPEED = 0.01
    TURNSPEED = 30
    SPEED = 160
    def __init__(self,snakesurf):
        self.surf = snakesurf
        self.surforigin = snakesurf.copy()
        self.startpos = 250,250
        self.x,self.y = self.startpos
        self.angle = 0.0
        self.turnfactor = 0.0
        self.zoom = 1.0
        self.zoomfactor = 1.0
    @property
    def pos(self):
        self._pos = int(self.x), int(self.y)
        return self._pos 
    def Move(self,pressedkeys,period):
        'move during KEYDOWN, stop if KEYUP' 
        movespeed = self.SPEED * period
        if pressedkeys[pygame.K_LEFT]:    self.x -= movespeed
        if pressedkeys[pygame.K_RIGHT]:   self.x += movespeed
        if pressedkeys[pygame.K_UP]:      self.y -= movespeed
        if pressedkeys[pygame.K_DOWN]:    self.y += movespeed
        #print 'pos: {pos} speed: {speed}'.format(pos=self.pos, speed=movespeed)
    def Turn(self,pressedkeys,period):
        # rotate snake with a A and D key
        if pressedkeys[pygame.K_a]:     self.turnfactor += 1 # counter-clockwise
        if pressedkeys[pygame.K_d]:     self.turnfactor -= 1 # clockwise
        self.angle += self.turnfactor * self.TURNSPEED * period
        self.transform(self.angle,self.zoom)
        self.turnfactor = 0

    def Zoom(self,pressedkeys,period):
        # zoom snake with W and S key
        if pressedkeys[pygame.K_w]:     self.zoomfactor += self.ZOOMSPEED
        if pressedkeys[pygame.K_s]:     self.zoomfactor -= self.ZOOMSPEED 
        self.zoom  *= self.zoomfactor
        self.transform(self.angle,self.zoom)
        self.zoomfactor = 1

    def transform(self, angle,scale):
        #print 'angle:', self.angle, 'scale:',self.zoom
        snakeoldrect = self.surf.get_rect()
        # NEW snake surf made by turning or zooming original snakesurf
        self.surf = pygame.transform.rotozoom(self.surforigin, angle, scale )
        snakenewrect = self.surf.get_rect()
        # put new surface center on the same spot as old surface center
        self.x += snakeoldrect.centerx - snakenewrect.centerx
        self.y += snakeoldrect.centery - snakenewrect.centery

    def control(self,pressedkeys,period):
        self.Move(pressedkeys,period)
        self.Turn(pressedkeys,period)
        self.Zoom(pressedkeys,period)

    def draw(self,screen):
        screen.blit( self.surf, self.pos ) #(round(snake.x,0), round(snake.y,0)) )
    

def main():
    # initialize pygame
    pygame.init()
    screen = pygame.display.set_mode( (640,480) )

    bgsurf = pygame.image.load(os.path.join("data","background640x480_a.jpg"))
    bgsurf = bgsurf.convert()
    snakesurf = pygame.image.load(os.path.join("data","snake.gif"))
    snakesurf = snakesurf.convert_alpha()

    snake = Snake(snakesurf)

    screen.blit(bgsurf,(0,0))
    screen.blit(snakesurf, snake.startpos)
    clock = pygame.time.Clock()

    mainloop = True
    while mainloop:
        miliseconds = clock.tick(fps) # miliseconds passed since last frame
        period = miliseconds/1000.0
        for e in pygame.event.get():
            if e.type == pygame.QUIT or \
               e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                mainloop = False
        pygame.display.set_caption("press arrow keys and w a s d - fps:"
            "%.2f zoom: %.2f angle %.2f" % (clock.get_fps(), snake.zoom, snake.angle))
        # move snake according to pressed key
        pressedkeys = pygame.key.get_pressed()
        snake.control(pressedkeys, period)
        # paint snake
        screen.blit( bgsurf,(0,0) )
        snake.draw(screen)
        pygame.display.flip()

if __name__ =='__main__':
    main()
