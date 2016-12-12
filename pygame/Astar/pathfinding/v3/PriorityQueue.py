import Queue

class PriorityQueue:
    def __init__(self):
        self.pq = Queue.PriorityQueue(maxsize=0)
    def empty(self):
        return self.pq.empty()
    def put(self,node):
        priority, item = node.F, node
        self.pq.put( [priority, item] )
    def get(self):
        return self.pq.get()[-1] # item = node
    def __contains__(self,node):
        priority, item = node.F, node
        return [priority,item] in self.pq.queue

if __name__ == '__main__':
    class Node:
        def __init__(self,coord):
            self.F = None
            self.coord = coord
    c1 = (0,0)
    c2 = (1,1)
    c3 = (1,2)
    c4 = (2,3)
    c5 = (5,3)
    n1 = Node(c1)
    n2 = Node(c2)
    n3 = Node(c3)
    n4 = Node(c4)
    n5 = Node(c5)
    n1.F = 1.2
    n2.F = 1.1
    n3.F = 1.2
    n4.F = 1.3
    n5.F = 1.0
#   print n1,n2
    pq = PriorityQueue()
    pq.put(n4)
    pq.put(n3)
    pq.put(n1)
    pq.put(n2)
#   print pq.get()
#   print pq.pq.queue
#   print n1 in pq
    i = 0
    while not pq.empty():
        print pq.get().F
        if i==0:
            pq.put(n5)
        i += 1
