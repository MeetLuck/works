# Listing 3-2. Displaying the Message Queue
# font height = font.get_linesize()
import pygame
from pygame.locals import *
from sys import exit

pygame.init()
screensize = screenwidth,screenheight = 800,600
screen = pygame.display.set_mode(screensize,0,32)
font = pygame.font.SysFont('arial bold',18)
fontheight = font.get_linesize()

# constants
white = pygame.Color('white')
black = pygame.Color('black')
darkgreen = pygame.Color('darkgreen')
event_text = list()
maxlines = screenheight/fontheight
print 'maxlines -> ',maxlines

while True:
    event = pygame.event.wait()
    if event.type == QUIT: pygame.quit(); exit()

    print 'oldeventtext =-> ',event_text
    event_text.append( str(event) )
    
#   if len(event_text) < maxlines:
#       start = -len(event_text)
#   else:
#       start = -maxlines

    neweventtext = event_text[-maxlines:]  # fit into screen height by cutting
    print 'new event_text =-> ', neweventtext

    screen.fill(white)
    y = screenheight - fontheight
    for text in reversed(neweventtext):
        screen.blit( font.render(text,True,darkgreen), (0,y) )
        y -= fontheight
    pygame.display.update()




