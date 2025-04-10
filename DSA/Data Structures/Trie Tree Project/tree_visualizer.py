"""

The Trie Tree is a tree data structure that stores words for incredibly fast lookup speed. In a Trie, each node is a character. The first layer holds the first characters of all
words in the tree. Each path from the top layer to the bottom is a full word (Ex: Trie.insert("Hello") | "H" -> "e" -> "l" -> "l" -> "o"). Each node character contains pointers
to every possible next node character (Ex: "Hello" and "Hector", "H" -> "e" <- This node points to both "l" and "c"). This implementation uses a nested dictionary to achieve this.
Time Complexity for searching is O(n), where n is the number of characters in the word. Time Complexity for creation is O(w*n), where w is the number of words.

This guy made a good visualizer for json trees:
https://github.com/akhiljay/JSON-tree-visualizer

"""

import json

# Trie Tree class
class Trie():

    # Initializes the root dictionary
    def __init__(self):
        self.links = {}

    # Inserts each word from a list of words
    def insert_from(self, word_list: list):
        for word in word_list:
            self.insert(word)

    # Inserts a word character by character
    def insert(self, word: str):
        word = word.lower()         # Case insensitive
        current_dict = self.links   # Initializes the current dictionary as root dictionary
        
        # Traverses each character in the word
        for letter in word:
            # Add a the current letter as a key of the previous letter if it did not exist
            if letter not in current_dict:
                current_dict[letter] = {}

            current_dict = current_dict[letter]     # Update the current dictionary

        print(f"Successfully added {word}")
        current_dict["end"] = True      # Add an "end" key to signify the end of the word

    # Searches for a word or prefix and returns true if it exists in the Trie
    def search(self, word: str, *, prefix=False) -> bool:

        search_type = "prefix" if prefix else "word"
        print(f"\nSearching for {search_type}: {word}")

        word = word.lower()         # Case insensitive
        current_dict = self.links   # Initializes the current dictionary as root dictionary
        
        # Traverse each character in the word
        for letter in word:
            # Return false if any character does not exist as a key in the current dictionary
            if letter not in current_dict:
                print(f"{search_type} does not exist")
                return False
            
            current_dict = current_dict[letter]     # Update the current dictionary

        # Return true if the "end" key exists or if searching for a prefix
        if current_dict.get("end", prefix):
            print(f"{search_type} '{word}' found!")
            return True
        else:
            print(f"{search_type} '{word}' not found")
            return False

    # Writes data to tree_data.json for storage and visualization
    def write(self):
        with open("tree_data.json", "w") as json_file:
            json.dump(self.links, json_file, indent=4)
    
if __name__ == "__main__":
    
    # Example random word list
    word_list = [
        "Lantern", "Drift", "Maple", "Quarry", "Whisper", "Orbit", "Velvet", "Crumble", "Brisk", "Alloy",
        "Meadow", "Spiral", "Clarity", "Nimbus", "Ember", "Grove", "Dusk", "Prism", "Vault", "Thistle",
        "Mirage", "Timber", "Echo", "Quartz", "Fable", "Snare", "Tundra", "Cascade", "Latch", "Flicker",
        "Sable", "Ponder", "Glimmer", "Husk", "Riddle", "Plume", "Crag", "Kindle", "Nestle", "Wisp",
        "Hinge", "Mirth", "Bramble", "Nomad", "Grotto", "Rumble", "Warden", "Bellow", "Shard", "Forge"
    ]

    trie = Trie()
    trie.insert_from(word_list)
    trie.insert("Landlord")
    trie.search("Sable")
    trie.search("Gro")
    trie.search("Gro", prefix=True)
    trie.write()