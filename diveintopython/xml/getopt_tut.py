from getopt import getopt
''' getopt.opt parses an argument sequence, such as sys.argv and returns
>>> a sequence of (option, argument) pairs and a sequence of non-option arguments.
>>> supported option systax:
        -a
        -bval
        -b val
        --noarg
        --witharg=val
        --witharg val
>>> getopt( args, shortopts,longopts=[] )
    args: sys.argv[1:]
    shortopts:
        the option definition string for single character options
        if one of the options requires an argument, its letter is followed
        by a colon.
    longopts = []:
        a sequence of the long-style option names such as --noarg or --widtharg
        if any long option requires an argument, its name should have a suffix of =
'''

#----------- Short Form Options ---------------------
# If a program wants to take 2 options, -a and -b with the b option requiring 
# an argument, the value should be 'ab:'
args = ['-a','-bval']
print getopt(args,'ab:')
#----------- Long Form Options ----------------------
# If a program takes 2 options, --noarg and --witharg,
# the sequence should be ['noarg','witharg=']
args = ['-n', '--noarg','--witharg','val','--witharg2=val2']
print getopt( args,'n',['noarg','witharg=','witharg2='] )

#----------------- takes 5 options -------------------
'''
>>> -o,-v, --ouput, --verbose, and --version
>>> -o, --ouput, and --version options require an argument
'''
print '*'*80

import sys
version = '1.0'
verbose = False
output_filename = 'default.out'
print 'ARGV   :', sys.argv[1:]
options, remainder = getopt(sys.argv[1:], 'o:v',['output=','verbose','version='] )
print 'OPTIONS  :', options

for opt, arg in options:
    if opt in ('-o','--ouput'):
        output_filename = arg
    elif opt in ('-v','--verbose'):
        verbose = True
    elif opt == '--version':
        version = arg
print 'version  :', version
print 'verbose  :', verbose
print 'output  :', output_filename
print 'remaining  :', remainder


