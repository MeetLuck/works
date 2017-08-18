# 9.9 Defining Decorators As Classes
import types
import functools

class Profiled(object):
    def __init__(self,func):
#       functools.wraps(func)(self)
        self.func = func
        self.ncalls = 0
    def __call__(self,*args,**kwargs):
        self.ncalls += 1
        return self.func(*args,**kwargs)
#       return self_wrapped__(*args,**kwargs)
    def __get__(self,instance,cls):
        # bind attribute(method) to instance
#       print self,instance
        if instance is None: return self
        return types.MethodType(self,instance,cls)
#       return functools.partial(self.__call__,instance)


def test1():
    class Spam(object):
#       @Profiled
        def bar(self,x):
            pass
        # decriptor
        bar = Profiled(bar)
#           print self,x
    s = Spam()
#   s.bar(9)
#   print s.bar
    print 's.__dict__:',vars(s)
    print 's.bar.__dict__:',vars(s.bar)
#   print s.bar.ncalls

    @Profiled
    def add(x,y):
        return x + y
#   print add(2,3)
#   print add.ncalls

def profiled(func):
    func.ncall = 0
    def wrapper(*args,**kwargs):
        func.ncall += 1
        return func(*args,**kwargs)
    wrapper.ncall = lambda: func.ncall
    return wrapper

def test2():
    @profiled
    def add(x,y):
        return x+y
    print add(2,3), add.ncall()
    print add(4,5), add.ncall()



if __name__ == '__main__':
    test2()
