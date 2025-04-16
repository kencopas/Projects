"""

Each function generates every possible permutation of n pairs of valid parentheses. The recursive and iterative implementation are nearly identical. The process is as follows:
The variables are l (number of left parentheses thus far), r (number of right parentheses thus far), and perm (the current permuatation). The generation process follows a dfs-like
traversal style, checking conditionals before recursively calling or appending the next permutations.

 * Interesting Note: On first implementation of the iterative approach, I used a queue instead of a stack. This resulted in a nearly 100x decrease in performance, and I can only
 speculate that the reason for this is because of the nature of the .pop() function on lists in python. Popping an element from the end of a list is O(1) runtime, while popping
 an element from the front is O(n), as this requires shifting every other element in the list one to the right.

"""

from utils.wrappers import timer

# Recursive solution
@timer
def rgen(n):
    list = []
    
    # Recursively passes the counts of left and right parentheses and the string of the current permutation
    def next_paren(l, r, perm):
        
        if l < n: # Check if left parentheses count is under the max
            next_paren(l+1, r, perm+"(") 
        if r < n and r < l: # Check if the right parentheses count is under the max and there is at least one more left parenthesis
            next_paren(l, r+1, perm+")")
        if r == n == l: # Check if the max left and right parentheses coutn has been met
            list.append(perm)

    next_paren(1, 0, "(")

    return list

# Iterative solution with stack
@timer
def igen(n):
    list = []
    stack = [(0, 0, "")]

    # Iterates through each tuple in the queue | (l, r, cur_permutation)
    while stack:

        l, r, perm = stack.pop()
        
        if l < n: # Check if left parentheses count is under the max
            stack.append((l+1, r, perm+"("))   
        if r < n and r < l: # Check if the right parentheses count is under the max and there is at least one more left parenthesis
            stack.append((l, r+1, perm+")"))
        if r == n == l: # Check if the max left and right parentheses coutn has been met
            list.append(perm)

    return list