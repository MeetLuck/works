from implementation import *
def BFS1(graph,start):
    # print out what we find
    frontier = Queue()
    frontier.put(start)
    visited = {}
    visited[start] = True

    while not frontier.empty():
        current = frontier.get()
        print 'Visiting %r' % current
        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                frontier.put(neighbor)
                visited[neighbor] = True

def BFS2(graph,start):
    frontier = Queue()
    frontier.put(start)
    camefrom = {}
    camefrom[start] = None

    while not frontier.empty():
        current = frontier.get()
        for neighbor in graph.neighbors(current):
            if neighbor not in camefrom:
                frontier.put(neighbor)
                camefrom[neighbor] = current
    return camefrom


if __name__ == '__main__':
#   BFS1(example_graph,'A')
    g = SquareGrid(30,15)
    g.walls = DIAGRAM1_WALLS
    parents = BFS2(g,(8,7))
    draw_grid(g, width=2, point_to = parents, start=(8,8) )
