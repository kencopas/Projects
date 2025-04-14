class ListNode():

    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.next = None
        self.prev = None

class LRUCache():

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.capacity = capacity
        self.nodes = {}
        self.head = ListNode(0, 0)
        self.tail = ListNode(0, 0)

        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """

        self.print_list(f"Getting Node: key = {key}")
        
        if key not in self.nodes:
            return -1
        
        node = self.nodes[key]
        self.remove(node)
        self.add(node)

        self.print_list(f"Got node: ({node.key}, {node.val})")

        return node.val

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: None
        """

        self.print_list(f"Putting node: ({key}, {value})")
        node = ListNode(key, value)
        
        if key in self.nodes:
            print("Key found in node map")
            self.remove(self.nodes[key])
            

        self.nodes[key] = node
        self.add(node)

        if len(self.nodes) > self.capacity:
            print(f"Capacity exceeded\n")
            self.remove(self.head.next)

        self.print_list("Node Put:")
        
    def add(self, node):

        self.print_list(f"Adding node: ({node.key}, {node.val})")

        node.next = self.tail
        node.prev = self.tail.prev

        node.next.prev = node
        node.prev.next = node

        self.nodes[node.key] = node

        self.print_list("Node added:")

    def remove(self, node):

        self.print_list(f"Removing node: ({node.key}, {node.val})")

        node.next.prev = node.prev
        node.prev.next = node.next
        del self.nodes[node.key]

        self.print_list("Node removed:")

    def print_list(self, text):
        print(text)
        cur_node = self.head
        node_string2 = f"({cur_node.key}, {cur_node.val})"
        while cur_node.next:
            cur_node = cur_node.next
            node_string2 += f" <-> ({cur_node.key}, {cur_node.val})"
        print("\n    ", node_string2, "\n")


obj = LRUCache(2)
obj.put(2, 1)
obj.put(2, 2)
print(obj.get(2))
obj.put(1, 1)
obj.put(4, 1)
print(obj.get(2))