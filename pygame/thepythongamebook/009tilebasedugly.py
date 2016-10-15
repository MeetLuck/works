''' 009 tile based ugly.py '''

def mazegame():
    import pygame,random
    pygame.init()
    screen = pygame.display.set_mode( (640,480) )
    screenrect = screen.get_rect()
    bgsurf = pygame.Surface( (screen.get_size()) )
    bgsurfrect = bgsurf.get_rect()
    bgsurf.fill(white)
    bgsurf = bgsurf.convert()
    bgsurf0 = bgsurf.copy()
    screen.blit(bgsurf,(0,0))

    ballsurf = pygame.Surface((10,10))
    ballsurf.set_colorkey(black)
    pygame.draw.circle(ballsurf,red,(5,5),5)
    ballsurf = ballsurf.convert_alpha()
    ballrect = ballsurf.get_rect()

