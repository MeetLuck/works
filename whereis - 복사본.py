import os, sys

def finddir(root):
    abspaths = list()
    for path in os.listdir(root):
        abspath = os.path.join(root,path)
        if os.path.isdir(abspath):
#           print abspath
            abspaths.append(abspath)
    return abspaths[:]

def findfile(filename,paths):
    for path in paths: 
#       print path
        p = os.path.join(path,filename)
        if os.path.exists(p):
            print 'found at -> '+ path

# search file in os.environment path
def main(filename):
    abspaths = os.environ['path'].split(os.pathsep)
    roots = ['c:\\program files','c:\\']
    for root in roots:
        abspaths.extend( finddir(root) )
    findfile(filename,abspaths)

if __name__ == '__main__':
    filename = sys.argv[1]
    main(filename)
