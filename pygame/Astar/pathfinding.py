# pathfinding part I(http://gabrielgambetta.com/path1.html) 
# reachable list
reachable = [ start_node ]
# explored list
explored = []
# at each step of the search,
# we choose one of the nodes we know how to reach but haven't explored yet,
# and see what new nodes we can reach from there
while reachable is not empty:
    # choose one of the nodes we know how to reach but haven't explored
    node = choose_node(reachable)
    if node == goal_node:
        path = []
        while node is not None:
            path.add(node)
            node = node.previous
        return path
    reachable.remove(node)
    explored.add(node)
    # figure out what nodes we can reach from here
    # start with the list of adjacent to this one
    # and remove the ones we've already explored
    new_reachable = get_adjacent_nodes(node) - explored
    for adjacent in new_reachable:
        if adjacent not in reachable:
            adjacent.previous = node # remember how we got there
            reachable.add(adjacent)
    return None

function find_path(start_node,goal_node):
    reachable = [ start_node ]
    explored = [ ]
    while reachable is not empty:
        # choose some node we know how to reach
        node = choose_node(reachable)
        # if we just go to the goal node, build and return the path
        if node == goal_node:
            return build_path(goal_node)
        # don't repeat
        reachable.remove(node)
        explored.add(node)
        # where can we get from here?
        new_reachable = get_adjacent_node(node) - explored
        for adjacent in new reachable:
            if adjacent not in reachable:
                adjacent.previous = node # remember how we got there
                reachable.add(adjacent)
    # if we get here, no path was found
    return None

function build_path(node):
    path = []
    while node != None:
        path.add(node)
        node = node.previous
    return path

# pathfinding part II: the heart of the matter

