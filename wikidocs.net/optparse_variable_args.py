import optparse

def vargs_callback(option, opt_str, value, parser):
    assert value is None
    value = list()
    print '\topt_str: ',opt_str
    print '\tvalue :', value
    print '\tparser.rargs :', parser.rargs
    print '\tparser.largs :', parser.largs
    def floatable(str):
        try:
            float(str)
            return True
        except ValueError:
            return False
    for arg in parser.rargs:
        # stop on --foo like options
        if arg[:2] == '--' and len(arg)>2:
            break
        # stop on -a, but not on -3 or -3.0
        if arg[:1] == '-' and len(arg)>1 and not floatable(arg):
            break
        value.append(arg)
    del parser.rargs[:len(value)]
    setattr(parser.values, option.dest, value)
    print 'variable arguments for %s' %opt_str
    print '\toption: ',option
    print '\tdest :', option.dest
    print '\topts: ', parser.values

parser = optparse.OptionParser()
parser.add_option('-c','--callback', dest='vargs_attr', action='callback', callback=vargs_callback)
argv = '--callback -1.0 2.0 3.0 4.0'.split()
#argv = '-b -a'.split()
opts,args = parser.parse_args(argv) 
print opts
