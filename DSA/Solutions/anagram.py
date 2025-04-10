def isAnagram(s: str, t: str) -> bool:
    comb = list(s) + list(t)
    char_byte = 0

    for char in comb:
        char_byte = char_byte ^ (1 << (ord(char)-65))

    return char_byte == 0