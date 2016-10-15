'''
003static_blit.py
static blitting and drawing

Blitting a surface on a static position
Drawing a filled circle into ballsurface
Blitting this surface once
Introducing pygame draw methods
The ball's rectangular surface is black because the background color of the ball's surface
was never defined nor filled
'''
import pygame
pygame.init()
screen = pygame.display.set_mode((640,480))
background = pygame.Surface( screen.get_size() )
background.fill(pygame.Color('white'))
background = background.convert()
ballsurface = pygame.Surface((50,50)) # create a rectangular surface for the ball
# pygame.draw.circle(surface, color, pos, radius, width=0)
# draw blue filled circle on the ball surface
pygame.draw.circle(ballsurface,pygame.Color('blue'),(25,25),25)
ballsurface = ballsurface.convert()
ballx,bally = 320,240
# try out some pygame draw functions
# http://www.pygame.org/docs/ref/draw.html
# pygame.draw.rect(surface,color,Rect,width=0): return Rect
# rect: x-position of topleft corner, y-position of topleft corner, width, height
pygame.draw.rect( background,(0,255,0),(50,50,200,50) )
# pygame.draw.circle(surface, color, pos, radius,width=0): return Rect
pygame.draw.circle( background,(0,200,0),(200,50),35 )
# pygame.draw.polygon(surface, color, pointlist, width=0): return Rect
pygame.draw.polygon(background,(0,180,0),((250,100),(300,0),(350,50)))
# pygame.draw.arc(surface, color, Rect, start_angle, stop_angle, width=1): return Rect
pygame.draw.arc(background,(0,150,0),(400,10,150,100),0,3.14)

#---- blit the surfaces on the screen to make them visible
screen.blit(background,(0,0))
screen.blit(ballsurface,(ballx,bally)) # blit the topleft corner of ball surface at pos ballx,bally
clock = pygame.time.Clock()
mainloop = True
fps = 30
playtime = 0.0

while mainloop:
    miliseconds = clock.tick(fps)
    playtime += miliseconds/1000.0
    # event handler
    for e in pygame.event.get():
        if e.type == pygame.QUIT or \
           e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            mainloop = False
    pygame.display.set_caption('Frame rate: {:0.2f} frames per seconds'
                               'Playtime: {:.2} seconds'.format(clock.get_fps(), playtime) )
    pygame.display.flip()
