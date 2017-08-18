class SuperMeta(type):
    def __call__(metaname, clsname, baseclasses, attrs):
        print 'SuperMeta Called %s' %metaname
        clsob = type.__new__(metaname, clsname, baseclasses, attrs)
        type.__init__(clsob, clsname, baseclasses, attrs)
        return clsob
 
 
class MyMeta(type):
    __metaclass__ = SuperMeta
    def __call__(cls, *args, **kwargs):
        print 'MyMeta called', cls, args, kwargs
        ob = object.__new__(cls, *args)
        ob.__init__(*args)
        return ob
 
print 'create class'
 
class Kls(object):
    __metaclass__ = MyMeta
 
    def __init__(self, data):
        self.data = data
 
    def printd(self):
        print self.data
 
print 'class created'

if __name__ == '__main':
    ik = Kls('arun')
