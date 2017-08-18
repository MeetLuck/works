# 9.5 Defining a Decorator with User Adjustable Attributes

import functools
import logging

# Utility decorator to attach a function as an attribute of obj
def attach_wrapper(obj,func=None):
    if func is None:
        return functools.partial(attach_wrapper,obj)
    setattr(obj,func.__name__,func)
    return func

def attach(obj):
    def _attach(func):
        setattr(obj,func.__name__,func)
        return func
    return _attach


def logged(level,name=None,message=None):
    ''' Add logging to a function,log level,log name, log message'''
    def decorate(func):

        decorate.logmsg  = message if message else func.__name__
        decorate.level = level
        logname = name if name else func.__module__
        log = logging.getLogger(logname)

        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            log.log(decorate.level,decorate.logmsg)
            return func(*args,**kwargs)

        # Attach setter function
        @attach(wrapper)
        def set_level(newlevel):
            decorate.level = newlevel
#       setattr(wrapper,set_level.__name__,set_level)

        @attach_wrapper(wrapper)
        def set_message(newmsg):
            decorate.logmsg = newmsg

        return wrapper

    return decorate
            
def test():
    @logged(logging.DEBUG)
    def add(x,y):
        return x+y
    logging.basicConfig(level=logging.DEBUG)
    print add(2,3)
    # change the log message
    add.set_message('Add called')
    print add(2,3)
    # change the log level
    add.set_level(logging.WARNING)
    print add(2,3)

if __name__ == '__main__':
    test()
