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
    print(valid_parentheses(string))