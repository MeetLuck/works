''' shift sequence '''
def shift(seq,direction=1):
    if direction ==1: # right shift
        seq.insert(0, seq.pop())
    elif direction == -1: # left shift
        seq.insert(len(seq),seq.pop(0))



if __name__ == '__main__':
    li = [1,2,3]
    print '\nshift left'
    print 0,li
    for i in range(len(li)):
        shift(li)
        print i+1,li

    li = [1,2,3]
    print '\nshift left'
    print 0, li
    for i in range(len(li)):
        shift(li,-1)
        print i+1,li
