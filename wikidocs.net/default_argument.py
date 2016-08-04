''' default argument list '''

def func1(x,y):
    print locals()
    print x + y

def f(x,y= -100):
    print 'locals() : ' , locals()
    print 'f.func_default: ' ,f.func_defaults
    z = x * y
    print 'locals() : ' , locals()
    print "z = " , z
    return z
if __name__ == '__main__':

    print '*'*80
    func1(10,20)
    print '*'*80
    func1(x=10,y=20)

    print '*'*80
    f(2)
    print '*'*80
    f(x=3)
    print '*'*80
    f(x=3,y=10)


