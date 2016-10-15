"""
012text.py
displaying and moving text
This program demonstrate how to render and blit text into a surface
"""
from constants import *

def newcolor():
    return ( random.randint(10,250), random.randint(10,250),random.randint(10,250) )
def write(msg):
    sysfont = pygame.font.SysFont('None', random.randint(34,128) )
    textsurf = sysfont.render(msg,True,newcolor())
    textsurf = textsurf.convert_alpha()
    return textsurf
def main():
    pygame.init()
    x,y = 60,60
    dx,dy = 5,5
    screen = pygame.display.set_mode( (640,480) )
    bgsurf = pygame.Surface( screen.get_size() )
    bgsurf.fill(white)
    bgsurf = bgsurf.convert()
    screen.blit(bgsurf,(0,0))
    clock = pygame.time.Clock()
    fps = 60
    mainloop = True
    while mainloop:
        miliseconds = clock.tick(fps)
        period = miliseconds/1000.0
        mainloop = checkQuit()
        textsurf = write('hello world')
        x += dx
        y += dy
        if x < 0:
            x = 0
            dx *= -1
            # clear screen
            #screen.blit(bgsurf,(0,0))
        elif x + textsurf.get_width() > screen.get_width():
            x = screen.get_width() - textsurf.get_width()
            dx *= -1
        if y < 0:
            y = 0
            dy *= -1
            # clear screen
            #screen.blit(bgsurf,(0,0))
        elif y + textsurf.get_height() > screen.get_height():
            y = screen.get_height() - textsurf.get_height()
            dy *= -1
        screen.blit(textsurf,(x,y))
        pygame.display.flip()
    else:
        pygame.quit()

if __name__ == '__main__':
    main()
