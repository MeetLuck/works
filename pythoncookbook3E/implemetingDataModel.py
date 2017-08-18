# 8.13 Implementing a Data Model or Type System

# Base class. Uses a descriptor to set a value
class Descriptor(object):
    def __init__(self,name=None,**opts):
        self.name = name
        for key,value in opts.items():
            setattr(self,key,value)
    def __set__(self,obj,value):
        obj.__dict__[self.name] = value

# Descriptor for enforcing types
class Typed(Descriptor):
    expected_type = type(None)
    def __set__(self,obj,value):
        if not isinstance(value, self.expected_type):
            raise TypeError('expected ' + str(self.expected_type) )
        super(Typed,self).__set__(obj,value)

# Descriptor for enforcing values
class Unsigned(Descriptor):
    def __set__(self,obj,value):
        if value < 0:
            raise ValueError('Expected >= 0')
        super(Unsigned,self).__set__(obj,value)

class Maxsized(Descriptor):
    def __init__(self,name=None,**opts):
        if 'size' not in opts:
            raise TypeError('missing size option')
        super(Maxsized,self).__init__(name,**opts)
    def __set__(self,obj,value):
        if len(value) >= self.size:
            raise ValueError('size must be < ' + str(self.size) )
        super(Maxsized,self).__set__(obj,value)

class Integer(Typed):
    expected_type = int

class Float(Typed):
    expected_type = float

class String(Typed):
    expected_type = str

class UnsignedInteger(Integer,Unsigned):
    pass

class UnsignedFloat(Float,Unsigned):
    pass

class SizedString(String,Maxsized):
    pass

class Stock(object):

    name = SizedString('name',size=8)
    shares = UnsignedInteger('shares')
    price = UnsignedFloat('price')

    def __init__(self,name,shares,price):
        self.name = name
        self.shares = shares
        self.price = price

if __name__ == '__main__':
    s = Stock('ACME',50,91.1)
    s.shares = -10
