adj = {
       0: [(1,3)],
       1: [(3,7),(6,3)],
       2: [(4,8)],
       3: [(7,5)],
       4: [],
       5: [(1,7),(3,9),(6,4)],
       6: [(7,9)],
       7: [(6,3)]
       }

# Iterative graph dfs
def dfs(graph):
    
    visited = set()

    # Iterate each node in the graph
    for start_node, start_edge in graph.items():
        # If the node has been visited, skip the iteration
        if start_node in visited:
            continue
        visited.add(start_node)        # Add the starting node to visited
        print("\nNew Starting Node\n")
        stack = start_edge             # Initialize the stack with the starting edge
        
        # While the stack is not empty
        while stack:
            # print(f"Stack: {stack}")
            cur_node, weight = stack.pop() # Unpack the current node and weight
            
            # If the node has been visited, skip the iteration
            if cur_node in visited:
                continue
            
            visited.add(cur_node)         # Add the current node to visited
            print(f"Visited: {visited}")
            stack.extend(graph[cur_node]) # Append all edges to the stack

dfs(adj)