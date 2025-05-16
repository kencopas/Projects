class WordDictionary:

    def __init__(self):
        # Initialize Trie Tree
        self.trie = {}

    def addWord(self, word: str) -> None:
        cur_node = self.trie
        # Iterate each character in the word
        for char in word:
            # Initialize nested dict if not exists
            if not cur_node.get(char):
                cur_node[char] = {}
            # Update current node
            cur_node = cur_node[char]

        # Place END flag in the current node
        cur_node["END"] = True

    def search(self, word: str) -> bool:
        # DFS
        def dfs(cur_node, word):

            # If the current node is not a dict, return False
            if type(cur_node) != dict:
                return False

            # Iterate each character in the word
            for index, char in enumerate(word):

                # For wildcards, perform dfs on every value in the current node passing the spliced word
                if char == ".":
                    # Iterate each possible character's node
                    for node in cur_node.values():
                        # Perform DFS on that node with the current word, ignoring the characters that have already been traversed
                        if dfs(node, word[index+1:]):
                            return True
                    return False

                # If the current node is not a dict, return False
                if type(cur_node.get(char)) != dict:
                    return False

                # Update current node
                cur_node = cur_node[char]

            # Return True if there is an END flag in the node
            return cur_node.get("END", False)
        
        # Perform dfs on the root of the trie tree
        return dfs(self.trie, word)

my = WordDictionary()
# ["WordDictionary","addWord","addWord","search","search","search","search","search","search"]
# [[],["a"],["a"],["."],["a"],["aa"],["a"],[".a"],["a."]]
my.addWord("a")
my.addWord("a")
for char in ['.', 'a', 'aa', 'a', '.a', 'a.']:
    print(my.search(char))