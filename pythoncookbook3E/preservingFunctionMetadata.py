# 9.2 Preserving Function Metadata When Writing Decorators
import time
import functools
import inspect
import sys

def timethis(func):
    ''' decorator that reports the execution time '''
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        start = time.time()
        result = func(*args,**kwargs)
        end = time.time()
        print '%s took %s seconds' %(func.__name__, end-start)
        return result
    if sys.version[0] == str(2):
        wrapper.__wrapped__ = func
    return wrapper

def test():

    @timethis
    def countdown(n):
        'couns down for n seconds'
        print 'countdown starts...'
        while n > 0:
            n -= 1
            time.sleep(1)
        else:
            print 'coundown ends...'
#   print 'METADATA'
#   print 'name: ',countdown.__name__
#   print 'doc: ', countdown.__doc__
#   print 'annotation: ', countdown.__annotations__
    print vars(countdown)
    countdown.__wrapped__(2)
#   print inspect.signature(countdown)
    
#   countdown(3)
#   countdown(5)

if __name__ == '__main__':
    test()
