import pygame,os,sys
from random import randint,choice
from math import sin,cos,radians
from gridmap import GridMap
from pathfinder import PathFinder
from simpleanimation import SimpleAnimation
from utils import Timer
from vec2d import vec2d
from widgets import Box, MessageBoard

red = pygame.Color('red')
green = pygame.Color('green')

class Creep(pygame.sprite.Sprite):
    ALIVE, EXPLODING, DEAD = range(3)
    def __init__(self,screen,game,creep_images,explosion_images,field,init_position,init_direction,speed):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.game = game
        self.speed = speed
        self.field = field
        self.baseimage0 = creep_images[0]
        self.baseimage45 = creep_images[1]
        self.image = self.baseimage0
        # list of image objects
        self.explosion_images = explosion_images
        self.pos = vec2d(init_position)
        self.prev_pos = vec2d(self.pos)
        self.direction = vec2d(init_direction).normalized()
        self.state = Creep.ALIVE
        self.health = 15
    def isAlive(self):
        return self.state in (Creep.ALIVE, Creep.EXPLODING)
    def update(self,time_passed):
        if self.state == Creep.ALIVE:
            self.computeDirection(time_passed)
            if int( round(self.direction.angle) ) % 90 == 45:
                self.image = pygame.transform.rotate(self.baseimage45,-(self.direction.angle + 45) )
            elif int( round(self.direction.angle) ) % 90 == 0:
                self.image = pygame.transform.rotate(self.baseimage0, -self.direction.angle)
            else:
                assert False
            displacement = vec2d( self.direction.x * self.speed * time_passed, self.direction.y * self.speed * time_passed)
            self.prev_pos = vec2d(self.pos)
            self.pos += displacement
            self.image_w, self.image_h = self.image.get_size()
        elif self.state == Creep.EXPLODING:
            if self.explode_animation.active:
                self.explode_animation.update(time_passed)
            else:
                self.die()
        elif self.state == Creep.DEAD:
            pass
    def draw(self):
        if self.state == Creep.ALIVE:
            self.draw_rect = self.image.get_rect().move( self.pos.x - self.image_w/2, self.pos.y - self.image_h/2)
            self.screen.blit(self.image,self.draw_rect)
            health_bar_x = self.pos.x - 7
            health_bar_y = self.pos.y - self.image_h/2 - 6
            self.screen.fill(red, [health_bar_x,health_bar_y,15,4]) 
            self.screen.fill(green,[health_bar_x, health_bar_y,self.health,4])
        elif self.state == Creep.EXPLODING:
            self.explode_animation.draw()
        elif self.state == Creep.DEAD:
            pass
    def mouseClickEvent(self,pos):
        if self.pointIsInside( vec2d(pos) ):
            self.decreaseHealth(3)
    def die(self):
        self.state = Creep.DEAD
        self.kill()
    def computeDirection(self,time_passed):
        coord = self.game.xy2coord(self.pos)
        if self.game.isGoalCoord(coord):
            self.die()
        else:
            x_mid,y_mid = self.game.coord2xy_mid(coord)
            if (x_mid-self.pos.x)*(x_mid-self.prev_pos.x) < 0 or  (y_mid-self.pos.y)*(y_mid-self.prev_pos.y) < 0:
               next_coord = self.game.nextOnPath(coord)
               self.direction = vec2d( next_coord[1] - coord[1], next_coord[0] - coord[0] ).normalized()
    def pointIsInside(self,point):
        img_point = point - vec2d( int(self.pos.x-self.image_w/2), int(self.pos.y-self.image_h/2) )
        try:
            pix = self.image.get_at(img_point)
            return pix[3] > 0
        except IndexError:
            return False
    def decreaseHealth(self,n):
        self.health = max(0, self.health - n)
        if self.health == 0:
            self.explode()
    def explode(self):
        self.state = Creep.EXPLODING
        pos = self.pos.x - self.explosion_images[0].get_width()/2, self.pos.y - self.explosion_images[1].get_height()/2
        self.explode_animation = SimpleAnimation( self.screen, pos, self.explosion_images, 100, 300 )
                    
class GridPath(object):
    def __init__(self,nrows,ncols,goal):
        self.map = GridMap(nrows,ncols)
        self.goal = goal
        self.path_cache = {}
    def getNext(self,coord):
        if not (coord in self.path_cache):
            self.computePath(coord)
        if coord in self.path_cache:
            return self.path_cache[coord]
        else:
            return None
    def set_blocked(self,coord,blocked=True):
        self.map.set_blocked(coord,blocked)
        self.path_cache = {}
    def computePath(self,coord):
        pf = PathFinder(self.map.successors, self.map.move_cost,
                self.map.move_cost)
        path_list = list(pf.compute_path(coord, self.goal) )
        for i, path_coord in enumerate(path_list):
            next_i = i if i==len(path_list)-1 else i+1
            self.path_cache[path_coord] = path_list[next_i]

class Game(object):
    BG_TITLE_IMG = 'images/brick_tile.png'
    SCREEN_WIDTH, SCREEN_HEIGHT = 580, 500
    GRID_SIZE = 20
    FIELD_SIZE = 400,400
    CREEP_FILENAMES = [
            ('images/bluecreep_0.png', 'images/bluecreep_45.png'),
            ('images/greencreep_0.png', 'images/greencreep_45.png'),
            ('images/yellowcreep_0.png', 'images/yellowcreep_45.png'),
            ('images/pinkcreep_0.png', 'images/pinkcreep_45.png'),
            ]
    MAX_N_CREEPS = 50

    def getFieldBox(self):
        self.field_border_width = 4
        self.field_outer_width = self.FIELD_SIZE[0] + 2 * self.field_border_width
        self.field_outer_height = self.FIELD_SIZE[1] + 2 * self.field_border_width
        self.field_rect_outer = pygame.Rect(20,60, self.field_outer_width, self.field_outer_height)
        self.field_bgcolor = pygame.Color(109,41,1,100)
        self.field_border_color = pygame.Color(0,0,0)
        return Box(self.screen, rect=self.field_rect_outer, bgcolor= self.field_border_width,
                border_color = self.field_border_color)

    def getTboard(self):
        self.tboard_text = ['The amazing Creeps!']
        self.tboard_rect = pygame.Rect(20,20,self.field_outer_width,30)
        self.tboard_bgcolor = pygame.Color(50,20,0)
        return MessageBoard(self.screen, rect=self.tboard_rect, bgcolor=self.tboard_bgcolor,
                border_width=4, border_color=pygame.Color('black'), text=self.tboard_text,
                font=('tahoma',18), font_color=pygame.Color('yellow') )

    def getMBoard(self):
        self.mboard_text = []
        self.mboard_rect = pygame.Rect(440,60,120,60)
        self.mboard_bgcolor = pygame.Color(50,20,0)
        return MessageBoard(self.screen, rect = self.mboard_rect, bgcolor=self.mboard_bgcolor,
                border_width = 4, border_color = pygame.Color('black'), text=self.mboard_text,
                font = ('verdana',16), font_color = pygame.Color('white') )

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( [self.SCREEN_WIDTH,self.SCREEN_HEIGHT],0,32 )
        self.tile_img = pygame.image.load(self.BG_TITLE_IMG).convert_alpha()
        self.tile_img_rect = self.tile_img.get_rect()
        self.field_box = self.getFieldBox()
        self.tboard = self.getTboard()
        self.mboard = self.getMBoard()
        self.clock = pygame.time.Clock()
        self.creep_images = list()
        self.paused = False
        self.creep_images = [
                ( pygame.image.load(f1).convert_alpha(), pygame.image.load(f2).convert_alpha() )
                  for f1,f2 in self.CREEP_FILENAMES ]
        explosion_img = pygame.image.load('images/explosion1.png').convert_alpha()
        self.explosion_images = [ explosion_img, pygame.transform.rotate(explosion_img,90) ]
        self.field_rect = self.getFieldRect()
        self.creeps = pygame.sprite.Group()
        self.spawnNewCreep()
        self.creep_spawn_timer = Timer(500, self.spawnNewCreep)
        self.createWalls()
        # create the grid path representation of the grid
        self.grid_nrows = self.FIELD_SIZE[1]/self.GRID_SIZE
        self.grid_ncols = self.FIELD_SIZE[0]/self.GRID_SIZE
        self.goal_coord = self.grid_nrows - 1, self.grid_ncols - 1
        self.gridpath = GridPath(self.grid_nrows,self.grid_ncols,self.goal_coord)
        for wall in self.walls:
            self.gridpath.set_blocked(wall)
        self.options = dict( draw_grid=False )

    def createWalls(self):
        walls_list = list()
        for r in range(0,15):
            walls_list.append( (r,6) )
            if r != 7:
                walls_list.append( (r,3) )
                walls_list.append( (r,4) )
            if r > 4:
                walls_list.append( (r,1) )
        for r in range(9,20):
            walls_list.append( (r,10) )
        self.walls = dict().fromkeys(walls_list,True)

    def nextOnPath(self,coord):
        return self.gridpath.getNext(coord)

    def xy2coord(self,pos):
        # covnert mouse position (x,y) to (row,col) coordinate
        x,y = pos[0] - self.field_rect.left, pos[1] - self.field_rect.top
        return int(y)/self.GRID_SIZE, int(x)/self.GRID_SIZE

    def coord2xy_mid(self,coord):
        row,col = coord
        return self.field_rect.left + col * self.GRID_SIZE + self.GRID_SIZE/2,\
               self.field_rect.top  + row * self.GRID_SIZE + self.GRID_SIZE/2

    def isGoalCoord(self,coord):
        return coord == self.goal_coord

    spawned_creep_count = 0

    def spawnNewCreep(self):
        if self.spawned_creep_count >= self.MAX_N_CREEPS:
            return
        self.creeps.add(
                Creep( screen = self.screen,
                       game = self,
                       creep_images = choice(self.creep_images),
                       explosion_images = self.explosion_images,
                       field = self.field_rect,
                       init_position = (self.field_rect.left+self.GRID_SIZE/2,
                                       self.field_rect.top +self.GRID_SIZE/2),
                       init_direction = (1,1),
                       speed = 0.05 ) )
        self.spawned_creep_count += 1

    def getFieldRect(self):
        return self.field_box.get_internal_rect()

    def drawBackground(self):
        img_rect = self.tile_img.get_rect()
        nrows = int(self.screen.get_height()/img_rect.height) + 1
        ncols = int(self.screen.get_width() /img_rect.width) + 1
        for y in range(nrows):
            for x in range(ncols):
                img_rect.topleft = x*img_rect.width, y*img_rect.height
                self.screen.blit(self.tile_img, img_rect)

    def drawPostals(self):
        self.entrance_rect = pygame.Rect(self.field_rect.left, self.field_rect.top,
                                         2*self.GRID_SIZE,2*self.GRID_SIZE)
        self.exit_rect = pygame.Rect(self.field_rect.right - 2*self.GRID_SIZE,
                                     self.field_rect.bottom - 2*self.GRID_SIZE,
                                     2*self.GRID_SIZE, 2*self.GRID_SIZE)
        entrance = pygame.Surface( (self.entrance_rect.w, self.entrance_rect.h) )
        entrance.fill(pygame.Color(80,200,80) )
        entrance.set_alpha(150)
        self.screen.blit(entrance,self.entrance_rect)
        exit = pygame.Surface( (self.exit_rect.w,self.exit_rect.h) )
        exit.fill( pygame.Color(80,200,80) )
        exit.set_alpha(150)
        self.screen.blit(exit,self.exit_rect)

    def drawGrid(self):
        for y in range(self.grid_nrows+1):
            pygame.draw.line(self.screen, pygame.Color(50,50,50),
                    (self.field_rect.left, self.field_rect.top+y*self.GRID_SIZE-1),
                    (self.field_rect.right, self.field_rect.top + y*self.GRID_SIZE-1) )
    def drawWalls(self):
        wallcolor = pygame.Color(140,140,140)
        for wall in self.walls:
            row, col = wall
            pos_x = self.field_rect.left + col*self.GRID_SIZE + self.GRID_SIZE/2
            pos_y = self.field_rect.top +  row*self.GRID_SIZE + self.GRID_SIZE/2
            radius = 3
            pygame.draw.polygon(self.screen, wallcolor,
                    [ (pos_x - radius, pos_y),(pos_x,pos_y + radius),
                      (pos_x + radius, pos_y), (pos_x,pos_y-radius) ] )
            if (row+1,col) in self.walls:
                pygame.draw.line(self.screen, wallcolor, (pos_x,pos_y),(pos_x,pos_y+self.GRID_SIZE),3 )
            if (row, col+1) in self.walls:
                pygame.draw.line(self.screen, wallcolor, (pos_x,pos_y),(pos_x+self.GRID_SIZE,pos_y),3)

    def draw(self):
        self.drawBackground()
        self.field_box.draw()
        if self.options['draw_grid']: self.drawGrid()
        self.drawWalls()
        self.tboard.draw()
        self.mboard.text = self.mboard_text
        self.mboard.draw()
        for creep in self.creeps:
            creep.draw()
        self.drawPostals()

    def onEvent(self,event):
        if event.type == pygame.QUIT:
            self.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.paused = not self.paused
            elif event.key == pygame.K_g:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.options['draw_grid'] = not self.options['draw_grid']
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for creep in self.creeps:
                creep.mouseClickEvent(event.pos)

    def run(self):

        while True:
            time_passed = self.clock.tick(30)
            if time_passed > 100: continue
            for event in pygame.event.get():
                self.onEvent(event)
            if not self.paused:
                msg1 = 'Creeps:%d' %len(self.creeps)
                msg2 = ''
                self.mboard_text = [msg1,msg2]
                self.creep_spawn_timer.update(time_passed)
                # update and all creeps
                for creep in self.creeps:
                    creep.update(time_passed)
                self.draw()
            pygame.display.flip()
        def quit(self):
            sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()
