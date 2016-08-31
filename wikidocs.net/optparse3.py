import optparse
def foo_callback(option, opt_str, value, parser):
    parser.values.foo = True
    print 'trivial callback:'
    print '\toption: ',option
    print '\topt_str: ',opt_str
    print '\topts: ', parser.values

def check_order(option, opt_str, value, parser):
    if parser.values.b:
        raise optparse.OptionValueError("can't use -a after -b")
    parser.values.a = True
    print 'check option order:'
    print '\toption: ',option
    print '\topt_str: ',opt_str
    print '\topts: ', parser.values

parser = optparse.OptionParser()
#parser.add_option('-f','--foo', action='callback', callback=foo_callback)
#argv = '--foo'.split()
parser.add_option('-a', action = 'callback', callback=check_order)
parser.add_option('-b', action = 'store_true', dest='b')
argv = '-a -b'.split()
#argv = '-b -a'.split()
opts,args = parser.parse_args(argv) 
print opts
