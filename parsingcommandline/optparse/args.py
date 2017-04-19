# optparse
import optparse
# create OptionParser object
parser = optparse.OptionParser()
# add options
parser.add_option('-n','--new',help='create a new object')
# parse arguments
opts, args = parser.parse_args()

# run
# python args.py -n opts args
# {'new':'opts'}, ['args']
print opts, args
print opts.new, args[0]
