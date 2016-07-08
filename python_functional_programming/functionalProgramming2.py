#----- 13.9 Lab -------------------
# functional-1-reduce.py
def add_powers(power):
    '''
    >>> series1 = (0,1,2,3,4,5)
    >>> series2 = (2,4,8,16,32)
    >>> power_reducer = add_powers(2)
    >>> power_reducer(series1)
    55
    >>> power_reducer(series2)
    1364
    >>> power_reducer = add_powers(3)
    >>> power_reducer(series1)
    225
    >>> power_reducer(series2)
    37448
    '''
    def mypowers(lst):
        return reduce(lambda x,y:x+pow(y,power),lst, 0 )
    return mypowers
if __name__ == '__main__':
#   series1 = (0,1,2,3,4,5)
#   p = add_powers(2)
#   print p(series1)
    import doctest
    doctest.testmod()
