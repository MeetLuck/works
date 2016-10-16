import match

class Vector:
    def __init__(self,x=0,y=0):
        self.x,self.y = x,y
    def __str__(self):
        return '(%s,%s)' %(self.x,self.y)
    @classmethod
    def from_points(cls,P1,P2):
        return Vector(P1.x-P2.x, P1.y-P2.y)
    def get_magnitude(self):
        return match.sqrt( self.x**2 + self.y**2 )
    def normalize(self):
        self.x /= self.get_magnitude()
        self.y /= self.get_magnitude()
    def __add__(self,other):
        return Vector(self.x+other.x, self.y+other.y)
    def __sub(self,other):
        return Vector(self.x-other.x, self.y-other.y)
    def __neg__(self):
        return Vector(-self.x,-self.y)
    def __mul__(self,scalar):
        return Vector(scalar*self.x,scalar*self.y)
    def __truediv__(self,scalar):
        return Vector(scalar/self.x,scalar/self.y)
