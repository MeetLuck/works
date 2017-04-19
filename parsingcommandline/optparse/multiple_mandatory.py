# optparse
import optparse
# create OptionParser object
parser = optparse.OptionParser()

# --------------------------- #
# multiple mandatory options  #
# --------------------------- #

parser.add_option('-m',help='mandatory option',dest='man', action='store_true')
parser.add_option('-p',help='mandatory option',dest='pan', action ='store_true')
# parse arguments
opts, args = parser.parse_args()
# make sure all mandatory options appeared
mandatories = ['man','pan']
for m in mandatories:
    if not opts.__dict__[m]:
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
print dir(opts.man)
print opts.man
