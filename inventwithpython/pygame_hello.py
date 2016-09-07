import pygame, sys
from pygame.locals import *
# set up pygame
pygame.init()
# set up the window
windowSurface = pygame.display.set_mode((500,400),0,32)
pygame.display.set_caption('Hello World')
# set up the colors
black = 0,0,0
white = 255,255,255
red   = 255,0,0
green = 0,255,0
blue  = 0,0,255
# set up fonts
f1 = pygame.font.get_default_font()
#basicfont = pygame.font.Font(f1,30)
basicfont = pygame.font.SysFont(None,48)
# set up the text
text = basicfont.render('Hello world!', True, white, blue)
textrect = text.get_rect()
textrect.centerx = windowSurface.get_rect().centerx
textrect.centery = windowSurface.get_rect().centery
# draw the white background onto the surface
windowSurface.fill(white)
# draw a green polygon onto the surface
pygame.draw.polygon(windowSurface, green,((146,0),(291,106),(236,277),(56,277),(0,106)))
# draw some blue lines onto the surface
pygame.draw.line(windowSurface,blue,(60,60),(120,60),4)
pygame.draw.line(windowSurface,blue,(120,60),(60,120))
pygame.draw.line(windowSurface,blue,(60,120),(120,120),4)
# draw a blue circle onto the surface
pygame.draw.circle(windowSurface,blue,(300,50),20,0)
# draw a red ellipse onto the surface
pygame.draw.ellipse(windowSurface, red, (300,250,40,80),1)
# draw the text's background rectange onto the surface
pygame.draw.rect(windowSurface,red,(textrect.left-20, textrect.top-20, textrect.width+40, textrect.height+40))
# get a pixel array of the surface
pixArray = pygame.PixelArray(windowSurface)
pixArray[480][380] = black
del pixArray
# draw the text onto the surface
windowSurface.blit(text,textrect)
# draw the window onto the screen
pygame.display.update()
# run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

