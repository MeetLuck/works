# 8.9 Creating a New Kind of Class or Instance Attribute

# Descriptor for a type-checked attribute
class Typed(object):
    def __init__(self,name,expected_type):
        self.name = name
        self.expected_type = expected_type
    def __get__(self,instance,cls):
        if instance is None: return self
        return instance.__dict__[self.name]
    def __set__(self,instance,value):
        if not isinstance(value, self.expected_type):
            raise TypeError('Expected '+ str(self.expected_type) )
        instance.__dict__[self.name] = value
    def __delete__(self,instance):
        del instance.__dict__[self.name]

# class decorator that applies it to selected attributes
def type_assert(**kwargs):
    def decorate(cls):
        for name, expected_type in kwargs.items():
            # Attach a Typed descriptor to the class
            setattr(cls,name, Typed(name,expected_type) )
        return cls
    return decorate

# example use
if __name__ == '__main__':
    @type_assert(name=str, share=int,price=float)
    class Stock(object):
        def __init__(self,name,shares,price):
            self.name = name
            self.shares = shares
            self.price = price
    stock = Stock('AAPL',50,10000.0)
    print stock.name,stock.shares,stock.price
    stock.name = 'GOOG'
    stock.price = 4000.0
    print stock.name,stock.shares,stock.price

