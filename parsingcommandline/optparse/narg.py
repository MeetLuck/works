# --------------------- #
# number of arguments   #
# --------------------- #

# optparse
import optparse
# create OptionParser object
parser = optparse.OptionParser()
# add one or more arguments
parser.add_option('-m',help='multiple arguments',dest='multi', action='store',nargs=2)
# parse arguments
opts, args = parser.parse_args()

# test
#  narg.py -m arg1 arg2 lefts
# opts:  {'multi': ('arg1', 'arg2')} args:  ['lefts']
# opts.multi:  ('arg1', 'arg2')

print 'opts: ',opts, 'args: ',args
print 'opts.multi: ',opts.multi
