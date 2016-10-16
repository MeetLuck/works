# Listing 7-5 The Ant Entity Class
class Ant(GameEntity):
    def __init__(self,world,image):
        # call the base constructor
        GameEntity.__init__(self,world,'ant',image)
        # create instances of each of the states
        exploringstate = AntStateExploring(self)
        seekingstate = AntStateSeeking(self)
        deliveringstate = AntStateDelivering(self)
        huntingstate = AntStateHunting(self)
        # add the states to the state machine(self.brain)
        self.brain.addState(exploringstate)
        self.brain.addState(seekingstate)
        self.brain.addState(deliveringstate)
        self.brain.addState(huntingstate)
        
        self.carryimage = None
    def carry(self,image):
        self.carryimage = image
    def drop(self,surface):
        # blit the 'carry' image to the background and reset it
        if self.carryimage:
            x,y = self.location
            w,h = self.carryimage.get_size()
            surface.blit(self.carryimage, (x-w/2, y-h/2))
            self.carryimage = None
    def render(self,surface):
        # call the render function of the base class
        GemeEntity.render(self,surface)
        # extra code to render the carry image
        if self.carryimage:
            x,y = self.location
            w,h = self.carryimage.get_size()
            surface.blit(self.carryimage,(x-w/2,y-h/2))
