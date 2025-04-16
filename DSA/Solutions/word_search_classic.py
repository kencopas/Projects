# Simpler implementation that can be optimized be converting to an iterative approach
def word_search(board: list[list[str]], word: str):
        
    # Convert the board into a set for efficient lookup
    all_chars = {item for sublist in board for item in sublist}
    
    # Return false if any characters in the word are not present in the board
    for char in word:
        if char not in all_chars:
            return False

    # Recursively check the next node
    def backtrack(coords, dir, chars, path):

        y, x = coords

        # Return true if the word is empty (all characters have been found)
        if not chars:
            return path
        
        # Return false if the coordinates are out of bounds, already path, or the character does not match the next character in the word
        inbounds = (0 <= y < len(board) and 0 <= x < len(board[0]))
        if (not inbounds) or (board[y][x] != chars[0]):
            return None

        yd, xd = dir
        return backtrack((y+yd, x+xd), dir, chars[1:], path+[coords])
    
    # Return the valid path found from all 8 possible directions, otherwise return False
    def first_search(y, x, word):
        return (backtrack((y, x+1), (0, 1), word[1:], [(y, x)]) or backtrack((y-1, x), (-1, 0), word[1:], [(y, x)]) 
             or backtrack((y, x-1), (0, -1), word[1:], [(y, x)]) or backtrack((y+1, x), (1, 0), word[1:], [(y, x)])
             or backtrack((y+1, x+1), (1, 1), word[1:], [(y, x)]) or backtrack((y-1, x-1), (-1, -1), word[1:], [(y, x)]) 
             or backtrack((y+1, x-1), (1, -1), word[1:], [(y, x)]) or backtrack((y-1, x+1), (-1, 1), word[1:], [(y, x)]))
    
    # Traverse the board and perform a word search on the nodes whose character matches the first character of the word
    for y, row in enumerate(board):
        for x, char in enumerate(row):
            
            if char == word[0]:

                search = first_search(y, x, word)
                if search:
                    return search

    # Return false if no path is found
    return False

# Perform word search and print a board showing the path found
def visualize_search(board: list[list[str]], word: str, dimensions: tuple[int]):

    length, height = dimensions

    print(f"\nSearching for: {word}\n")

    solution_board = [[0 for _ in range(length)] for _ in range(height)]    # Initialize the solution board of equal dimensions to search board
    coord_list = word_search(board, word)   # Retrieve the coordinates for the solution

    # Set the elements at each coordinate to 1
    for coord in coord_list:
        y, x = coord
        solution_board[y][x] = 1

    # Print the solution board
    for row in solution_board:
        print(row)

# Perform visualize_search on each word in a list
def visualize_all(board: list[list[str]], words: list[str]):

    dimensions = (len(board[0]), len(board))
    for word in words:
        visualize_search(board, word, dimensions)