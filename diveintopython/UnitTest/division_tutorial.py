''' divmod(x,y) -> (quotient, remainder)
    return the tuple ( (x-x%y)/y, x%y )
    div,mod = divmod(x,y),  div*y + mod == x
'''
def divmod2(x,y):
    ''' using ONLY add, substract
    q = 0
    while x >= y:
        x -=  y
        q += 1
    return q,x
    '''
    quotient  = 0
    remainder = x 
    while remainder >= y:
        remainder -=  y
        quotient  +=  1
#       print quotient,remainder
    return quotient, remainder 

def divmod3(x,y):
    ''' 
    q = int(x/y)
    r = x % y
    return q,r
    '''
    q = int(x/y)
    r = x % y
    return q,r


def main():
    ''' divmod2 doctest
    >>> x,y = 2,3
    >>> div,mod = divmod2(x,y)
    >>> assert div*y + mod == x
    >>> x,y = 10,3
    >>> div,mod = divmod2(x,y)
    >>> assert div*y + mod == x
    >>> x,y = 5, 2.5
    >>> div,mod = divmod2(x,y)
    >>> assert div*y + mod == x
    >>> x,y = 2,3
    >>> div,mod = divmod3(x,y)
    >>> assert div*y + mod == x
    >>> x,y = 10,3
    >>> div,mod = divmod3(x,y)
    >>> assert div*y + mod == x
    >>> x,y = 5, 2.5
    >>> div,mod = divmod3(x,y)
    >>> assert div*y + mod == x
    '''

if __name__ == '__main__':
    import doctest
    doctest.testmod()
#   print divmod2(10,3.0)
#   print divmod2(1,3.0)
#   print divmod2(5,2.5)
#   print divmod2(7,3)
