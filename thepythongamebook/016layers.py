# 016 layers.py
# pygame sprites with different layers and parallax scrolling
# change the sprite layer by clicking with left or right mouse button
# the birdsprites will apear before or behind the blocks
# POINT ON a sprite and press 'p' to print out more information about that  sprite
from constants016 import *

class Text(pygame.sprite.Sprite):
    def __init__(self,msg):
        self.groups = textgroup, allgroup
        self._layer = 99
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.newMsg(msg)
    def update(self,time):
        pass
    def newMsg(self, msg ='i have nothing to say'):
        self.image = write(msg)
        self.rect = self.image.get_rect()
        self.rect.center = screen.get_width/2, 10

class Mountain(pygame.sprite.Sprite):
    # generate a mountain sprite for the background to demonstrate parallax scrolling
    # like in the classic 'moonbuggy' game. Mountains slide from right to left
    def __init__(self,atype):
        self.groups = mountaingroup, allgroups
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.type = atype
        if self.type == 1:
            self._layer = -1
            self.dx = -100
            self.color = blue
        elif self.type == 2:
            self._layer = -2
            self.color = (200,0,255) # pink
            self.dx = -75
        else:
            self._layer = -3
            self.dx = -35
            self.color = red
        self.dy = 0
        width = 1.5 * 100 * self.type # 1.5%
        height = screen.get_height/2 + 50*(self.type-1)
        self.image = pygame.Surface( (width,height))
        self.image.set_colorkey(black)
        pygame.draw.polygon(self.image, self.color,
                ( (0,height), (0,height-10*self.type),(width/2, int( random.random() * height/2 ) ),
                  (width,height),(9,height) ), 0)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.x = screen.get_width() + self.rect.width/2
        self.y = screen.get_height() - self.rect.height/2
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
        self.parent = False
    @property
    def pos(self):
        return self.x, self.y
    def update(self,time):
        self.x += self.dx * time
        self.y += self.dy * time
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
        # kill mountains too far to the left
        if self.rect.centerx + self.rect.width/2 + 10 < 0:
            self.kill()
        # create new mountains if necessary
        if not self.parent:
            if self.rect.centerx < screen.get_width():
                self.parent = True
                Mountain(self.type) # new Mountain coming from the right side

class Block(pygame.sprite.Sprite):
    # a block with a number indicating it's layer
    # Blocks move horizontal and bounce on screen edges
    def __init__(self, blockNum=1):
        self.blockNum = blockNum
        self.color = random.randint(10,255), random.randint(10,255), random.randint(10,255)
        self._layer = self.blockNum
        self.groups = blockgroup, allgroup
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.screenrect = screen.get_rect()
        self.image = pygame.Surface( (100,100))
        self.image.fill(self.color)
        self.image.blit( write(str(self.blockNum)), (40,40) )
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = 50 + 100*self.blockNum
        self.rect.centery = screen.get_height()/2
        self.x = self.rect.centerx
        self.y = self.rect.centery
        self.dx, self.dy = 0,random.randint(50,100) * random.choice([-1,1])
    def newSpeed(self):
        self.dy *= -1 # toggle y direction
    def update(self,time):
        if not self.screenrect.contains(self.rect):
            # compare self.rect and screen.rect
            if self.y < self.screenrect.top:
                self.y = self.screenrect.top
            elif self.y > self.screenrect.bottom:
                self.y = self.screenrect.bottom
                self.newSpeed() # opposite y direction
        self.x += self.dx * time
        self.y += self.dy * time
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

class BirdCatcher(pygame.sprite.Sprite):
    # circle around the mouse pointer. 
    # LEFT button create new sprite, RIGHT button kill sprite
    def __init__(self):
        self._layer = 9
        self.groups = stuffgroup, allgroup
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.image = pygame.Surface( (100,100) )
        self.image.set_colorkey(black)
        self.radius = 50
        pygame.draw.circle(self.image,red,(self.radius,self.radius), self.radius, 2)
    def update(self,seconds):
        self.rect.center = pygame.mouse.get_pos()

class Lifebar(pygame.sprite.Sprite):
    # show a bar with the hitpoints of a Bird sprite with a given bossnumber
    # Lifebar class can identify the boss(Bird sprite) with this codeline: Bird.birds[bossnumber]
    def __init__(self,bossNum):
        self.groups = lifebargroup, allgroup
        self.bossNum = bossNum
        self._layer = Bird.birds[self.bossNum]._layer
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface(Bird.birds[self.bossNum].rect.width,7) )



