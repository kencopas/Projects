"""

This solution uses recursive backtracking to find a word within a word search board. Once a character is found in the board that matches the first character of the word, a call to
backtrack() is made passing the starting coordinates of that character, the word, and an empty path set. Each recursive call checks if the current coordinates are in bounds, 
haven't been path, and the character matches the first character from the passed string. If these conditions are met, a recursive call is made to the surrounding nodes. This call
passes updated coordinates, the current string with the check character removed, and the updated path set.

"""

def word_search(board, word):
    
    # Convert the board into a set for efficient lookup
    all_chars = {item for sublist in board for item in sublist}
    visited = set()
    
    # Return false if any characters in the word are not present in the board
    for char in word:
        if char not in all_chars:
            return False

    # Recursively check surrounding nodes
    def backtrack(y, x, chars, visited):

        # Return true if the word is empty (all characters have been found)
        if not chars:
            return True
        
        # Return false if the coordinates are out of bounds, already visited, or the character does not match the next character in the word
        inbounds = (0 <= y < len(board) and 0 <= x < len(board[0]))
        if (not inbounds) or ((x, y) in visited) or (board[y][x] != chars[0]):
            return False

        # Return true if any recursive calls to the four surrounding nodes return true
        return (backtrack(y, x+1, chars[1:], visited | {(x, y)}) or backtrack(y-1, x, chars[1:], visited | {(x, y)}) 
             or backtrack(y, x-1, chars[1:], visited | {(x, y)}) or backtrack(y+1, x, chars[1:], visited | {(x, y)}))

    # Traverse the board and perform a word search on the nodes whose character matches the first character of the word
    for y, row in enumerate(board):
        for x, char in enumerate(row):
            
            if char == word[0]:
                search = backtrack(y, x, word, visited)
                if search:
                    return True

    # Return false if no path is found
    return False