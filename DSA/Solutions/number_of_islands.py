"""

This solution works with a minesweeper-like elimination process. Every time an island is found, one or more 1s, the check() function is run on that island, which recursively
checks surrounding elements. All elements that are 1s are turned to 0s, preventing them from being found again. When the entire island is converted to 0s, the island_counter is
increased and the linear traversal continues.

"""

from time import sleep
# from utils.wrappers import timer
from random import random


# Prints the grid and number of islands found thus every 200ms for process visualization
def print_grid(grid: list[list[str]], speed: int, island_count: int=None):
    sleep(0.2/speed)
    print("----"*len(grid[0])+"-")
    for row in grid:
        my_str = "| "
        for element in row:
            my_str += f"{'\'' if element == 0 else '1'} | "
        print(my_str)
        print("----"*len(row)+"-")
    if island_count: print(f"Island Count: {island_count}")

# Recursive Approach
# @timer
def rnumber_of_islands(grid: list[list[str]], speed: int) -> int:

    width, height = len(grid[0]), len(grid)
    island_count = 0

    # Takes multiple coordinate tuples, converts all surrounding 1s to 0s recursively
    def check(*coords: tuple):

        for x, y in coords:
            # Check if coordinates are inbounds and the element is a 1
            if 0 <= y < height and 0 <= x < width and grid[y][x] == 1:
                # Set the element to 0 and check surrounding elements
                grid[y][x] = 0
                print_grid(grid, speed, island_count)
                check((x+1, y), (x, y+1), (x-1, y), (x, y-1))
    
    # Traverse the grid looking for 1s
    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            # For each 1, increase the island_counter and recursively check
            if value == 1:
                island_count += 1
                check((x, y))
                
    return island_count

# Iterative Approach -- check() function is replaced with a coordinate stack and a while loop
# @timer
def inumber_of_islands(grid: list[list[str]], speed: int) -> int:

    width, height = len(grid[0]), len(grid)
    island_count = 0
    stack = [] # Coordinate stack
    
    # Traverse the grid looking for 1s
    for i, row in enumerate(grid):
        for j, value in enumerate(row):

            # For each 1, increase the island_counter and append the coordinates to the stack
            if value == 1:
                island_count += 1
                stack.append((j, i))
            
            # check() function equivalent
            # Once the first coordinate is appended to the stack, check itself and iterate through it's surrounding elements
            while stack:
                x, y = stack.pop(0)

                # Check if coordinates are inbounds and the element is a 1
                if 0 <= y < height and 0 <= x < width and grid[y][x] == 1:

                    # Set the element to 0 and check surrounding elements
                    grid[y][x] = 0
                    print_grid(grid, speed, island_count) # Visualization
                    stack.extend([(x+1, y), (x, y+1), (x-1, y), (x, y-1)])
                
    return island_count

def gen_grid(size, density):
    return [[round(random()+(density-0.5)) for _ in range(size)] for _ in range(size)]

def test(approach: str, grid_size: int, density: int, speed: int):

    """
    Approach = 'R' (Recursive) or 'I' (Iterative)
    """

    test_grid = gen_grid(grid_size, density)
    
    if approach == "R":
        print("Test Grid:")
        print_grid(test_grid, speed)
        print(f"Number of Islands (Recursive): {rnumber_of_islands(test_grid, speed)}")
    elif approach == "I":
        print("Test Grid:")
        print_grid(test_grid, speed)
        print(f"Number of Islands (Iterative): {inumber_of_islands(test_grid, speed)}")
    else:
        print("Invalid approach type")

def test_all(approach: str='R', grid_size: int='20', n: int=1, density: int=0.5, speed: int=1):
    for _ in range(n):
        test(approach, grid_size, density, speed)

if __name__ == "__main__":

    # Params:
    #   Approach: str -> Iterative vs Recursive (Different pattern)
    #   Grid Size: int
    #   Iterations: int -> Number of iterations of randomly generate matricies
    #   Density: int -> 0-1 density of 1s on the matrix
    #   Speed: int -> 0.1-20 speed of visualization
    test_all('I', 20, 10, 1, 5)

    # !!! Run in 'OUTPUT' tab with ctrl-shift-n and click the lock in the top right corner to lock the output scroll, not terminal. Terminal violently shakes the visualization 