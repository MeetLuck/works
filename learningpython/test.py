class Meta(type):
#   @classmethod
#   def __prepare__(mcls,name,bases,**kwargs):
#       print mcls,name,bases,kwargs
#       return {}
    def __new__(mcls,name,bases,attrs):
        print mcls
        print attrs
        return type.__new__(mcls,name,bases,attrs)
    def __init__(cls,name,bases,attrs):
        print cls
        return type.__init__(cls,name,bases,attrs)
    def __call__(cls,*args,**kwargs):
        print cls,args,kwargs
        return type.__call__(cls,*args,**kwargs)

class Class(object):
    __metaclass__ = Meta
    def __new__(cls,myarg):
        print 'inside %s' %cls
        print cls,myarg
        return super(Class,cls).__new__(cls)
    def __init__(self,myarg):
        self.myarg = myarg
        return super(Class,self).__init__()

c1 = Class(2)

