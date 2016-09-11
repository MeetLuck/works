import os, sys
import fnmatch

def _search(path,filename,founds,visited):
    print '=>',path
    if path in visited:
#       print 'already searched',path
        return
    if os.path.isdir(path):
        return
#       print 'not directory',path
    p = os.path.join(path,filename)
    if os.path.exists(p):
        founds.append('found at -> ' + path)
    else:
        print 'not found at ' + path
    visited.append(path)
#   print '=> end of _search'

def search(filename,paths,depth=3):
#   arg = filename, depth, founds, visited
    visited = []
    founds  = []
    for path in paths: 
        _search(path,filename,founds,visited)
        i=0
        for root, dirs, files in os.walk(path):
            for dir in normpaths(dirs):
                _search(os.path.join(path,dir),filename,founds,visited)
            i += 1
            if i > 6:
                break
    print ' '.join(visited)
    return founds

def normpaths(paths):
    # paths become local because assignments 
    paths = map(os.path.normcase, paths)
    paths = map(os.path.normpath, paths)
#   paths = [ os.path.normpath(p) for p in paths ]
    return paths

# search file in os.environment path
def main(filename):
    envpaths = os.environ['path'].split(os.pathsep)
    userpaths = ['c:\\', 'c:\\program files']
    envpaths = ['d:\j\home\works\win32']
#   userpaths = ['c:\python27\lib']
    envpaths = normpaths(envpaths)
    userpaths = normpaths(userpaths)
    
#   print envpaths
    searchpaths = list()
    searchpaths.extend(envpaths)
    searchpaths.extend(userpaths)

    # search file in search paths
    founds = search(filename,searchpaths)
    print '======================'
    print '\n'.join(founds)


if __name__ == '__main__':
#   filename = sys.argv[1]
#   main(filename)
    main('firefox.exe')
    main('python.exe')
