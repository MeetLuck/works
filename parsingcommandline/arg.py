# arg.py
import argparse
import sys

def check_arg(args=None):
    parser = argparse.ArgumentParser(description='script to learn basic argparse')
    parser.add_argument('-H','--host',
                         help='host IP address',
                         required='True',
                         default='localhost')
    parser.add_argument('-p','--port',
                        help='port of the web server',
                        default='8080')
    parser.add_argument('-u','--user',
                        help='user name',
                        default = 'root')
    result = parser.parse_args(args)
    return result.host, result.port, result.user

if __name__ == '__main__':
    h,p,u = check_arg(sys.argv[1:])
    print 'h =',h
    print 'p =',p
    print 'u =',u
