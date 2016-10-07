'''
002 display fps.py
open a pygame window and display framerate
URL    : http://thepythongamebook.com/en:part2:pygame:step002
Author : horst.jens@spielend-programmieren.at
License: GPL, see http://www.gnu.org/licenses/gpl.html
'''
# the next line is only needed for python2.x
from __future__ import print_function, division
import pygame
# initialize pygame
pygame.init()
# set size of pygame window
screen = pygame.display.set_mode( (640,480) )
# creae empty pygame surface
background = pygame.Surface(screen.get_size())
# fill the background white color
background.fill( pygame.Color('white') )
# convert Surface object to make blitting faster
background = background.convert()
# copy background to screen
screen.blit(background,(0,0))
# create pygame clock object
clock = pygame.time.Clock()

mainloop = True
# desired frame rate in Frames Per Second
fps = 30
# how many seconds the game is play
playtime = 0.0
while mainloop:
    # do not go faster than this framerate
    miliseconds = clock.tick(fps)
    playtime += miliseconds/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
    # print framerate and playtime in tilebar
    text = 'FPS: {0: .2f}    Playtime: {1: .2f}'.format(clock.get_fps(), playtime)
    pygame.display.set_caption(text)
    # update pygame display
    pygame.display.flip()

# finish pygame
pygame.quit()
# at the very last:
print("This game was played for {:.2f} seconds".format(playtime) )

