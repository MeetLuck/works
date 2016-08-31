import os

os.chdir('D:\home')
path = 'example'

def print_os_walk1(path,topdown):
    for root, dirs, files in os.walk(path,topdown):
        print root
        for dir in dirs:
            print '  {}\\'.format(dir)
        for file in files:
            print '  {}'.format(file)

def count_path(path):
#   print 'counting path...'
#   print '-> path: '+ path
    dirname = os.path.dirname(path)
    depth = 0
#   print '=> dir: '+ dirname
    while dirname:
        depth += 1
        dirname = os.path.dirname(dirname)
#       print '==> dir: '+ dirname
#   print '===> dir: '+ dirname
#   print count
#   print 
    return depth

def print_os_walk2(path):
    exptab = '    '
    for root, dirs, files in os.walk(path): #,topdown=False):
        depth = count_path(root)
        basename = os.path.basename(root)
        print '{tab}{base}/'.format(tab = exptab*depth, base = basename)
        for file in files:
            print '{tab}{file}'.format(tab = exptab*(depth+1), file = file)

def walkdir(dirname):
    for cur, _dirs, files in os.walk(dirname):
        pref = ''
        head, tail = os.path.split(cur)
        print head,':',tail
        while head:
            pref += '---'
            head, _tail = os.path.split(head)
            print head,'::',tail
        print(pref+tail)
        for f in files:
            print(pref+'---'+f)
        print '-'*70, '\n' 


def recursive_walk(folder):
    for folderName, subfolders, filenames in os.walk(folder):
        if subfolders:
            for subfolder in subfolders:
                recursive_walk(subfolder)
        print('\nFolder: ' + folderName + '\n')
        for filename in filenames:
            print(filename + '\n')

if __name__ == '__main__':
#   print_os_walk1(path,topdown=True)
    print_os_walk2(path)
    recursive_walk(path)
#   walkdir(path)
