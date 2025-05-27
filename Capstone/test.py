from anytree import Node, RenderTree

root = Node("root")
child1 = Node("child1", parent=root)
child2 = Node("child2", parent=root)
subchild1 = Node("subchild1", parent=child1)

for pre, fill, node in RenderTree(root):
    print(f"{pre}{node.name}")