''' get sub-directories according to recursive depth 
    depth = 2 -> root, sub(1)
    detph = 3 -> root, sub(1), sub(2)
'''
import os

def getsubs(path):
    ' return (path,dirs) '
    subdirs = []
    for name in os.listdir(path):
        subdir = os.path.join(path,name)
        if os.path.isdir(subdir):
            subdirs.append(subdir)
    root,dirs = path,subdirs
    return root,dirs

def mywalk(path):
    result = []
    val = getsubs(path)
    result.append(val) 
    print result
    dirs = val[1]
    for root in dirs:
        if root: 
            print ' => recursive',root
            val = mywalk(root)
            result.extend(val)
    return result

root = 'd:\home\example'
os.chdir(root)
print os.path.abspath(os.curdir)
#li = mywalk(root)
li = mywalk(os.curdir)
print type(li)
print
print '-------------------------'
for x in li:
    print x
    print '+++'






