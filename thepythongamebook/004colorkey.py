'''
004colorkey.py
dynamic blitting and colorkey
blitting one surface on 2 static positions, once before the mainloop and once inside the mainloop
using colorkey to make a part of the surfaces transparent
blitting lines on the screen to create a colourful patter like in a screensaver
'''
import pygame, random
pygame.init()
screen = pygame.display.set_mode((640,480))
# colors
white = pygame.Color('white')
black = pygame.Color('black')
blue = pygame.Color('blue')
# background surface
background = pygame.Surface(screen.get_size())
background.fill(white)
ballsurface = pygame.Surface((50,50))
ballsurface.set_colorkey(black) # make black the transparent color
pygame.draw.circle(ballsurface,blue,(25,25), 25)
ballsurface = ballsurface.convert_alpha() # for transparency
screen.blit(background,(0,0))
ballpos1 = 20,240
screen.blit(ballsurface, ballpos1)  #draw the ball surface (lines will draw over this ball)
ballpos2 = 400,380
clock = pygame.time.Clock()
mainloop = True
fps = 35
playtime = 0.0
t = 0 # used to draw a pattern
color1,color2 = 0,0

while mainloop:
    msec = clock.tick(fps)
    playtime += msec/1000.0
    # event handler
    for e in pygame.event.get():
        if e.type == pygame.QUIT or \
           e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            mainloop = False
    #-------- draw cute pattern ----------
    pygame.draw.line(screen,(color1,255-color1,color2),(32*t,0),(0,480-24*t))
    pygame.draw.line(screen,(color1,color2,255-color1),(32*t,480),(640,480-24*t))
    screen.blit(ballsurface,ballpos2)
    t += 1 
    if t>20:
        t = 0 # reset t
        color1,color2 = random.randint(0,255), random.randint(0,255)
    #---------- end of cute pattern drawing code ---------------
    pygame.display.set_caption("Frame rate %.2f frames per second. Playtime: %.2f seconds"
                                % (clock.get_fps(),playtime) )  
    pygame.display.flip()          # flip the screen 30 times a second
print "This 'game' was played for %.2f seconds." % playtime



