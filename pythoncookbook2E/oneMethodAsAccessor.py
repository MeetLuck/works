# 20.5 Using One Method as Accessor for Multiple Attributes

class CommonProperty(object):
    def __init__(self,realname, fget=getattr, fset=setattr, fdel=delattr, doc=None):
        self.realname = realname
        self.fget,self.fset,self.fdel = fget,fset,fdel
        self.__doc__ = doc or ''
    def __get__(self,obj,objtype=None):
        print '__get__',obj,objtype
        if obj is None: return self
        return self.fget(obj,self.realname)
    def __set__(self,obj,value):
        print obj,self.realname,value
        self.fset(obj,self.realname,value)
    def __delete__(self, obj):
        self.fdel(obj,self.realname,value)


class Rectangle(object):

    def __init__(self,a,b):
        self._x = a
        self._y = b 
#       self.y  = b # trigger y.__get__
    def _setSide(self,attr,value):
        setattr(self,attr,value) # self.attr = value
        self.area = self._x * self._y
        print 'self,attr,value : ', self, attr, value
#       print 'locals:',vars(self)

    x = CommonProperty('_x', fset= _setSide, fdel=None)
    y = CommonProperty('_y', fset= _setSide, fdel=None)

    @staticmethod
    def test():
        r = Rectangle(2,3)
        type(r).__dict__['x']
        type(r).x
        r.x
        print vars(r)
        r.x = 4
        r.y = 5
        print vars(r)

if __name__ == '__main__':
    Rectangle.test()
