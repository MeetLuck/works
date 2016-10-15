tetrisS = [
    list(  '.....' ),
    list(  '.....' ),
    list(  '..OO.' ),
    list(  '.OO..' ),
    list(  '.....' )
   ]

tetrisZ = [
    list( '.....' ),
    list( '.....' ),
    list( '.OO..' ),
    list( '..OO.' ),
    list( '.....' )
]

tetrisI = [
    list( '..O..' ),
    list( '..O..' ),
    list( '..O..' ),
    list( '..O..' ),
    list( '.....' )
]

tetrisO = [
    list( '.....' ),
    list( '.....' ),
    list( '.OO..' ),
    list( '.OO..' ),
    list( '.....' )
]

tetrisJ = [
    list( '.....' ),
    list( '.O...' ),
    list( '.OOO.' ),
    list( '.....' ),
    list( '.....' )
]

tetrisL = [
    list( '.....' ),
    list( '...O.' ),
    list( '.OOO.' ),
    list( '.....' ),
    list( '.....' )
]

tetrisT = [
    list( '.....' ),
    list( '..O..' ),
    list( '.OOO.' ),
    list( '.....' ),
    list( '.....' )
]

if __name__ == '__main__':

    from rotateXY import rotate90
    '''
    t = tetrisI
    for row in t:
        print row
    t = rotate90(t)
    print '-'* 80
    for row in t:
        print row
    t = rotate90(t)
    print '-'* 80
    for row in t:
        print row
    '''
    t = tetrisZ[:]
    pieces = []
    for row in t:
        print ''.join(row)
    print '-'*80
    print '-'*80
#   t1 = rotate90(t)
#   for row in t1:
#       print row
    import copy
    for i in range(4):
        t = rotate90(t)
#       for row in t:
#           print ''.join(row)
        pieces.append(t[:])
#       print
#       print

    for p in pieces:
        print '*'*80
        for row in p:
            print ''.join(row)
