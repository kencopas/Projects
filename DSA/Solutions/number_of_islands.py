"""

This solution works with a minesweeper-like elimination process.

"""

from time import sleep

def printGrid(grid, count):
    sleep(0.2)
    print("----"*len(grid[0])+"-")
    for row in grid:
        my_str = "| "
        for element in row:
            my_str += f"{element} | "
        print(my_str)
        print("----"*len(row)+"-")
    print(f"Islands: {count}")

def numIslands(grid):
    """
    :type grid: List[List[str]]
    :rtype: int
    """
    count = 0

    # Takes multiple coordinate tuples, converts all surrounding 1s to 0s recursively.
    def check(*coords: tuple):
        for x, y in coords:
            # Check if coordinates are inbounds and the element is a "1"
            if 0 <= y < len(grid) and 0 <= x < len(grid[0]) and grid[y][x] == "1":
                # Set the element to 0 and check surrounding elements
                grid[y][x] = "0"
                printGrid(grid, count)
                check((x+1, y), (x, y+1), (x-1, y), (x, y-1))
    
    # Traverse the grid looking for 1s
    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            # For each 1, increase the counter and recursively check
            if value == "1":
                count += 1
                check((x, y))
                
    return count