# stderr.py
import sys

fsock = open('error.log', 'w')
### redirect standard error to fsock
sys.stderr = fsock
raise Exception, 'this error will be logged'
