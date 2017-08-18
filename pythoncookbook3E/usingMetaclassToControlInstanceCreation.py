# 9.13 Using a MetaClass to Control Instance Creation
class NoInstance(type):
    def __call__(self,*args,**kwargs):
        raise TypeError("Can't instantiate directly")

class Spam(object):
    __metaclass__= NoInstance
    @staticmethod
    def grok(x):
        print('Spam.grok %s' %x)

    @staticmethod
    def test():
        Spam.grok(23)
        s = Spam()

class Singleton(type):
    def __init__(self,*args,**kwargs):
        self.__instance = None
        super(Singleton,self).__init__(*args,**kwargs)
    def __call__(self,*args,**kwargs):
        if self.__instance is None:
            self.__instance = super(Singleton,self).__call__(*args,**kwargs)
            return self.__instance
        else:
            return self.__instance
class Foo(object):
    __metaclass__ = Singleton
    def __init__(self,name):
        print('Creating Foo')
        self.name = name
    @staticmethod
    def test():
        a = Foo('apple')
        b = Foo('pea')
        print a
        print b
        print a is b

# cached instance
import weakref
class Cached(type):
    def __init__(self,*args,**kwargs):
        super(Cached,self).__init__(*args,**kwargs)
        self.__cached = dict()
#       self.__cached = weakref.WeakValueDictionary()
    def __call__(self,*args,**kwargs):
        if args in self.__cached:
            return self.__cached[args]
        else:
            obj = super(Cached,self).__call__(*args)
            self.__cached[args] = obj
            return obj

class Bar(object):
    __metaclass__ = Cached
    def __init__(self,name):
        print('Creating Bar({!r})'.format(name))
        self.name = name
    @staticmethod
    def test():
        a = Bar('Jame')
        b = Bar('Diana')
        c = Bar('Diana')
        print repr(b)
        print repr(c)
        print b is c


if __name__ == '__main__':
#   Spam.test()
#   Foo.test()
    Bar.test()

