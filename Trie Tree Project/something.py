class PrefixTree:
    trie = {}

    def __init__(self):
        self.trie = {}

    def insert(self, word: str) -> None:
        cur_trie = self.trie
        for char in word:
            if not cur_trie.get(char):
                cur_trie[char] = {}
            cur_trie = cur_trie[char]

    def search(self, word: str) -> bool:
        cur_trie = self.trie
        for char in word:
            if not cur_trie.get(char):
                return False
            cur_trie = cur_trie[char]
        return cur_trie == {}

    def startsWith(self, prefix: str) -> bool:
        cur_trie = self.trie
        for char in prefix:
            if not cur_trie.get(char):
                return False
            cur_trie = cur_trie[char]
        return True
    
new_tree = PrefixTree()
new_tree.insert("Hello")
print(new_tree.trie)
print(new_tree.search("Hello"))