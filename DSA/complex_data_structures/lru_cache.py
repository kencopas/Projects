"""

This class reperesents an LRU Cache (Least Recently Used Cache). This complext data structure is implemented using a doubly linked list and a hash map. The head and tail of the
linked list are initialized for easy appending and removal. Nodes are appended at the end of the list, and moved to the end of the list everytime they are accessed. When the
cache capacity is reached, the node at the head of the list is removed, as it has been unused for the longest period of time. This creates efficient appending and removal, but
suffers from O(n) lookup, which is why the dictionary is implemented. The dictionary holds a reference to every node in the list via the node's key.

"""

# The node class for the LRU Cache is a doubly-linked key-value node
class ListNode():

    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.next = None
        self.prev = None

# Holds a specified number of nodes, removing the least recently used when needed
class LRUCache():

    def __init__(self, capacity):

        self.capacity = capacity
        self.nodes = {} # Dictionary of node keys and references !! Values are not node values, they are node references
        self.head = ListNode(0, 0)
        self.tail = ListNode(0, 0)

        # Doubly link the head and tail !! The positions of the head and tail nodes remain unchanged throughout, appended and popped nodes are tail.prev and head.next
        self.head.next = self.tail
        self.tail.prev = self.head

    # Used to retrieve the value of a node by key, updates the 'timestamp' of the node
    def get(self, key):

        self.print_list(f"Getting Node: key = {key}")
        
        # If node does not exist, return -1
        if key not in self.nodes:
            return -1
        
        node = self.nodes[key] # Retrieve the node reference
        
        # Remove and re-append the node to the list, moving it to the tail
        self.remove(node)
        self.add(node)

        self.print_list(f"Got node: ({node.key}, {node.val})")

        return node.val

    # Used to add a node or update a node value by key-value pair
    def put(self, key, value):

        self.print_list(f"Putting node: ({key}, {value})")
        
        node = ListNode(key, value) # Create the new node
        
        # Remove the node with the old value if it already exists
        if key in self.nodes:
            self.remove(self.nodes[key])
            
        self.add(node)         # Add the new node to the list and dictionary

        # If capacity is exceeded, remove the least frequently used node from the head
        if len(self.nodes) > self.capacity:
            self.remove(self.head.next)

        self.print_list("Node Put:")
        
    # Helper for put() and get() methods, adds a node by reassigning the surrounding nodes' pointers
    def add(self, node):

        print(f"Adding node: ({node.key}, {node.val})")

        # Insert the node between the last node and the tail
        node.next = self.tail
        node.prev = self.tail.prev

        # Reassign surrounding nodes' pointers
        node.next.prev = node
        node.prev.next = node

        self.nodes[node.key] = node # Create or update key-reference pair

        self.print_list("Node added")

    # Helper for put() and get() methods, removes a node by reassinging surrounding nodes' pointers
    def remove(self, node):

        print(f"Removing node: ({node.key}, {node.val})")

        # Reassign surrounding nodes' pointers
        node.next.prev = node.prev
        node.prev.next = node.next

        del self.nodes[node.key] # Delete key-reference pair

        self.print_list("Node removed:")

    # Visualizer | Prints a visualization of linked list in the format: (key, val) <-> (key, val) <-> ...
    def print_list(self, text):

        print(text)

        cur_node = self.head
        node_string2 = f"({cur_node.key}, {cur_node.val})"
        
        while cur_node.next:
            cur_node = cur_node.next
            node_string2 += f" <-> ({cur_node.key}, {cur_node.val})"
        
        print("\n    ", node_string2, "\n")

if __name__ == "__main__":

    # Test instructions
    my_cache = LRUCache(2)
    
    my_cache.put(2, 1)
    my_cache.put(2, 2)
    
    print(my_cache.get(2))
    
    my_cache.put(1, 1)
    my_cache.put(4, 1)
    
    print(my_cache.get(2))