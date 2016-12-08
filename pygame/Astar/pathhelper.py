#==============================================================================
#   Generic helpers
#==============================================================================

# return the index of a node in the list
def getNodeIndex(node,lst):
    try:
        return lst.index(node)
    except ValueError:
        print 'no such node'
        return -1
def test_getNodeIndex():
    lst = [0,1,'a',3,'b']
    print getNodeIndex('a',lst)
    print getNodeIndex('c',lst)

def findNode(node,lst):
    return getNodeIndex(node,lst) >= 0



if __name__ == '__main__':
    test_getNodeIndex()
