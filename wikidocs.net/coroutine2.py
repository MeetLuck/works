''' Generator Tricks for System Programers version 2.0
    from http://www.dabeaz.com/generators-uk/
'''
import os
cls = lambda : os.system('cls')

################## os.walk() ##############################
topdir = os.getcwd()
for path, dirlist,filelist in os.walk(topdir):
    print 'path: {path}'.format(path=path)
    print 'dirlist: {dirlist}'.format(dirlist=dirlist)
    print 'filelist: {filelist}'.format(filelist=filelist)
################## find ##############################
cls()
def gen_find(filepat,top):
    import fnmatch
    for path,dirlist,filelist in os.walk(top):
        for name in fnmatch.filter(filelist,filepat):
            yield os.path.join(path,name)

pyfiles = gen_find('*.py', '../')
for name in pyfiles: print name
