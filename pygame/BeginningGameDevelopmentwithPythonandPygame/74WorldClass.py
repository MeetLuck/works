# Listing 7-4 World Class
class World(object):
    def __init__(self):
        self.entities = {} # store all the entities
        self.entity_id = 0 # last entity id assigned
        # draw the next(a circle) on the background
        self.bgsurf = pygame.surface.Surface(screensize).convert()
        self.bgsurf.fill(white)
        pygame.draw.circle(self.bgsurf,(200,255,200), nestposition, int(nestsize) )
    def addEntity(self,entity):
        # store the entity then advances the current id 
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1
    def removeEntity(self,entity):
        del sel.entitites[entity.id]
    def get(self,entity_id):
        # find the entity, givent its id(or None if it is not found)
        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None
    def process(self,timepassed):
        # process every entity in the world
        for entity in self.entities.itervalues():
            entity.process(timepassed)
    def render(self,surface):
        # draw the background and all the entities
        surface.blit(self.bgsurf,(0,0))
        for entity in self.entities.values():
            entity.render(surface)
    def getCloseEntity(self,name,location,erange=100):
        # find an entity within range of a location
        location = Vector2(*location)
        for entity in self.entities.values():
            if entity.name == name:
                distance = location.get_distance_to(entity.location)
                if distance < erange:
                    return entity
        return None

