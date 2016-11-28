def findPath(start,goal):
    reachable = [start]
    explored = []
    while reachable: # is not empty:
        # choose some node we know how to reach
        node = chooseNode(reachable)
        # if we just got to the goal node, build and return the path
        if node == goal:
            return buildPath(node)
        # do not repeat
        reachable.remove(node)
        explored.add(node)
        # where can we get from here?
        new_reachable = getAdjacents(node)
        for adjacent in new_reachable:
            if adjacent not in reachable:
                adjacent.previous = node
                reachable.add(adjacent)
    # if we get here, no path was found
    return None


def buildPath(node):
    path = list()
    while node != None:
        path.add(node)
        node = node.previous
    return path
