# The Base Class for a Game Entity
class GameEntity(object):
    def __init__(self,world,name,image):
        self.world = world
        self.name = name
        self.image = image
        self.location = Vector2(0,0)
        self.destination = Vector2(0,0)
        self.speed = 0
        self.brain = StateMachine()
        self.id = 0
    def render(self,surface):
        x,y = self.location
        w,h = self.image.get_size()
        surface.blit(self.image, x-w/2,y-h/2)
    def process(self,timepassed):
        self.brain.think()
        if self.speed >0 and self.location != self.destination:
            vec_to_destination = self.destination - self.location
            dist_to_destination = vec_to_destination.get_length()
            heading = vec_to_destination.get_normalized()
            travel_distance = min(dist_to_destination, timepassed * self.speed)
            self.location += tranvel_distance * heading


