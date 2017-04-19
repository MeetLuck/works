# optparse
import optparse
# create OptionParser object
parser = optparse.OptionParser()

# ----------------- #
# add bool options  #
# ----------------- #

# case I : default : False, action = 'store_true'
# parser.add_option('-b',help='boolean option',dest='bool',
#                     default=False, action='store_true')
#  < test > 
# python bool.py
# {'bool':False},[] 
# opts.bool: False
# python bool.py -b
# {'bool':True},[] 
# opts.bool: True

# case II : default = None, action = 'store_false'
# parser.add_option('-b',help='boolean option',dest='bool',
#                 default=None, action='store_false')
#  < test > 
# python bool.py
# {'bool':None},[] 
# opts.bool: None
# python bool.py -b
# {'bool':False},[] 
# opts.bool: False

# case III : not use default,action 
parser.add_option('-b',help='boolean option',dest='bool',)
#  < test > 
# python bool.py
# {'bool':None},[] 
# opts.bool: None
# python bool.py -b
# error : -b option requires option

# parse arguments
opts, args = parser.parse_args()

# test
# python bool.py
# {'bool':False},[] 
# opts.bool: False
# python bool.py -b
# {'bool':True},[] 
# opts.bool: True
print opts, args
print opts.bool
