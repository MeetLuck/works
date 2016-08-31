import optparse
parser = optparse.OptionParser()
parser.add_option('--clobber', action='store_true', dest='clobber')
parser.add_option('--no-clobber', action='store_false', dest='clobber')
if __name__ == '__main__':
    argv = '--clobber'.split()
    opts, args = parser.parse_args(argv) 
    print opts
    argv = '--no-clobber'.split()
    opts, args = parser.parse_args(argv) 
    print opts
