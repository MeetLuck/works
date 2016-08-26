def product(*args, **kwds):
    '(A+B+C+D)(x+y)'
    # product('ABCD','xy') -> Ax Ay Bx By Cx Cy Dx Dy
    '(0+1)(0+1)(0+1)'
    # product(range(2), repeat=3) -> 000 001 010 011 100 101 110 111
    pools = map(tuple, args) * kwds.get('repeat',1)
    result = [[]]
    for pool in pools:
        print 'result: ',result
        print 'pool: ', pool
        result = [ x+[y] for x in result for y in pool ]
    for prod in result:
        yield tuple(prod)

if __name__ == '__main__':
    p = product('ABCD','xy')
    print list(p)
    p = product(range(2), repeat=3)
    print list(p)




