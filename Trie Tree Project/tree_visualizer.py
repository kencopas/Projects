from anytree import Node, RenderTree
import json

class Trie(object):

    def __init__(self):
        self.links = {}

    def insert_from(self, word_list):
        for word in word_list:
            self.insert(word)

    def insert(self, word):
        """
        :type word: str
        :rtype: None
        """
        word, current_dict = word.lower(), self.links
        for letter in word:
            if letter not in current_dict:
                current_dict[letter] = {}
            current_dict = current_dict[letter]
        current_dict["end"] = True

    def search(self, word):
        """
        :type word: str
        :rtype: bool
        """
        word, current_dict = word.lower(), self.links
        for letter in word:
            if letter not in current_dict:
                return False
            current_dict = current_dict[letter]
        return "end" in current_dict

    def startsWith(self, prefix):
        """
        :type prefix: str
        :rtype: bool
        """
        prefix, current_dict = prefix.lower(), self.links
        for letter in prefix:
            if letter not in current_dict:
                return False
            current_dict = current_dict[letter]
        return True
    
def plot(node, prev):
    for key, values in node.items():
        if key == "end": continue
        plot(values, Node(key, parent=prev))

def show():
    for pre, fill, node in RenderTree(root):
        print(f"{pre}{node.name}")

def write_json(input_dict):
    with open(r"\Users\kenneth.copas\Desktop\Trie Tree Project\tree_data.json", "w") as json_file:
        json.dump(input_dict, json_file, indent=4)
    
trie = Trie()
# word_list = [
#     "Lantern", "Drift", "Maple", "Quarry", "Whisper", "Orbit", "Velvet", "Crumble", "Brisk", "Alloy",
#     "Meadow", "Spiral", "Clarity", "Nimbus", "Ember", "Grove", "Dusk", "Prism", "Vault", "Thistle",
#     "Mirage", "Timber", "Echo", "Quartz", "Fable", "Snare", "Tundra", "Cascade", "Latch", "Flicker",
#     "Sable", "Ponder", "Glimmer", "Husk", "Riddle", "Plume", "Crag", "Kindle", "Nestle", "Wisp",
#     "Hinge", "Mirth", "Bramble", "Nomad", "Grotto", "Rumble", "Warden", "Bellow", "Shard", "Forge"
# ]

word_list = ["Cat", "Car"]


trie.insert_from(word_list)
root = Node("Trie")
# plot(trie.links, root)
# show()
write_json(trie.links)