from __future__ import division
import os
cls = lambda:os.system('cls')
def pi_series():
    sum = 0
    i = j = 1
    while 1:
        sum += j/i
        yield 4 * sum
        i += 2; j = -j

def firstN(g,N):
    for i in range(N):
        yield g.next()

#print list(firstN(pi_series(),20))

def f():
    val = 0
    while True:
        print '>> line 2, val={val}'.format(val=val)
        val = yield
        print '>> line 4, val={val}'.format(val=val)
        yield 10*val
        print '>> line 6, val={val}'.format(val=val)

g = f()
print g.send(None)
print g.send(1)
print g.next()
print g.send(2)
cls()
def minimize():
    current = yield
    print 'current = {current}'.format(current = current)
    while True:
        value = yield current
        print 'current,value = {c},{v}'.format(c = current,v=value)
        current = min(value, current)

it = minimize()
next(it)
print it.send(10)
print it.send(4)
print it.send(22)
print it.send(-1)

cls()
def receiver():
    while True:
        item = (yield 100) + '->'
        print 'Got', item

recv = receiver()
print next(recv)
print recv.send("Hello")
print recv.send("World")


