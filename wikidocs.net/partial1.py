class partial(object):
    def __init__(*args, **kw):
        self = args[0]
        self.fn = args[1]
        self.args = args[2:]
    def __call__(self,*args):
        return self.fn( *(self.args + args) )

def curry(fn, *cargs):
    def call_fn(*fargs):
        return fn( *(cargs + fargs) )
    return call_fn

def seq_pow(li,exponent):
    seq = li[:]
    y = [ x**exponent for x in seq ]
    return y 

li = [1,2,3,4,5]
x = partial(seq_pow,li)
y = curry(seq_pow, li)
print x(2)
print x(3)
print y(4)
print y(5)

