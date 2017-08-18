# 9.8 Defining Decorators As Part of a Class
import functools

class A(object):
    # decorator as an instance method
    def decorator1(self,func):
        def wrapper(*args,**kwargs):
            print '@Decorator 1'
            return func(*args,**kwargs)
        return wrapper
    # decorator as a class method
    @classmethod
    def decorator2(cls,func):
        def wrapper(*args,**kwargs):
            print '@Decorator 2'
            return func(*args,**kwargs)
        return wrapper
    @staticmethod
    def test():
        a = A()
        @a.decorator1
        def spam():
            print 'method Spam!'
        @A.decorator2
        def grok():
            print 'method Grok!'

        spam()
        grok()

class Person(object):
    # create a property instance
    firstname = property()
    # apply decorator methods
    @firstname.getter
    def firstname(self):
        return self._firstname
    @firstname.setter
    def firstname(self,value):
        if not isinstance(value,str):
            raise TypeError('Expected a string')
        self._firstname = value

    @staticmethod
    def test():
        jane = Person()
        try:
            print jane.firstname
        except AttributeError:
            jane.firstname = 'Jane'
            print jane.firstname

if __name__ == '__main__':
#   A.test()
    Person.test()
