''' get sub-directories according to recursive depth 
    depth = 2 -> root, sub(1)
    detph = 3 -> root, sub(1), sub(2)
'''
import os
import fnmatch,winsound

def getsubs(path):
    ' return tuple(root,dirs) '
    subdirs = []
    if 'System Volume' in path:
        return 
    for name in os.listdir(path):
        subdir = os.path.join(path,name)
        if os.path.isdir(subdir):
            subdirs.append(subdir)
    root,dirs = path,subdirs
    return root,dirs

def mywalk(path,depth):
    '''
    root +- A - a1
         |    - a2
         +- B - b1 - b2
    root> 
     [A,B]
    root/A>  
     [a1,a2] 
    root/A/a1> 
     []
    '''
    result = []
    val = getsubs(path)
    result.append(val) 
    if val:
        subdirs = val[1]
    else:
        subdirs = []

    # check sub-directory's depth
    subdepth = path.count(os.sep)
#   print ' -> depth,subdepth = ',depth,subdepth
    if subdepth > depth:
#       print ' ... passing',path
        return []

    # loop subdirs
    for sub in subdirs: # subdirs = [] -> PASS for loop
#       print ' => recursive call \tsub = ',sub
        val = mywalk(sub,depth)
        result.extend(val)
    return result


def doesExist(path,filename,founds,visited):
#   print '... path = ',repr(path)
    if path in visited or not os.path.isdir(path):
#       print 'already searched or not a directory',path
        return
    p = os.path.join(path,filename)
    if os.path.exists(p):
        print 'found at -> ' + path
        winsound.Beep(440,300)
        founds.append('found at -> ' + path)
    else:
        pass
#       print 'not found at ' + path
    visited.append(path)
#   print '=> end of search at ',path

def search(filename,paths,depth):
    print 'start search'
    paths = normpaths(paths)
    print len(paths)
#   print '\n'.join(paths)
    visited = []
    founds  = []
    for path in paths:
        idepth = depth + path.count(os.sep)
        subdirs = mywalk(path,idepth)
#       print 
#       print '%s \t subdirs = %s' %(path,len(subdirs))
        for dir in subdirs:
            if dir:
                doesExist(dir[0],filename,founds,visited)
#   print ' '.join(visited)
    print len(founds), len(visited)
    return founds

def normpaths(paths):
    # paths become local because assignments 
    paths = map(os.path.normcase, paths)
    paths = map(os.path.normpath, paths)
    return paths

def main(filename,depth=0):
    print 'start main'
    envpaths = os.environ['path'].split(os.pathsep)
    userpaths = ['c:\\', 'c:\\program files']
    
#   print envpaths
    searchpaths = list()
    searchpaths.extend(envpaths)
    searchpaths.extend(userpaths)

    # search file in search paths
    founds = search(filename,searchpaths,depth)
    print '======================'
    print '\n'.join(founds)
if __name__ == '__main__':
#   main('firefox.exe')#,1)
    main('firefox.exe',1)
