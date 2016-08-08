class curry:
    """from Scott David Daniels'recipe
    "curry -- associating parameters with a function"
    in the "Python Cookbook"
    http://aspn.activestate.com/ASPN/Python/Cookbook/
    """
    def __init__(self, fun, *args, **kwargs):
        self.fun = fun
        self.pending = args[:]
        self.kwargs = kwargs.copy()
    def __call__(self, *args, **kwargs):
        if kwargs and self.kwargs:
            kw = self.kwargs.copy()
            kw.update(kwargs)
        else:
            kw = kwargs or self.kwargs
        return self.fun(*(self.pending + args), **kw)
def fcurry(fn, *cargs, **ckwargs):
    def call_fn(*fargs, **fkwargs):
        d = ckwargs.copy()
        d.update(fkwargs)
        return fn(*(cargs + fargs), **d)
    return call_fn

def event_lambda(f, *args, **kwds ):
    """A helper function that wraps lambda in a prettier interface.
    Thanks to Chad Netzer for the code."""
    return lambda event, f=f, args=args, kwds=kwds : f( *args, **kwds )

def mysum(seq,n):
    li = seq[:]
    print sum(x**n for x in li)
    return

f1 = curry(mysum,range(1,11))
f1(1); f1(2); f1(3)
f2 = curry(mysum,range(1,11))
f2(1); f2(2); f2(3)
from functools import partial
f3 = partial(mysum, range(1,11))
f3(1); f3(2); f3(3)



