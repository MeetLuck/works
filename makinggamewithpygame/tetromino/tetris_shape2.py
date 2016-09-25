tetrisS = [
    list(  '.....' ),
    list(  '..OO.' ),
    list(  '.OO..' ),
    list(  '.....' )
   ]

tetrisZ = [
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
]

tetrisO = [
    list( '.....' ),
    list( '.OO..' ),
    list( '.OO..' ),
    list( '.....' )
]

tetrisJ = [
    list( '.....' ),
    list( '.O...' ),
    list( '.OOO.' ),
    list( '.....' )
]

tetrisL = [
    list( '.....' ),
    list( '...O.' ),
    list( '.OOO.' ),
    list( '.....' ),
]

tetrisT = [
    list( '.....' ),
    list( '..O..' ),
    list( '.OOO.' ),
    list( '.....' ),
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
    t = tetrisZ
    pieces = []
    print '*'*80
    for y in range(4): # row
        for x in range(4):
            print t[x][y],
        print 
    t = rotate90(t)
    pieces.append(t)
    print '*'*80
    for y in range(4): # row
        for x in range(4):
            print t[x][y],
        print 

#   for p in pieces:
#       print '*'*80
#       for y in range(4): # row
#           for x in range(4):
#               print p[x][y],
#           print 
