# 20.8 Adding a Method to a Class Instance at Runtime

def add_method_to_objects_class(obj, name, method):
    class NewClass(obj.__class__):
        pass
    setattr(NewClass, name, method)
    obj.__class__ = NewClass

import inspect
def _rich_str(self):
    pieces = list()
    for name,value in inspect.getmembers(self):
        pieces.append( name.ljust(15) + '\t' + str(value) +'\n')
    return ''.join(pieces)

if __name__ == '__main__':
    class Foo(object):
        def __init__(self,x=23,y=42):
            self.x,self.y = x,y
            self.show()
        def show(self):
            self.total = self.x + self.y
        __str__ = _rich_str
#       def __str__(self):
#           pieces = list()
#           for name,value in inspect.getmembers(self):
#               pieces.append( name.ljust(15) + '\t' + str(value) +'\n')
#           return ''.join(pieces)

    print '*'*80
    f = Foo()
    print type(f),type(f).__bases__; print f
    print '*'*80
    add_method_to_objects_class(f, '__str__',_rich_str)
#   set_rich_str(f)
    print type(f),type(f).__bases__; print f
#   print '*'*80
#   print vars(f)
