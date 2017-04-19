# optparse
import optparse
# create OptionParser object
parser = optparse.OptionParser()

# ------------------ #
# mandatory options  #
# ------------------ #

parser.add_option('-m',help='mandatory option',dest='mandatory',
                   action='store_true')
# parse arguments
opts, args = parser.parse_args()
if opts.mandatory is None:
    print "A mandatory option is missing"
    parser.print_help()
    exit(-1)

# test
# python mandatory.py
#
# A mandatory option is missing
# Usage: mandatory.py [options]

# Options:
#   -h, --help  show this help message and exit
#   -m          mandatory option

# python mandatory.py -m args
# mandatory.py -m args
# {'mandatory': True} ['args']
print opts, args
print opts.mandatory
