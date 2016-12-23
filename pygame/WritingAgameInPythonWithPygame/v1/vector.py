import math
class Vector:
    def __init__(self,*args):
        ''' args = args[0],args[1],... '''
        if len(args) == 0: # obj = Vector()
            self.x,self.y = 0,0
        elif len(args) == 1: # obj = Vector(tuple or list)
            assert len(args[0]) == 2, 'tuple or list of 2 elements required'
            self.x,self.y = args[0]
        elif len(args) == 2: # obj = Vector(x,y)
            self.x,self.y = args # args[0],args[1]
        else:
            raise AssertionError,'x,y or tuple(list) required'
        # convert to float
        self.x,self.y = float(self.x),float(self.y)
    def getMagnitude(self):
        return math.sqrt( self.x**2 + self.y**2 )
    def getNormalized(self):
        return self/self.getMagnitude()
    def getDistanceTo(self,other):
        if not isinstance(other,Vector):
            other = Vector(other)
        return (other-self).getMagnitude()

    @property
    def angle(self):
        if self.getMagnitude()==0:
            return 0
        return math.degrees(math.atan2(self.y, self.x))

    def __iter__(self): # tu = tuple(obj)
        return iter( (self.x,self.y) )
    def __add__(self,other):
        return Vector(self.x+other.x, self.y+other.y)
    def __iadd__(self,other):
        return self.__add__(other)
    def __sub__(self,other):
        return Vector(self.x-other.x,self.y-other.y)
    def __neg__(self):
        return Vector(-self.x,-self.y)
    def __mul__(self,scalar):
        return Vector(scalar*self.x,scalar*self.y)
    def __div__(self,scalar):
        return Vector(self.x/scalar, self.y/scalar)
    def __rdiv__(self,scalar):
        return Vector(scalar/self.x, scalar/self.y)
    def __str__(self):
        return 'Vector(%s,%s)' %(self.x,self.y)

if __name__ == '__main__':
    v = Vector()
    print v
    print v.getMagnitude()
    v1 = Vector(1,2)
    print v1
    print v1*2
    print v1/2.0
    print 2.0/v1
    tu = 0.707,0.707
    v2 = Vector(tu)
    print v2
    a = tuple()
    a = v2
    print a
    print v2.getMagnitude()
    print v1 + v2
    v2 += v1*10
    print v2
    astu = tuple(v2)
    print astu,type(astu)


