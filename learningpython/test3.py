#staticmethod
def new(cls,*args,**kwargs):
    print 'cls:',cls
    instance = object.__new__(cls,*args,**kwargs)
    print instance
    return instance

class Tuner(object):
#   numInstances  = 0
#   def __new__(cls,*args,**kwargs):
#      print cls,args,kwargs
#      instance = object.__new__(cls,*args,**kwargs)
#      cls.numInstances += 1
#      print '{num} {clsname}s being created...'.format(num =cls.numInstances,clsname = cls.__name__)
#      return instance
    def __init__(self,*args,**kwargs):
        pass
    def show(self):
        print vars(self)
        print vars(type(self))

if __name__ == '__main__':

#   Spam();Spam();Spam()
    Tuner.__new__ = new
    a=Tuner();Tuner();Tuner().show()
