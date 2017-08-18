# 7.11 Inlining Callback Functions

#from operator import add
from functools import wraps
from queue import Queue

def apply_async(callback,func,*args):
    print callback, func, args
    callback( func(*args) )


class Async(object):
    def __init__(self,func,args):
        self.func = func
        self.args = args

def inlined_async(func):
    @wraps(func)
    def wrapper(*args):
        print(func,args )
        f = func(*args)
        result_queue = Queue()
        result_queue.put(None)
        while True:
            result = result_queue.get()
            try:
                a = f.send(result)
                print 'a -->'
                print a , a.func, a.args 
                apply_async(result_queue.put, a.func, *a.args)
            except StopIteration:
                break
    return wrapper

def add(x,y): return x+y

@inlined_async
def test():
    r = yield Async(add, (2, 3))
    print(r)
    r = yield Async(add, ('hello', 'world'))
    print(r)

if __name__ == '__main__':
    # Simple test
    print('# --- Simple test')
    test()
