# --------------------- #
#     meta var          # 
# --------------------- #

# optparse
import optparse
# create OptionParser object
parser = optparse.OptionParser()
# add option
parser.add_option('-s',help='single argument',dest='signle', action='store',metavar='<ARG>')
parser.add_option('-M',help='multiple argument',dest='multi', action='store',
                   metavar='<ARG1> <ARG2>', nargs=2)
# parse arguments
opts, args = parser.parse_args()

# test
'''
> metavar.py -h
Usage: metavar.py [options]

Options:
      -h, --help        show this help message and exit
      -s <ARG>          single argument
      -M <ARG1> <ARG2>  multiple argument

> metavar.py -s 10 -M 20 30
opts:  {'multi': ('20', '30'), 'signle': '10'} args:  []
'''

print 'opts: ',opts, 'args: ',args
