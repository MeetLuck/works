import os, sys
import fnmatch,winsound

def doesExist(path,filename,founds,visited):
    if path in visited or not os.path.isdir(path):
        print 'already searched or not directory',path
        return
    p = os.path.join(path,filename)
    if os.path.exists(p):
        print 'found at -> ' + path
        winsound.Beep(440,300)
        founds.append('found at -> ' + path)
    else:
        print 'not found at ' + path
    visited.append(path)
    print '=> end of _search'

def search(filename,paths,depth=3):
    print 'start search'
    paths = normpaths(paths)
    paths.extend( getsubdirs(path
    print len(paths)
#   print '\n'.join(paths)
    visited = []
    founds  = []
    for path in paths:
        for root, dirs, files in os.walk(path):
            doesExist(root,filename,founds,visited)
            for dir in dirs:
                doesExist(os.path.join(root,dir),filename,founds,visited)
            break
#   print ' '.join(visited)
    print len(founds), len(visited)
    return founds

def normpaths(paths):
    # paths become local because assignments 
    paths = map(os.path.normcase, paths)
    paths = map(os.path.normpath, paths)
#   paths = [ os.path.normpath(p) for p in paths ]
    return paths

# search file in os.environment path
def main(filename):
    print 'start main'
    envpaths = os.environ['path'].split(os.pathsep)
    userpaths = ['c:\\', 'c:\\program files','d:\\']
#   envpaths = ['d:\\home\\works\\win32\\console']
#   userpaths = ['d:\\pds']
#   userpaths = ['c:\python27\lib']
    
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
#   main('python.exe')
