class Property(object):
    "Emulate PyProperty_Type() in Objects/descrobject.c"
    def __init__(self, fget = None, fset = None):
        self.fget = fget
        self.fset = fset
    def __get__(self,obj,objtype=None):
#       print self,obj
        return self.fget(obj)
    def __set__(self, obj, value):
        self.fset(obj, value)
#   def getter(self, fget):
#       return type(self)(fget, self.fset)
#   def setter(self, fset):
#       return type(self)(self.fget, fset)

class Point(object):
    def getx(self):
#       print '...calling getx'
        return self.__x
    def setx(self, value):
#       print '...calling setx'
        self.__x = value
    x = Property(getx, setx)

if __name__ == '__main__':
    p = Point()
    p.x = 10
    p.x

