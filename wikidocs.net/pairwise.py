def pairwise(iterable):
    's -> (s0,s1), (s1,s2), (s2,s3), ... '
    a,b = tee(iterable)
    next(b,None)
    return izip(a,b)

if __name__ == '__main__':
    from itertools import *
    pw = pairwise([0,1,2,3,4,5])
    print list(pw)
