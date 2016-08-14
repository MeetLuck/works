class Shape:
    def __init__(self,x,y):
        self.x, self.y = x,y
class Util:
    def distance_from_origin(self):
        from math import sqrt
        return sqrt(self.x**2 + self.y**2)
class Circle(Shape,Util):
    def __init__(self,x,y,r):
        Shape.__init__(self,x,y)
#       super(self.__class__,self).__init__(x,y)
        self.radius = r


if __name__ == '__main__':
    c1 = Circle(1,1,2)
    print c1.distance_from_origin()
