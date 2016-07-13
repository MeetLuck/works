#stdout.py
import sys

print 'Dive in'
### always ave stdout before redirecting ###
saveout = sys.stdout

fsock = open('out.log', 'w')
### redirect all further output to the fsock 'out.log'
sys.stdout = fsock
print 'This message will be logged instead of diplayed'
### set stdout back to the way it was before you mucked with it.
sys.stdout = saveout
fsock.close()
