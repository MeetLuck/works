# import pygame modules
import pygame,time
from pygame.locals import *
# basic screen initialisation
screen = pygame.display.set_mode((1024,768))
screen.fill((255,255,255))
#pygame.display.flip()
flight = pygame.image.load('flight.png')
screen.blit(flight, (200,50) )
pygame.display.flip()
time.sleep(1)
# rotate image
import math
rotated = pygame.transform.rotate(flight, 45 * math.pi/180)
screen.blit(flight,(200,150))
pygame.display.update()
time.sleep(2)
# animating the car
for i in range(1000):
    screen.fill((255,255,255))
    screen.blit(flight, (1024-i,0))
    pygame.display.update()
    time.sleep(0.02)
