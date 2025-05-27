from anytree import Node, RenderTree
import os
import glob


def project_tree(root_dir: str, *, ignore: list[str]) -> None:
    """
    Generates a project filestructure tree using anytree
    """

    project_name = os.path.basename(root_dir).title()
    project = Node(project_name)
    queue = [(root_dir, project)]

    while queue:
        filepath, root = queue.pop()
        if "pycache" in filepath:
            continue
        print(f"Filepath: {filepath}, Root: {root}")
        dirs = glob.glob(rf"{filepath}\*")
        ignores = []
        for name in ignore:
            ignores.extend([dir for dir in dirs if name in dir])
        for dir in dirs:
            if dir in ignores:
                continue
            filename = os.path.basename(dir)
            print(f"Basename: {filename}")
            cur_node = Node(
                filename,
                parent=root
            )
            new_filepath = filepath+"/"+filename
            queue.append((new_filepath, cur_node))

    print()
    for pre, fill, node in RenderTree(project):
        print(f"{pre}{node.name}")


project_tree(
    r"C:\Users\kenneth.copas\OneDrive - PeopleShores PBC"
    r"\Desktop\Projects\Capstone",
    ignore={
        "pycache",
        "debug",
        "project_tree.py",
        "file_structure.txt"
    }
)
