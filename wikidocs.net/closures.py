def outer():
    free = 10
    print 'free: ', free
    def inner(a):
        y = free + a
        print locals()
        print globals()
        return y
    return inner
f = outer()
print f(20)
print f(30)


