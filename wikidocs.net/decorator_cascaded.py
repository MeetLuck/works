def A(func):
    def wrapper1(*args):
        print 'A=>{}{}'.format(func,str(args) )
        val = func(*args)
        return val
    return wrapper1

def B(func): # func = <function wrapper1>
    def wrapper2(*args):
        print 'B=>{}{}'.format(func,str(args) )
        val = func(*args)
        return val
    return wrapper2

@B
@A
def f(*args):
    print 'calling original f{}'.format(args)
    return 

f(1,2,3)
print'-'*40

def g(*args):
    print 'calling original g{}'.format(args)
    return 
g = B(A(g))

g(1,2,3)
