# class decorator
# run at the end of a class statement to rebind a class to a callable
'''
>>> def decorator(cls): ... return cls
>>> @decorator
    class C:...
>>> class C: ...
    C = decorator(C)
'''
def count_instances(cls):
    cls.numofInstances = 0
    def count(self):
        cls.numofInstances += 1
        print '{num} {clsname}s being created...'.format(num =cls.numofInstances,clsname = cls.__name__)
    cls.count = count
    return cls

def count_instances2(cls):
    cls.numInstances = 0
#   @staticmethod
    def new(cls,*args,**kwargs):
       instance = object.__new__(cls,*args,**kwargs)
       cls.numInstances += 1
       print '{num} {clsname}s being created...'.format(num =cls.numInstances,clsname = cls.__name__)
       return instance
    # __new__ is staticmethod in a class body
    # bind new function to cls
    cls.__new__ = staticmethod(new)
    return cls

@count_instances
class Spam(object):
    def __init__(self,*args,**kwargs):
        self.count()

@count_instances2
class Tuner(object):
    def __init__(self,*args,**kwargs):
        pass

if __name__ == '__main__':
#   Spam();Spam();Spam()
    Tuner();Tuner();Tuner()#.show()
