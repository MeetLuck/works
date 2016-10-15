def rotate90(lst):
    '''
    >>> # rotate +90 degrees
    >>> list = [
    ...     [1,2,3],
    ...     [4,5,6],
    ...     [7,8,9]
    ...        ]
    >>> list.reverse() = [ 
    ...     [7,8,9],
    ...     [4,5,6],
    ...     [1,2,3],
            ]
    >>> # (x,y) -> (y,x)
    >>> transpose = [ 
    ...     (7,4,1),
    ...     (8,5,2),
    ...     (9,6,3),
            ]
    >>> # rotate -90 degrees
    >>> list = [
    ...     [1,2,3],
    ...     [4,5,6],
    ...     [7,8,9]
    ...        ]
    >>> # (x,y) -> (y,x)
    >>> transpose = [ 
    ...     (1,4,7),
    ...     (2,5,8),
    ...     (3,6,9),
            ]
    >>> list.reverse() = [ 
    ...     [3,6,9],
    ...     [2,5,8],
    ...     [1,4,7],
            ]
    '''
    import copy
    #lst = copy.deepcopy(lst)
    lst.reverse()
    return zip(*lst)

def symmetricY(lst):
    '''
    >>> list = [
    ...     [1,2,3],
    ...     [4,5,6],
    ...     [7,8,9]
    ...        ]
    >>> # symmetric w.r.t. Y 
    >>> list.reverse()
    ...     [
    ...     [7,8,9],
    ...     [4,5,6],
    ...     [1,2,3],
            ]
    '''
    import copy
    lst = copy.deepcopy(lst)
    return lst.reverse()


if __name__ == '__main__':
    li = [
        [1,2,3],
        [4,5,6],
        [7,8,9]
        ]
    li90 = rotate90(li)
    print '*'*80
    print li90
    for row in li90:
        print row
    li = [
        [1,  2,  3,  4],
        [5,  6,  7,  8],
        [9,  10, 11, 12],
        [13, 14, 15, 16]
        ]
    li90 = rotate90(li)
    print '*'*80
    print li90
    for row in li90:
        print row

