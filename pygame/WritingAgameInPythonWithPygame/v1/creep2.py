from constants import *

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
        elif self.state == Creep.EXPLODING:
            if self.explode_animation.active:
                self.explode_animation.update(time_passed)
            else:
                self.die()
        elif self.state == Creep.DEAD:
            pass

    def draw(self):
        if self.state == Creep.ALIVE:
            self.draw_rect = self.image.get_rect()
            self.draw_rect.center = self.pos
            self.screen.blit(self.image,self.draw_rect)
            health_bar_x = self.pos.x - 7
            health_bar_y = self.pos.y - self.image.get_height()/2 - 6
            # draw life bar
            self.screen.fill(red, [health_bar_x,health_bar_y,15,4]) 
            self.screen.fill(green,[health_bar_x, health_bar_y,self.health,4])
        elif self.state == Creep.EXPLODING:
            self.explode_animation.draw()

    def mouseClickEvent(self,pos):
        if self.pointIsInside( vec2d(pos) ):
            self.decreaseHealth(3)

    def die(self):
        self.state = Creep.DEAD
        self.kill()

    def isPassedCenterCoord(self,current,previous,screenpos_of_coord):
        xo,yo = screenpos_of_coord
        # x,y : screen position of coord(destination)
        # return left_to_right or right_to_left or top_to_bottom or bottom_to_top
        # ----xp---o---xc------ xo-xc<0, xo-xp>0  ==> (xo-xc)*(xo-xp)<0
        return (xo-current.x)*(xo-previous.x) < 0 or (yo-current.y)*(yo-previous.y)<0


    def computeDirection(self,time_passed):
        ' check whether creep is passed center of coord '
        coord = self.game.screenToCoord(self.pos)
        if self.game.isGoalCoord(coord):
            self.die()
        else:
            screenpos_of_coord = self.game.coordToScreenPos(coord)
            if self.isPassedCenterCoord(self.pos,self.prev_pos,screenpos_of_coord):
               next_coord = self.game.gridpath.getNext(coord)
               self.direction = vec2d( next_coord[1] - coord[1], next_coord[0] - coord[0] ).normalized()

    def pointIsInside(self,point):
        w,h = self.image.get_size()
        img_point = point - vec2d( int(self.pos.x-w/2), int(self.pos.y-h/2) )
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
        if coord not in self.path_cache:
            self.computePath(coord)
        if coord in self.path_cache:
            return self.path_cache[coord]
        else:
            raise Exception('not found next coord')

    def set_blocked(self,coord,blocked=True):
        self.map.set_blocked(coord,blocked)
        self.path_cache = {}

    def computePath(self,coord):
        pf = PathFinder(self.map.successors, self.map.move_cost,
                self.map.move_cost)
        # find path
        path_list = list(pf.compute_path(coord, self.goal) )
        # add path to cache
        # self.path_cache[coord] = next coord
        for i, path_coord in enumerate(path_list):
            next_i = i if i==len(path_list)-1 else i+1
            self.path_cache[path_coord] = path_list[next_i]

class Game(object):

    spawned_creep_count = 0

    def getFieldBox(self):
        self.field_border_width = 4 
        self.field_outer_width  = FIELD_SIZE[0] + 2 * self.field_border_width
        self.field_outer_height = FIELD_SIZE[1] + 2 * self.field_border_width
        self.field_rect_outer = pygame.Rect(20,60, self.field_outer_width, self.field_outer_height)
        self.field_bgcolor = pygame.Color(109,41,1,100)
        self.field_border_color = black
        return Box(self.screen, rect=self.field_rect_outer, bgcolor= self.field_border_width,
                border_color = self.field_border_color)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( [SCREEN_WIDTH,SCREEN_HEIGHT],0,32 )
        self.field_box = self.getFieldBox()
        #self.tboard = self.getTboard()
        self.clock = pygame.time.Clock()
        self.creep_images = list()
        self.paused = False
        self.creep_images = [
                ( pygame.image.load(f1).convert_alpha(), pygame.image.load(f2).convert_alpha() )
                  for f1,f2 in CREEP_FILENAMES ]
        explosion_img = pygame.image.load('../images/explosion1.png').convert_alpha()
        self.explosion_images = [ explosion_img, pygame.transform.rotate(explosion_img,90) ]
        self.field_rect = self.getFieldRect()
        self.creeps = pygame.sprite.Group()
        self.spawnNewCreep()
        self.creep_spawn_timer = Timer(500, self.spawnNewCreep)
        self.createWalls()
        # create the grid path representation of the grid
        self.grid_nrows = FIELD_SIZE[1]/GRID_SIZE
        self.grid_ncols = FIELD_SIZE[0]/GRID_SIZE
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

    def screenToCoord(self,pos):
        # covnert screen position pos to (row,col) coordinate
        x,y = pos[0] - self.field_rect.left, pos[1] - self.field_rect.top
        row,col = int(y)/GRID_SIZE, int(x)/GRID_SIZE
        return (row,col)

    def coordToScreenPos(self,coord):
        row,col = coord
        return self.field_rect.left + col * GRID_SIZE + GRID_SIZE/2,\
               self.field_rect.top  + row * GRID_SIZE + GRID_SIZE/2

    def isGoalCoord(self,coord):
        return coord == self.goal_coord

    def spawnNewCreep(self):
        if self.spawned_creep_count >= MAX_N_CREEPS:
            return
        self.creeps.add(
                Creep( screen = self.screen,
                       game = self,
                       creep_images = choice(self.creep_images),
                       explosion_images = self.explosion_images,
                       field = self.field_rect,
                       init_position = (self.field_rect.left+GRID_SIZE/2,
                                       self.field_rect.top +GRID_SIZE/2),
                       init_direction = (1,1),
                       speed = 0.05 ) )
        self.spawned_creep_count += 1

    def getFieldRect(self):
        return self.field_box.get_internal_rect()

    def drawBackground(self):
        bgcolor = darkgray
        self.screen.fill(bgcolor)

    def drawPostals(self):
        self.entrance_rect = pygame.Rect(self.field_rect.left, self.field_rect.top,
                                         2*GRID_SIZE,2*GRID_SIZE)
        self.exit_rect = pygame.Rect(self.field_rect.right - 2*GRID_SIZE,
                                     self.field_rect.bottom - 2*GRID_SIZE,
                                     2*GRID_SIZE, 2*GRID_SIZE)
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
                    (self.field_rect.left, self.field_rect.top+y*GRID_SIZE-1),
                    (self.field_rect.right, self.field_rect.top + y*GRID_SIZE-1) )
        for x in range(self.grid_ncols+1):
            pygame.draw.line(self.screen,pygame.Color(50,50,50),
                    (self.field_rect.left + x*GRID_SIZE-1,self.field_rect.top),
                    (self.field_rect.left + x*GRID_SIZE-1,self.field_rect.bottom-1) )
    def drawWalls(self):
        wallcolor = pygame.Color(140,140,140)
        for wall in self.walls:
            row, col = wall
            pos_x = self.field_rect.left + col*GRID_SIZE + GRID_SIZE/2
            pos_y = self.field_rect.top +  row*GRID_SIZE + GRID_SIZE/2
            radius = 3
            pygame.draw.polygon(self.screen, wallcolor,
                    [ (pos_x - radius, pos_y),(pos_x,pos_y + radius),
                      (pos_x + radius, pos_y), (pos_x,pos_y-radius) ] )
            if (row+1,col) in self.walls:
                pygame.draw.line(self.screen, wallcolor, (pos_x,pos_y),(pos_x,pos_y+GRID_SIZE),3 )
            if (row, col+1) in self.walls:
                pygame.draw.line(self.screen, wallcolor, (pos_x,pos_y),(pos_x+GRID_SIZE,pos_y),3)

    def draw(self):
        self.drawBackground()
        self.field_box.draw()
        if self.options['draw_grid']: self.drawGrid()
        self.drawWalls()
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
            elif event.key == pygame.K_ESCAPE:
                self.quit()
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
