import pygame, sys
from pygame.locals import *

pygame.init()
surface = pygame.display.set_mode((400,300))
pygame.display.set_caption('Hello World')

white = pygame.Color('white')
green = pygame.Color('green')
blue = pygame.Color('blue')

fontobj = pygame.font.Font('freesansbold.ttf',32)
textobj = fontobj.render('Hello World!', True, green, blue)
textrect = textobj.get_rect()
textrect.center = (200,150)

while True:
    surface.fill(white)
    surface.blit(textobj,textrect)
    for e in pygame.event.get():
        if e.type==KEYDOWN and e.key==K_ESCAPE:
            pygame.quit(); sys.exit()
    pygame.display.update()

" Font object "
# >>> pygame.font.get_fonts()
# >>> pygame.font.match_font('kartika')
'C:\\WINDOWS\\Fonts\\kartika.ttf'
# >>> font = pygame.font.Font('C:\\WINDOWS\\Fonts\\kartika.ttf',24)
# >>> font
' <pygame.font.Font object at 0x00BD69F0> '
" text object"
# >>> text = font.render('kartica',True,pygame.Color('green'),pygame.Color('white'))
# >>> text
' <Surface(44x25x8 SW)> '
# >>> textrect = text.get_rect()
# >>> textrect
' <rect(0, 0, 44, 25)> '
# >>> textrect.center = (200,200)
" surface.blit(source,destination,area=None,special_flags=0)"
# >>> surf.blit(text, textrect) 
# >>> pygame.display.update()
