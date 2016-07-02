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

    ''' find all files in dirname and sub-directories'''

    filenames = list()
    for dirpath, sub_dirs, files in os.walk(dirname):
        print '<<---  %s  --->> ' %dirpath
        for file in files:
            path = os.path.join(dirpath, file)
            print path
            filenames.append(path)
#       for dir in sub_dirs:
#           print os.path.join(dirpath, dir)
    return filenames

if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
#   walk(script_dir)
#   print walk2(script_dir)
    walk2(script_dir)

