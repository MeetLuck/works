import Queue

class PriorityQueue:
    def __init__(self):
        self.pq = Queue.PriorityQueue(maxsize=0)
    def empty(self):
        return self.pq.empty()
    def put(self,node):
        self.pq.put( [node.cost,node] )
#       priority = node.cost
#       item = priority,node
#       self.pq.put(item)
    def get(self):
        return self.pq.get()

if __name__ == '__main__':
    class Node:
        def __init__(self,coord):
            self.cost = None
            self.coord = coord
    c1 = (0,0)
    c2 = (1,1)
    c3 = (1,2)
    n1 = Node(c1)
    n2 = Node(c2)
    n3 = Node(c3)
    n1.cost = 1.2
    n2.cost = 1.1
    n3.cost = 1.2
    print n1,n2
    pq = PriorityQueue()
    pq.put(n1)
    pq.put(n2)
    pq.put(n3)
    while not pq.empty():
        print pq.get()
