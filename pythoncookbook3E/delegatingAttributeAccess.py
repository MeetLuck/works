# 8.15 Delegating Attribute Access

class A(object):
    def cook(self,food):
        print '...cook ' + str(food)
    def order(self,food):
        print '...order ' + str(food)

class B(object):
    def __init__(self):
        self._a = A()
    def cook(self,food):
        # delegate to the internal self._a instance
        return self._a.cook(food)
    @staticmethod
    def test():
        B().cook('spam')

class C(object):
    def __init__(self):
        self._a = A()
    def bar(self):
        pass
    # Expose all of the methods defined on class A
    def __getattr__(self,name):
        print name
        return getattr(self._a, name)
    @staticmethod
    def test():
        c = C()
        c.cook('spam')
        c.order('stake')

# A proxy class that wraps around another object, but expose its public attributes

class Proxy(object):
    def __init__(self,obj):
        self._obj = obj
    # delegate attribute lookup to internal obj
    def __getattr__(self,name):
        print 'getattr: ',name
        return getattr(self._obj,name)
    # delegate attribute assignment
    def __setattr__(self,name,value):
        if name.startswith('_'):
            super(Proxy,self).__setattr__(name,value)
        else:
            print 'setattr: ',name, value
            setattr(self._obj,name,value)
    # delegate attribute deletion
    def __delattr__(self,name):
        if name.startswith('_'):
            super(Proxy,self).__deltattr__(name)
        else:
            print 'delattr: ',name
            delattr(self._obj,name)

class Spam(object):
    def __init__(self,x):
        self.x = x
    def bar(self,y):
        print 'Spam.bar: ', self.x, y
    @staticmethod
    def test():
        s = Spam(2)
        p = Proxy(s)
        print p.x
        print vars(s)
        p.bar(3)
        print vars(s)
        p.x = 37
        print vars(s)




if __name__ == '__main__':
#   C.test()
    Spam.test()


