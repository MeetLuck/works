import os, sys
import fnmatch,winsound
''' path +- sub1a +- sub2a +- sub3a
         |        +- sub2b
         |        +- sub2c
         |
         +- sub1b +- sub2d
         |        +- sub2e 
         |
         +- sub1c
         |
'''     

def pathwalk(path):
    ' return dirs '
    subdirs = []
    for name in os.listdir(path):
        if os.path.isdir(name):
            subdir = os.path.join(path,name)
            subdirs.append(subdir)
    return subdirs

def countpath(path):
    if os.path.isabs(path):
        path = os.path.basename(path)
    dirname = os.path.dirname(path)
    depth = 0
    while dirname:
        depth += 1
        dirname = os.path.dirname(dirname)
    return depth

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

def addSub(paths):
    subpaths = []
    for path in paths:
        for root, dirs,files in os.walk(path):
            for dir in dirs:
                subpaths.append( os.path.join(root,dir) )
            break
    return normpaths(subpaths)

def search(filename,paths,depth=3):
    print 'start search'
    paths = normpaths(paths)
    paths.extend( addSub(paths) )
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
    main('refreshenv')
#   main('python.exe')
