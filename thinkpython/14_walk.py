''' 14.4 Filenames and paths'''
import os
#----------- current working directory--------
cwd = os.getcwd()
print cwd
#----------- os.path.abspath('14_walk.py')
abspath = os.path.abspath('14_walk.py')
print abspath
#----------- os.path.exists check whether a file or directory exists
print os.path.exists('14_walk.py')
#----------- os.path.isdir checks whether it's a directory --------
print os.path.isdir(cwd)
print os.path.isdir('14_walk.py')
#----------- os.path.isfile checks whether it is a file -----------
print os.path.isfile('14_walk.py')
#----------- os.listdir returns a list of the files ---------------
print os.listdir(cwd)

#----------- os.path.join(dirname, filename) ----------------
def walk(dirname):
    for name in os.listdir(dirname):
        path = os.path.join(dirname, name)
        if os.path.isfile(path):
            print path
        else:
            walk(path)
def walk2(dirname):
    ''' os.walk(top, topdown=True, onerror=None,followlinks=False)'''
    # Generate the file names in a directoroy tree by walking the tree
    # either top-down or bottom-up
    # For each directory in the tree rooted at a directory top(including top itself)
    # it yields a 3-tuple ( dirpath, dirnames, filenames)
    # dirpath is a string, the path to the directory
    # dirnames is a list, of names of the subdirectories in dirpath
    # filenames is a list, of names of the non-directory files in dirpath

    for root, dirs, files in os.walk(dirname):
        print 'root',root
        print 'dirs',dirs
        print 'files',files
#       for filename in files:
#           print os.path.join(root, filename)

#walk('D:\py\git\works')
walk2('D:\py\git\works')

