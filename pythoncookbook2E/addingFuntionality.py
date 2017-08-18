# 20.6 Adding Funtionality to a Class by Wrapping a Method

import inspect

def wrapfunc(obj, name, processor, avoid_doublewrap=True):
    ''' patch obj.<name> so that calling it actually calls, instead,
        processor(original_callable, *arg, **kwargs) '''
    # get the callable at obj.<name>
    call = getattr(obj,name)
    # optionally avoid multiple idential wrappings
    if avoid_doublewrap and getattr(call,'processor',None) is processor:
        return
    # get underlying function, and anyway def the wrapper closure
    original_callable = getattr(call,'im_func',call)
    def wrappedfunc(*args,**kwargs):
        return processor(original_callable,*args,**kwargs)
    # set attributes, for future unwrapping and to avoid doulbe-wrapping
    wrappedfunc.original = call
    wrappedfunc.processor = processor
    wrappedfunc.__name__ = getattr(call,'__name__',name)
    # rewrap staticmethod and classmethod specifically(iff obj is a clss)
    if inspect.isclass(obj):
        if hasattr(call,'im_self'):
            if call.im_self:
                wrappedfunc = classmethod(wrappedfunc)
        else:
            wrappedfunc = staticmethod(wrappedfunc)
    # finally, install the wrapper closure as requested
    setattr(obj,name, wrappedfunc)

def unwrapfun(obj,name):
    ''' undo the effects of wrapfunc(obj,name,processor)'''
    setattr(obj, name, getattr(obj,name).original)


def tracing_processor(original_callable, *args, **kwargs):
    r_name = getattr(original_callable,'__name__','<unknown>')
    r_args = map(repr, args)
    r_args.extend( ['%s=%r' %x for x in kwargs.iteritems() ] )
    print 'begin call to %s(%s)' %(r_name, ', '.join(r_args))
    try:
        result = original_callable(*args, **kwargs)
    except:
        print 'EXCEPTION in call to %s' %r_name
        raise
    else:
        print 'call to %s result: %r' %(r_name,result)
        return result

def add_tracing_prints_to_method(class_object, method_name):
    wrapfunc(class_object, method_name, tracing_processor)

def processedby(processor):
    ''' decorator to wrap the processor around a function'''
    def processedfunc(func):
        def wrappedfunc(*args,**kwargs):
            return processor(func,*args,**kwargs)
        return wrappedfunc
    return processedfunc

class SomeClass(object):
    @processedby(tracing_processor)
    def amethod(self,s):
        return 'Hello, ' + s

class Circle(object):
    def __init__(self,r):
        self.r = r
    def show(self):
        import math
        self.area = math.pi * self.r ** 2 
        return self.area

#print dir(Circle)
Circle(2)
add_tracing_prints_to_method(Circle, 'show')
Circle(2).show()
#print dir(Circle)
