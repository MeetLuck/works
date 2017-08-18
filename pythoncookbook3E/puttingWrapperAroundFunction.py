# 9.1 Putting a Wrapper Around a Function

import time
from functools import wraps

def timethis(func):
    ''' decorator that reports the execution time '''
    @wraps(func)
    def wrapper(*args,**kwargs):
        start = time.time()
        result = func(*args,**kwargs)
        end = time.time()
        print func.__name__, end-start
        return result
    return wrapper

def test():

    @timethis
    def countdown(n):
        while n > 0:
            n -= 1
    K,M,G = 1e3,1e6,1e9
    countdown(M)
    countdown(G)

if __name__ == '__main__':
    test()
