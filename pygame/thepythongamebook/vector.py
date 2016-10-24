import math

class Vector:
    def __init__(self,*args): #x=0,y=0):
        ''' args = ( arg[0],args[1],.... ) '''
        if len(args) == 0:  # Vector()
            self.x,self.y = 0,0
        elif len(args) == 1: # Vector(tu or list)
            assert len(args[0])==2,'tuple or list of 2 elements required'
            self.x,self.y = args[0]
        elif len(args) == 2: # Vector(x,y)
            self.x,self.y = args[0],args[1]
        else:
            raise AssertionError, 'x,y or tuple required'
        # convert to float type
        self.x,self.y = float(self.x),float(self.y)

    def __str__(self):
        return 'Vector(%s,%s)' %(self.x,self.y)
    def __repr__(self):
        return __str__(self)
    @classmethod
    def from_points(cls,P1,P2):
        return Vector(P1.x-P2.x, P1.y-P2.y)
    def get_magnitude(self):
        return math.sqrt( self.x**2 + self.y**2 )
    def normalize(self):
        self.x /= self.get_magnitude()
        self.y /= self.get_magnitude()
    def __iter__(self): # tu = tuple(Vector(x,y))
        return iter( (self.x,self.y) )
    def __add__(self,other):
        return Vector(self.x+other.x, self.y+other.y)
    def __iadd__(self,other):
        return Vector(self.x+other.x, self.y+other.y)
    def __sub__(self,other):
        return Vector(self.x-other.x, self.y-other.y)
    def __neg__(self):
        return Vector(-self.x,-self.y)
    def __mul__(self,scalar):
        return Vector(scalar*self.x,scalar*self.y)
    def __truediv__(self,scalar):
        return Vector(scalar/self.x,scalar/self.y)

if __name__ == '__main__':
    v = Vector()
    print v
    print v.get_magnitude()
    v1 = Vector(1,2)
    print v1
    print v1*2
    tu = 0.707,0.707
    v2 = Vector(tu)
    print v2
    print v2.get_magnitude()
    print v1 + v2
    v2 += v1*10
    print v2
    astu = tuple(v2)
    print astu,type(astu)
