# 20.8 Adding a Method to a Class Instance at Runtime

def add_method_to_objects_class(obj, method, name=None):
    if name is None:
        name = method.func_name
    class NewClass(obj.__class__):
        pass
    setattr(NewClass, name, method)
    obj.__class__ = NewClass

import inspect
def _rich_str(self):
    pieces = list()
    for name,value in inspect.getmembers(self):
        # do not display specials
#       if name.startswith('__'): continue
#       print 'name,value : %s, %s' %(name, value)
        # do not display the object's own methods
#       if inspect.ismethod(value) and value.im_self is self: continue
        pieces.append( name.ljust(15) + '\t' + str(value) +'\n')
#       pieces.extend( (name.ljust(15),'\t',str(value),'\n'))

    return ''.join(pieces)

def set_rich_str(obj, on=True):
    def isrich():
        attr = getattr(obj.__class__.__str__, 'im_func',None)
#       print obj.__class__.__str__
        print 'attr: ',attr
        return getattr(obj.__class__.__str__, 'im_func',None) is _rich_str
    if on:
#       if not isrich():
        add_method_to_objects_class(obj, _rich_str, '__str__')
    else:
        if not isrich(): return
        bases = obj.__class__.__bases__
        assert len(bases) == 1
        obj.__class__ = bases[0]
        assert not isrich()

if __name__ == '__main__':
    class Foo(object):
        def __init__(self,x=23,y=42):
            self.x,self.y = x,y
        def show(self):
            self.total = self.x + self.y
    print '*'*80
    f = Foo(); set_rich_str(f); print f
    print '*'*80
    g = Foo(); set_rich_str(g,False); print g
