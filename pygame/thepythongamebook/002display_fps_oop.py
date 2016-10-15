'''
002display_fps_pretty.py

Display framerate and playtime

URL    : http://thepythongamebook.com/en:part2:pygame:step002
Author : horst.jens@spielend-programmieren.at
License: GPL, see http://www.gnu.org/licenses/gpl.html
'''

import pygame, os

class PygView(object):
    def __init__(self,width=640,height=480,fps=30):
        # initialize pygame, window, background, font, ...
        pygame.init()
        self.width,self.height = width,height
        self.screen = pygame.display.set_mode( (self.width,self.height), pygame.DOUBLEBUF)
        pygame.display.set_caption('Press ESC to quit')
        #self.background = pygame.Surface( self.screen.get_size() ).convert()
        #self.background.fill(pygame.Color('darkgreen'))
        self.clock = pygame.time.Clock()
        #self.fps = fps
        self.fps = 60 # max = 40 fps shit
        self.playtime = 0.0
        self.font = pygame.font.SysFont('mono',20,bold=True)
    def run(self):
        # the main loop
        running = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT: running = False
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        running = False

            miliseconds = self.clock.tick(self.fps)
            self.playtime += miliseconds
            os.system('cls')
            #self.screen.blit(self.background,(0,0))
            self.screen.fill(pygame.Color('darkgreen'))
            self.drawText("FPS : {:6.2f}{}PLAYTIME : {} SECONDS".format(self.clock.get_fps(),' '*5, self.playtime) )
            pygame.display.flip()
        pygame.quit()
    def drawText(self,text):
        # center text in window
        fw,fh = self.font.size(text) # font width,height
        textSurf = self.font.render( text, True, pygame.Color('white') )
        # makes integer division in python 3
        screenX =  (self.width - fw)//2
        screenY =  (self.height -fh)//2
        self.screen.blit(textSurf, ( (self.width - fw)//2, (self.height-fh)//2 ) )

if __name__ == '__main__':
    PygView(600,300).run()

