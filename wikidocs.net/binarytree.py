# A binary tree class.
class Tree:

    def __init__(self, label, left=None, right=None):
        self.label = label
        self.left = left
        self.right = right

    def __repr__(self, level=0, indent="    "):
        s = level*indent + `self.label`
        if self.left:
            s = s + "\n" + self.left.__repr__(level+1, indent)
        if self.right:
            s = s + "\n" + self.right.__repr__(level+1, indent)
        return s

    def __iter__(self):
        return inorder(self)

# Create a Tree from a list.
def tree(list):
    n = len(list)
    if n == 0:
        return []
    i = n / 2
    print n,i
    label = list[i]
    left  = tree(list[:i])
    right = tree(list[i+1:])
    print '->',label,left,right
    return Tree(label,left,right)
#   return Tree(list[i], tree(list[:i]), tree(list[i+1:]))

# A recursive generator that generates Tree labels in in-order.
def inorder(t):
    if t:
        for x in inorder(t.left):
            yield x
        yield t.label
        for x in inorder(t.right):
            yield x

# Show it off: create a tree.
t = tree("ABCDE")
print 'tree'
print t
print '-'*80
# Print the nodes of the tree in in-order.
#for x in t:
#    print x
#
#print
#for x in inorder(t):
#    print x
#print

# A non-recursive generator.
def inorder(node):
    stack = []
    while node:
        while node.left:
            stack.append(node)
            node = node.left
        yield node.label
        while not node.right:
            try:
                node = stack.pop()
            except IndexError:
                return
            yield node.label
        node = node.right

# Exercise the non-recursive generator.
#for x in t:
#    print x,
#print
