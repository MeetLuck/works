import sys
print 'arguments list:', sys.argv
for i, arg in enumerate(sys.argv):
    print 'arg[{i}]: {arg}'.format(i=i,arg=arg)
print sys.path[0]
