"""

This function tests the validity of a set of grouping symbols, making sure they are in order and have their respective pairs. This solution uses a stack that holds open grouping
symbols ('(', '[', '{'). While traversing the string of pairs, each open symbol is added to the stack. When a closing symbol is reached, the stack is checked to see if the top
element is the corresponding opening symbol. If it is, the stack is popped, and if it is not, the function returns false. This works because of this principle: For any given set
of grouping pairs traversed left to right, the closing symbol will always match the most recent unmatched opening symbol.

"""

# Tests if a set of parentheses are valid (each open symbol has a close symbol in order)
def valid_parentheses(string: str) -> bool:
    pairs = {')': '(', '}': '{', ']': '['} # Mapping of each open symbol to it's close symbol
    stack = []

    # Traverse each character
    for char in string:
        if pairs.get(char) is None: 
            stack.append(char)  # If it's an open symbol, stack it
        elif stack and stack[-1] == pairs[char]: 
            stack.pop()         # If it's a close symbol and the previous element was the corresponding close symbol, pop the stack
        else:   
            return False        # If it's a close symbol and the previous element did not match, return False
    
    # Return true if the stack is empty, otherwise return false
    if not stack:
        return True
    return False

if __name__ == "__main__":

    # Test cases
    test_strings = [
        "",
        "()",
        "()[]{}",
        "(]",
        "([)]",
        "{[]}",
        "(",
        ")",
        "((()))",
        "((())",
        "())",
        "{[()()]}",
        "{[()()]}]",
        "(((((((((())))))))))"
    ]

    # Run test cases
    for string in test_strings:
        # print(f"\n{string}")
        pad = ' '*((20-len(string)))
        print(f"{string}{pad} : {valid_parentheses(string)}")