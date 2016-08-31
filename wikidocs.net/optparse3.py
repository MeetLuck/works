import optparse
def foo_callback(option, opt_str, value, parser):
    parser.values.foo = True
    print 'callback for %s' %opt_str
    print '\topt_str: ',opt_str
    print '\tdest :', option.dest
    print '\topts: ', parser.values

def check_order(option, opt_str, value, parser):
    if parser.values.b:
        raise optparse.OptionValueError("can't use %s after -b" % opt_str)
    setattr(parser.values, option.dest,True)
    print 'check option order for %s' %opt_str
    print '\toption: ',option
    print '\topt_str: ',opt_str
    print '\tdest :', option.dest
    print '\topts: ', parser.values

def store_value(option, opt_str, value, parser):
    setattr(parser.values, option.dest, value)
    print 'emulate store action for %s' %opt_str
    print '\toption: ',option
    print '\topt_str: ',opt_str
    print '\tvalue: ',value
    print '\tdest :', option.dest
    print '\topts: ', parser.values

parser = optparse.OptionParser()
#parser.add_option('-f','--foo', action='callback', callback=foo_callback)
#argv = '--foo'.split()
#parser.add_option('-a', action = 'callback', callback=check_order, dest='a')
#parser.add_option('-b', action = 'store_true', dest='b')
#parser.add_option('-c', action = 'callback', callback=check_order, dest='c')
#argv = '-acb'.split()
#argv = '-abc'.split()
#argv = '-b -a'.split()
parser.add_option('--foo', action='callback', callback=store_value, type='int', nargs=3, dest='foo')
argv = '--foo 1 2 3'.split()
opts,args = parser.parse_args(argv) 
print opts
