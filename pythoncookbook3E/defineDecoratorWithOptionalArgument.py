# 9.6 Defining a Decorator That Takes an Optional Argument
import functools
import logging
logging.basicConfig(level=logging.DEBUG)

def logged(func=None,level=logging.DEBUG, name= None, message=None):
    if func is None:
        return functools.partial(logged, level=level,name=name,message=message)
    logname = name if name else func.__module__
    logmsg  = message if message else func.__name__
    log = logging.getLogger(logname)
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        log.log(level,logmsg)
        return func(*args,**kwargs)
    return wrapper

def test():
    @logged
    def add(x,y):
        print(x+y)
        return x + y
    @logged(level=logging.WARNING,name='example')
    def spam():
        print( 'Spam!' )
    add(2,3)
    spam()

if __name__ == '__main__':
    test()


