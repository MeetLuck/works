from subprocess import Popen, PIPE
def print_string(string):
    Popen('echo "%s" ' %string, shell=True)
import os
def whereis(program):
    for path in os.environ.get('PATH','').split(';'):
        print path
        if os.path.exists(os.path.join(path, program) ) and \
           not os.path.isdir(os.path.join(path, program)):
               return os.path.join(path, program)
    return None
#print_string('Hello World')
if whereis('python27') is not None:
    print location
