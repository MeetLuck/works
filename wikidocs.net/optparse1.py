import optparse
parser = optparse.OptionParser()
parser.add_option('-f','--file')
parser.add_option('-q','--quiet',action='store_true',default=False)
argv = '-f outfile --quiet'.split()
opts, args = parser.parse_args(argv) 
print opts
argv = '--quiet --file outfile'.split()
opts, args = parser.parse_args(argv) 
print opts
argv = '-q -foutfile'.split()
opts, args = parser.parse_args(argv) 
print opts
argv = '-q --file=outfile'.split()
opts, args = parser.parse_args(argv) 
print opts
argv = '-qfoutfile'.split()
opts, args = parser.parse_args(argv) 
print opts
