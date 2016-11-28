class SimpleGraph:
    def __init__(self):
        self.edges = {}
    def neighbors(self,id):
        return self.edges[id]

graph = SimpleGraph()
graph.edges = {
    'A': ['B'],
    'B': ['A', 'C', 'D'],
    'C': ['A'],
    'D': ['E', 'A'],
    'E': ['B']
 }

import collections
class Queue:
    def __init__(self):
        self.elements = collections.deque()
    def empty(self):
        return len(self.elements) == 0
    def put(self,node):
        self.elements.append(node)
    def get(self):
        return self.elements.popleft()

if __name__ == '__main__':
    def BFS1(graph,start):
        # print out what we find
        frontier = Queue()
        frontier.put(start)
        visited = {}
        visited[start] = True
        while not frontier.empty():
            current = frontier.get()
            print 'Visiting %r' %current
            for next in graph.neighbors(current):
                if next not in visited:
                    frontier.put(next)
                    visited[next] = True
    BFS1(graph,'A')
