# class decorator
# run at the end of a class statement to rebind a class to a callable

def decorator(cls):
    class Wrapper(object):
        def __init__(self,*args):
            print 'wrapper.__init__'
            print cls,args
            # call C(*args) -> C.__init__(*args)
            self.wrapped = cls(*args)
        def __getattr__(self,name):
            return getattr(self.wrapped,name)
    return Wrapper

@decorator
class C(object): # C = Wrapper
    def __init__(self,x,y):
        print 'C.__init__'
        self.attr = 'spam'

if __name__ == '__main__':
    x = C(6,7) # calling Wrapper.__init__
    y = C(1,2)
    print repr(C)
    print vars(x)
    print vars(y)
