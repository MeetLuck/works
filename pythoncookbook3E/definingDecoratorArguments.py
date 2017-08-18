# 9.4 Defining a Decorator That Takes Arguments
import functools
import logging

def logged(level,name=None,message=None):
    ''' Add logging to a function. level is logging level
        name is logger name, message is log message'''
    def decorate(func):
        logname = name if name else func.__module__  
        logmsg = message if message else func.__name__
        log = logging.getLogger(logname)
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            log.log(level,logmsg)
            return func(*args,**kwargs)
        return wrapper
    return decorate

def test():
    @logged(logging.DEBUG)
    def add(x,y):
        return x+y
    @logged(logging.CRITICAL,'example')
    def spam():
        print 'Spam!'
    print repr( add(2,3) )
    print repr( spam()  )

if __name__ == '__main__':
    test()
