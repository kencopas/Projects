from anytree import Node, RenderTree
import os
import glob


def project_tree(root_dir: str, *, ignore: set[str]) -> None:
    """
    Generates a project file-structure tree using anytree

    Useage:

        project_tree(
            <Directory to Project Folder>,
            ignore=<Set of Folder/File Names you want excluded>
        )

    """

    # Get the project name and print it
    project_name = os.path.basename(root_dir).title()
    print(project_name)
    print()

    # Initialize a queue
    queue = []

    dirs = glob.glob(rf"{root_dir}\*")

    ignores = [
        dir for dir in dirs
        for name in ignore
        if name in dir
    ]
    for dir in dirs:
        if dir in ignores:
            continue
        filename = os.path.basename(dir)
        cur_node = Node(
            filename
        )
        new_filepath = root_dir+"/"+filename
        queue.append((new_filepath, cur_node))

    root_nodes = [thing[1] for thing in queue]

    while queue:
        filepath, root = queue.pop()
        dirs = glob.glob(rf"{filepath}\*")
        ignores = []
        for name in ignore:
            ignores.extend([dir for dir in dirs if name in dir])
        for dir in dirs:
            if dir in ignores:
                continue
            filename = os.path.basename(dir)
            cur_node = Node(
                filename,
                parent=root
            )
            new_filepath = filepath+"/"+filename
            queue.append((new_filepath, cur_node))

    print()
    for root in root_nodes:
        for pre, fill, node in RenderTree(root):
            print(f"{pre}{node.name}")


# Example Useage:

project_tree(
    r"C:\Users\kenneth.copas\OneDrive - PeopleShores PBC\Desktop\Projects\Capstone",
    ignore={
        "pycache",
        "debug",
        "project_tree.py",
        "file_structure.txt",
        "screenshots",
        "csv",
        ".png",
        "dev"
    }
)
