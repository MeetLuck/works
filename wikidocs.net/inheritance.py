class Shape:
    def __init__(self,x,y):
        self.x, self.y = x,y
class Circle(Shape):
    def __init__(self,x,y,r):
        Shape.__init__(self,x,y)
#       super(self.__class__,self).__init__(x,y)
        self.radius = r

if __name__ == '__main__':
    c1 = Circle(0,0,1)
    print globals()
    print c1.__dict__
