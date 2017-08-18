# 20.2 Coding Properties as Nested Functions

import math

class Rectangle(object):
    def __init__(self,x,y):
        self.x, self.y = x, y
    def area():
        doc = 'Area of the rectangle'
        def fget(self):
            return self.x * self.y
        def fset(self,value):
            print value, self.area
            ratio = math.sqrt( (1.0*value)/self.area )
            self.x *= ratio
            self.y *= ratio
        return locals()
    area = property( **area() )

if __name__ == '__main__':
    r = Rectangle(2,3)
    print r.area
    r.area = 12
    print vars(r)
