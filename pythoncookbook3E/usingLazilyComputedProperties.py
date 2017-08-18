# 8.10 Using Lazily Computed Properties

class lazyproperty(object):
    def __init__(self,func):
        self.func = func
    def __get__(self,instance,cls):
        if instance is None: return self
        value = self.func(instance)
        print vars(instance)
        setattr(instance, self.func.__name__, value)
        print vars(instance)
        return value

import math
class Circle(object):

    def __init__(self,radius):
        self.radius = radius

    @lazyproperty
    def area(self):
        print 'Computing area'
        return math.pi * self.radius**2

    @lazyproperty
    def perimeter(self):
        print 'Computing perimeter'
        return 2*math.pi*self.radius

if __name__ == '__main__':
    c = Circle(4.0)
    print c.radius
    print c.area
    print c.perimeter
    print vars(Circle)
    print vars(c)
    print c.area
    print c.perimeter
