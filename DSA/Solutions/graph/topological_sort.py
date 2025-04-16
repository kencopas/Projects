"""

Topological Sort is a sorting algorithm that sorts a Directed Acyclic Graph such that each node could be reached from left to right with it's necessary dependencies
already reached. This algorithm works by picking a random node and performing DFS. Once a leaf node is reached or all of a node's neighbors have been visited, the node
is appended to a list. This process repeats until all nodes have been visited. Once all nodes have been visited, the list is returned in reverse order.

"""

from cycle_detection import cyclic

# Topological Sort, sorts a Directed Ayclic Graph of dependencies
def top_sort(graph: dict[any: list[any]]) -> list:

    # Check for cycles
    if cyclic(graph):
        print("Graph is cyclic and cannot be topologically sorted")
        return

    visited = set()
    output = []

    # Depth-First Search
    def dfs(key):

        # Check if the node has been visited
        if key in visited:
            return
        
        visited.add(key) # Add node to visited

        # Perform DFS on neighbors
        for next_key in graph[key]:
            dfs(next_key)
        
        output.append(key) # Once DFS has exhausted all neighbors, append the node to the list

    # Perform DFS on all nodes
    for key in graph.keys():
        dfs(key)
    
    return output[::-1] # Return reversed list

if __name__ == "__main__":

    adj = {
        'A': ['D'],
        'B': ['D'],
        'C': ['A', 'B'],
        'D': ['H', 'G'],
        'E': ['F', 'D', 'A'],
        'F': ['K', 'J'],
        'G': ['I'],
        'H': ['J', 'I'],
        'I': ['L'],
        'J': ['M', 'L'],
        'K': ['J'],
        'L': [],
        'M': []
        }

    print(top_sort(adj))