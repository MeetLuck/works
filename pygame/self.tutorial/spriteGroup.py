import pygame
# first, create your group
class Jewel1(pygame.sprite.Sprite): # inherit from Sprite class
    def __init__(self,*args):
        # call super constructor, and pass in the group you've created and
        # it is automatically added to the group everty time
        # you create an instance of this class
        '''pygame.sprite.Sprite.__init__(self,*groups) '''
        pygame.sprite.Sprite.__init__(self,gems)

print '-------------- first step ---------------------------'
gems = pygame.sprite.Group()
print 'gems: ',gems  # <Group(0 sprites)>
ruby = Jewel1()
print 'ruby: ',ruby  # <Jewel sprite(in 1 groups)>
print gems.sprites() # [ <Jewel sprite(in 1 groups)> ]
diamond = Jewel1()
print 'diamond: ',diamond  # <Jewel sprite(in 1 groups)>
print gems.sprites()       # [ <Jewel sprite(in 1 groups)>, [ <Jewel sprite(in 1 groups)> ] ]


print '-------------- second step ---------------------------'
gemsgroup = pygame.sprite.Group()
allgroup  = pygame.sprite.Group()
class Jewel2(pygame.sprite.Sprite): # inherit from Sprite class
    groups = gemsgroup,allgroup 
    def __init__(self,*args):
        '''pygame.sprite.Sprite.__init__(self,*groups) '''
        pygame.sprite.Sprite.__init__(self,self.groups)

print '\n => ruby object created'
ruby = Jewel2()
print 'ruby: ',ruby  # <Jewel sprite(in 1 groups)>
print 'gemsgroup: ',gemsgroup  # <Group(0 sprites)>
print 'allgroup: ',allgroup  # <Group(0 sprites)>
print 'gemsgroup.sprite() ',gemsgroup.sprites()
print 'allgroup.sprite() ',allgroup.sprites() 
print ruby.groups
print ruby.groups[0].sprites()
print ruby.groups[1].sprites()

print '\n => diamond object created'
diamond = Jewel2()
print 'diamond: ',diamond  # <Jewel sprite(in 1 groups)>
print 'gemsgroup: ',gemsgroup  # <Group(0 sprites)>
print 'allgroup: ',allgroup  # <Group(0 sprites)>
print 'gemsgroup.sprite() ',gemsgroup.sprites()
print 'allgroup.sprite() ',allgroup.sprites() 
print diamond.groups[0].sprites()
print diamond.groups[1].sprites()
