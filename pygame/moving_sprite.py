"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/
 
Explanation video: http://youtu.be/qbEEcQXw8aw
"""
 
import pygame
import random
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Block(pygame.sprite.Sprite):
    '''
    this class represents the ball
    it derives from the 'Sprite' class in pygame
    '''
    def __init__(self,color,width,height):
        # call the parent class Sprite constructor
        super(Block,self).__init__()
        # create an image of the block, and fill it with a color
        # this could also be an image loaded from the disk
        self.image = pygame.Surface((width,height))
        self.image.fill(color)
        # fetch the rectange object that has the dimesions of the image
        # update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
    def reset_pos(self):
        '''
        reset position to the top of the screen, at a random x location
        called by update() or the main program loop if there is a collision
        '''
        self.rect.y = random.randrange(-300,-20)
        self.rect.x = random.randrange(0,screen_width)
    def update(self):
        # called each frame
        # move block down one pixel
        self.rect.y += 1
        # if block is too far down, reset to top of screen
        if self.rect.y > 410: self.reset_pos()

class Player(Block):
    '''
    the player class derives from Block, but overrides the 'update' functionality with
    new a movement function that will move the block with the mouse 
    '''
    def update(self):
        # get the current mouse position.
        # this returns the position as a list of two numbers
        pos = pygame.mouse.get_pos()
        # fetch the x,y from the list
        # set the player object to the mouse location
        self.rect.x,self.rect.y = pos

# initialize pygame
pygame.init()
# set the height and width of the screen
screen_width,screen_height = 700,400
screen = pygame.display.set_mode( (screen_width,screen_height) )
# this is a list of 'sprites'. each block in the program is added to this list.
# the list is managed by a class called 'Group'
block_list = pygame.sprite.Group()
# this is a list of every sprite. All blocks and the player block as well
all_sprites_list = pygame.sprite.Group()

for i in range(50):
    # this represent a block
    block = Block(BLACK, 20, 15)
    # set a random location for the block
    block.rect.x, block.rect.y = random.randrange(screen_width), random.randrange(screen_height)
    # add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)

# create a red player block
player = Player(RED,20,15)
all_sprites_list.add(player)
# loop until the user clicks the close button
done = False
# used to manage how fast the screen updates
clock = pygame.time.Clock()
score = 0
# --------- main game loop -----------------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    # clear the screen
    screen.fill(WHITE)
    # calls update() on every sprite in the list
    all_sprites_list.update()
    # see if the player block has collided with anything
    blocks_hit_list = pygame.sprite.spritecollide(player,block_list,False)
    # check the list of collisions
    for block in blocks_hit_list:
        score += 1
        print score
    # reset block to the top of the screen to fall again
    block.reset_pos()
    # draw all the sprites
    all_sprites_list.draw(screen)
    # limit to 20 frames per second
    clock.tick(20)
    # go ahead and update the screen with what we've drawn
    pygame.display.flip()
pygame.quit()
