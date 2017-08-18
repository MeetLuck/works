def log_getattribute(cls):
    # get the original implementation
    orig_getattribute = cls.__getattribute__
    # make a new definition
    def new_getattribute(self,name):
        print 'getting:',name
        return orig_getattribute(self,name)
    # attach to the class and return
    cls.__getattribute__ = new_getattribute
    return cls

@log_getattribute
class A(object):
    def __init__(self,x):
        self.x = x
    def spam(self):
        pass

def test():
    print vars(A)
    a = A(42)
    print a.x
    print a.spam()

if __name__ == '__main__':
    test()
