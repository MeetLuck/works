from __future__ import print_function
''' Iterators, generators and decorators
>>> Iterators
    __iter__   returns the iterator object itself. This is used in 'for' and 'in' statements
    __next__   returns the next value from the iterator.
               If there is No More Items to return, it should raise StopInteration exception
'''
class Counter(object):
    def __init__(self, low, high):
        self.current, self.high = low, high
    def __iter__(self):
        return self
    def next(self):
        ' Python >= 3, use __next__ '
        if self.current > self.high:
            raise StopIteration
        else:
            self.current += 1
            return self.current - 1

''' Generators
>>> It is an easy way to create iterators using a keyword yield from a function
'''
def myGenerator():
    print('Inside my generator')
    yield 0
    yield 1
    yield 2

if __name__ == '__main__':
    c = Counter(5,10)
    for i in c:
        print( i, end=' ')

    print( '\nnext---------------------------' )
    c = Counter(5,6)
    print( c.next() )
    print( c.next() )
#   print( c.next() )

    print( '\nnext---------------------------' )
    iterator = iter(Counter(5,10))
    while True:
        try:
            x = iterator.next()
            print( x, end = ' ' )
        except StopIteration as e:
            break
    print( '\n---------- Generators ---------------------------' )
    print( '\nnext---------------------------------------------' )
    g = myGenerator()
    print( dir(g) )
    print( g.__class__, g.next )
    for i in g:
        print(i)
