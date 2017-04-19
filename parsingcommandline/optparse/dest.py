# --------------------- #
# destination types     #
# --------------------- #

# optparse
import optparse
# create OptionParser object
parser = optparse.OptionParser()
# add options
# parser.add_option('-n',help='integer arguments',dest='num1', action='store',type='int',default=10)
parser.add_option('-n',help='integer arguments',dest='num1', action='store',type='int',nargs=2,
                  default=(10,20) )
# parse arguments
opts, args = parser.parse_args()

# test

print 'opts: ',opts, 'args: ',args
print 'opts.num1: ',opts.num1
print 'sum = ',sum(opts.num1)
