"""

Time Complexity: O(n) | Space Complexity: O(n)
Cycle Detection is a means of determining whether a Directed Graph contains a cycle or not. The below function uses recursive DFS to traverse a Directed Graph while
keeping track of the current path. Each path is passed as an argument to each recursive call, meaning the path for a given node only contains the node visited by each
recursive call on the call stack. If a node that is already in the path is visited, a cycle is present and the function returns True. 

"""

# Detects cycles in a Directed Graph using recursive DFS
def cyclic(graph: dict[any: list[any]]):

    visited = set()

    # Depth-First Search
    def dfs(key, path, cycle):
        
        # Return True if node is in the path or a cycle has been detected
        if key in path or cycle:
            return True

        # Check if the node has been visited
        if key in visited:
            return False
        
        visited.add(key)

        # Perform DFS on neighbors
        for next_key in graph[key]:
            # Return True if any neighbor node detects a cycle
            if dfs(next_key, path+[key], cycle):
                return True
            
        return False
            
    # Perform DFS on all nodes
    for key in graph.keys():
        # Return True if any DFS detects a cycle
        if dfs(key, [], False):
            return True
    
    return False