def check_sets(*t):
    print 't',t
    sets = set(['a','b','c'])
    for need, have in zip(t, sets):
        print need,have
        if need > have: return False
    return True
check_sets(2)
check_sets(1,2)

