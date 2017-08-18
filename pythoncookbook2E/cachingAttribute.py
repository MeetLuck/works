# 20.4 Caching Attribute Values
# __get__ called only if there is no attribute

class CachedAttribute(object):
    ''' computes attribute value and caches it in the instance.'''
    def __init__(self,method,name=None):
        # record the unbound method and the name
        self.method = method
        self.name = name or method.__name__
    def __get__(self,inst,cls):
        if inst is None: # instance attribute accessed on class
            return self
        # compute, cache and return instance's attribute
        result = self.method(inst)
        setattr(inst, self.name, result)
        return result

class CachedClassAttribute(CachedAttribute):
    ''' computes attribute value and caches it in the class '''
    def __get__(self,inst,cls):
        # just delegate to CachedAttribute, with 'cls' as 'instance'
        return super(type(self), self).__get__(cls,cls)


class MyObject(object):
    def __init__(self,n):
        self.n = n
    @CachedAttribute
    def square(self):
        return self.n ** 2
    @staticmethod
    def test():
        m = MyObject(9)
        print vars(m)
        print m.square
        print vars(m)
        m.n = 10
        print vars(m)

class MyClass(object):
    class_attr = 11
    @CachedClassAttribute
    def square(cls):
        return cls.class_attr**2
    @staticmethod
    def test():
        x = MyClass()
        y = MyClass()
        print x.square
        print y.square
        del MyClass.square
        print x.square

if __name__ == '__main__':
#   MyObject.test()
    MyClass.test()
