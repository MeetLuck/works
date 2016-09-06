import os
def whereis(program):
    for path in os.environ.get('PATH','').split(os.pathsep):
#       print path
        if os.path.exists(os.path.join(path,program)) and \
                not os.path.isdir(os.path.join(path,program)):
                    return os.path.join(path,program)
    print 'not found'
    return None

if __name__ == '__main__':
    print whereis('notepad.exe')
    print whereis('cmd.exe')
    print whereis('fx.lnk')
    print whereis('cone.lnk')
    print whereis('ls.exe')
