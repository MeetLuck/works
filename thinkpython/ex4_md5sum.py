''' Exercise 4 '''
# 1. Write a program that searches a directory and all of its subdirectories,
#    recursively, and returns a list of complete paths for all files with a given suffix(like mp3)
# 2. To recognize duplicates, you can use md5sum to compute a 'checksum' for each files.
#    If two files have the same checksum, they probably have the same contents.
# 3. To duble-check, you can use the Unix command diff

import os

def walk(dirname):
    ''' Finds the names of all files in dirname and its sub-directories. '''
    names = list()
    for name in os.listdir(dirname):
        path = os.path.join(dirname, name)
        if os.path.isfile(path):
            names.append(path)
        else:
            names.extend( walk(path) )
    return names

def pipe(cmd):
    ''' Runs a command in a subprocess
        Returns (res,stat), the output of the subprocess and the exit status
        '''
    fp = os.popen(cmd)
    res = fp.read()
    stat = fp.close()
    assert stat is None
    return res, stat

def compute_checksum(filename):
    ''' Computes the MD5 checksum of the contents of a file '''
    cmd = 'md5sum ' + filename
    return pipe(cmd)

def check_diff(name1,name2):
    ''' Computes the difference between the contents of two files
    name1, name2 : string of filenames
    '''
    cmd = 'diff %s %s' %(name1,name2)
    return pipe(cmd)



def compute_checksums(dirname, suffix):
    ''' Computes checksums for all files with the given suffix
        dirname: string name of directory to search
        suffix: string suffix to match
        Returns map from checksum to list of files with that checksum
        '''
    names = walk(dirname)
    d = dict()
    for name in names:
        if name.endswith(suffix):
            res, stat = compute_checksum(name)
            checksum, _ = res.split()
            if checksum in d:
                d[checksum].append(name)
            else:
                d[checksum] = [name]
    return d

def check_pairs(names):
    ''' Checks whether any in a list of files differs from others
        names: [ list of string filenames ]
        '''

    for name1 in names:
        for name2 in names:
            if name1 < name2:
                res, stat = check_diff(name1,name2)
                if res:
                    return False
    return True

def print_duplicates(d):
    ''' checks for duplicate files
    Reports any files with the same checksum and checks whether they are, in fact, identical
    d: map from checksum to list of files with that checksum
    '''
    for key, names in d.iteritems():
        print key, names
        if len(names) > 1:
            print 'The following files have the same checksum:'
            for name in names:
                print name
            if check_pairs(names):
                print 'And they are identical'

if __name__ == '__main__':
#   dirname = os.path.abspath(__file__)
    dirname = os.path.dirname(__file__)
    print dirname
    d = compute_checksums(dirname=dirname, suffix='.py')
    print_duplicates(d)

