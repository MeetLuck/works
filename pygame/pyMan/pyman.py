import os, sys
import pygame
from pygame.locals import *
if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

def load_image(name, colorkey=None):
    # data\\images
    fullname = os.path.join('data','images')
    fullname = os.path.join(fullname, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    # convert() makes a new copy of a Surface and converts its color format
    # and depth to match the display.
    image = image.convert()
    # colorkey is used to represent a color of the image that is transparent
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class PyManMain:
    ''' The main PyMan class
        This class handles the main initialization and creating of the game
    '''
    def __init__(self, width=640,height=480):
        # initilize pygame
        pygame.init()
        # set the window size
        self.width, self.height = width,height
        # create the screen
        self.screen = pygame.display.set_mode( (self.width,self.height))
    def mainloop(self):
        # this is the main loop of the game
        # load all of our sprites
        self.loadSprites()
        # tell pygame to keep sending up keystrokes when they are held down
        pygame.key.set_repeat(500,30)
        # create the background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    if ( (event.key == K_RIGHT) or (event.key == K_LEFT) or
                         (event.key == K_UP) or (event.key == K_DOWN) ):
                        self.snake.move(event.key)
                # check for collision
                IstCols = pygame.sprite.spritecollide(self.snake, self.pellet_sprites,True)
                # update the amount of pellets eatean
                self.snake.pellets = self.snake.pellets + len(IstCols)
                # do the drawing
                self.screen.blit(self.background,(0,0))
                if pygame.font:
                    font = pygame.font.Font(None,36)
                    text = font.render('Pellets %s' % self.snake.pellets,1,(255,0,0))
                    textpos = text.get_rect(centerx=self.background.get_width()/2)
                    self.screen.blit(text,textpos)
                self.pellet_sprites.draw(self.screen)
                self.snake_sprites.draw(self.screen)
                pygame.display.flip()
    def loadSprites(self):
        # load the sprites that we need
        self.snake = Snake()
        self.snake_sprites = pygame.sprite.RenderPlain((self.snake))
        # figure out how many pellets we can display
        nNumHorizontal = int(self.width/64)
        nNumVertical = int(self.height/64)
        # create the Pellet group
        self.pellet_sprites = pygame.sprite.Group()
        # create all of the pellets and add them to the pellet_sprites group
        for x in range(nNumHorizontal):
            for y in range(nNumVertical):
                self.pellet_sprites.add(Pellet(pygame.Rect(x*64,y*64,64,64)))


class Snake(pygame.sprite.Sprite):
    ''' This is our snake that will move around the screen '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('snake.png',-1)
        self.pellets = 0
        # set the number of Pixels to move around the screen
        self.x_dist = 5
        self.y_dist = 5
    def move(self,key):
        # move yourself in one of the 4 directions according to key
        # key is the pyGame defined for either up,down,left,or right key
        # we will adjust ourselves in that direction
        xMove = 0
        yMove = 0
        if   key==K_RIGHT: xMove = +self.x_dist
        elif key==K_LEFT : xMove = -self.x_dist
        elif key==K_UP   : yMove = -self.x_dist
        elif key==K_DOWN : yMove = +self.x_dist
        self.rect.move_ip(xMove,yMove)

class Pellet(pygame.sprite.Sprite):
    def __init__(self, rect=None):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('pellet.png',-1)
        if rect != None:
            self.rect = rect

if __name__ == '__main__':
    mainwindow = PyManMain()
    mainwindow.mainloop()


