def isValid(s: str) -> bool:
        close = {')': '(', '}': '{', ']': '['}
        stack = []
        for char in s:
            if close.get(char) is None:
                stack.append(char)
            elif stack and stack[-1] == close[char]:
                stack.pop()
        if not stack:
            return True
        return False

print(isValid("]"))