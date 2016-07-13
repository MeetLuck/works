for i in range(3):
    print 'Dive in %d' %i
import sys
for i in range(3):
    sys.stdout.write('Dive in')

print
for i in range(3):
    sys.stderr.write('Dive in')
