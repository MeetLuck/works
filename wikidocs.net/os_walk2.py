import os

os.chdir('D:\home')
path = os.path.abspath('example')

def print_dir(path):
    # os.walk treats dirs breadth-first, but files depth-first (go figure)
    expandtab = '  '
    for root, dirs, files in os.walk(path):
        # print the directories below the root
#       print root
        levels = root.count(os.sep)
        print expandtab*levels + os.path.basename(root) +'/'
        for file in files:
            print expandtab*(levels+1) + file


if __name__ == '__main__':
    print_dir('example')
