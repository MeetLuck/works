from priorityqueueset import PriorityQueueSet


class PathFinder(object):
    def __init__(self, successors, move_cost, heuristic_to_goal):
        self.successors = successors
        self.move_cost = move_cost
        self.heuristic_to_goal = heuristic_to_goal
    
    def compute_path(self, start, goal):
        # Implementation of the A* algorithm.
        closed_set = {}
        
        start_node = self._Node(start)
        start_node.g_cost = 0
        start_node.f_cost = self._compute_f_cost(start_node, goal)
        
        open_set = PriorityQueueSet()
        open_set.add(start_node)
        
        while len(open_set) > 0:
            # Remove and get the node with the lowest f_score from  the open set            
            curr_node = open_set.pop_smallest()
            
            if curr_node.coord == goal:
                return self._reconstruct_path(curr_node)
            
            closed_set[curr_node] = curr_node
            
            for succ_coord in self.successors(curr_node.coord):
                succ_node = self._Node(succ_coord)
                succ_node.g_cost = self._compute_g_cost(curr_node, succ_node)
                succ_node.f_cost = self._compute_f_cost(succ_node, goal)
                
                if succ_node in closed_set:
                    continue
                   
                if open_set.add(succ_node):
                    succ_node.pred = curr_node
        
        return []

    ########################## PRIVATE ##########################
    
    def _compute_g_cost(self, from_node, to_node):
        return (from_node.g_cost + 
            self.move_cost(from_node.coord, to_node.coord))

    def _compute_f_cost(self, node, goal):
        return node.g_cost + self._cost_to_goal(node, goal)

    def _cost_to_goal(self, node, goal):
        return self.heuristic_to_goal(node.coord, goal)

    def _reconstruct_path(self, node):
        """ Reconstructs the path to the node from the start node
            (for which .pred is None)
        """
        path = [node.coord]
        n = node
        while n.pred:
            n = n.pred
            path.append(n.coord)
        
        return reversed(path)

    class _Node(object):
        def __init__(self, coord, g_cost=None, f_cost=None, pred=None):
            self.coord = coord
            self.g_cost = g_cost
            self.f_cost = f_cost
            self.pred = pred
        
        def __eq__(self, other):
            return self.coord == other.coord
        
        def __cmp__(self, other):
            return cmp(self.f_cost, other.f_cost)
        
        def __hash__(self):
            return hash(self.coord)

        def __str__(self):
            return 'N(%s) -> g: %s, f: %s' % (self.coord, self.g_cost, self.f_cost)

        def __repr__(self):
            return self.__str__()

