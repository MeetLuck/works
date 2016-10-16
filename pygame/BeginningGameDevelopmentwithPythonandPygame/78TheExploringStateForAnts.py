# Listing 7-8. The Exploring State for Ants
class AntStateExploring(State):
    def __int__(self,ant):
        # call the base constructor to initialize the State
        State.__init__(self,'exploring')
        # set the ant that this State will manipulate
        self.ant = ant
    def randomDestination(self):
        # select a point in the screen
        w,h = screensize
        self.ant.destination = Vector2( randinit(0,w), randint(0,h) )
    def doActions(self):
        # change direction, 1 in 20 calls
        if randint(1,20) == 1:
            self.randomDestination()
    def checkConditions(self):
        # if there is a nearby leaf, switch to seeking state
        leaf = self.ant.world.getCloseEntity('leaf',self.ant.location)
        if leaf is not None:
            self.ant.leaf_id = leaf.id
            return 'seeking'
        # if there is a nearby spider, switch to hunting state
        spider = self.ant.world.getCloseEntity('spider',nestposition,nestsize)
        if spider is not None:
            if self.ant.location.getDistanceTo(spider.location) < 100:
                self.ant.spider_id = spider.id
                return 'hunting'
        return None
    def entryActions(self):
        # start with random speed and heading
        self.ant.speed = 120 + randint(-30,30)
        self.randomDestination()
