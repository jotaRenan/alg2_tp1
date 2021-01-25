class Trie:
    class Node:
        def __init__(self):
            self.children = {}
            self.endOfWord = False
            self.code = -1
            self.text = ""

    def __init__(self):
        self.root = self.Node()
        self.next_code = 0

    def insertWord(self, word):
        self._insertWord(word, self.root)

    def _insertWord(self, word, current):
        if word == "":
            return

        if len(current.children) == 0:
            new_node = self.Node()
            new_node.code = self.next_code
            self.next_code += 1
            new_node.text = word
            current.children[word] = new_node
            return

        last_match = ""
        i = 0
        char = word[i]
        while (
            i < len(word)
            and len(
                [
                    prefix
                    for prefix in current.children.keys()
                    if prefix.startswith(last_match + char)
                ]
            )
            > 0
        ):
            last_match += char
            if len(word) > 1:
                char = word[i + 1]
            i += 1

        # last_match contem o maior prefixo comum entre word e o text de algum current.children
        if last_match == "":  # nenhum children com nome prefixo
            new_node = self.Node()
            new_node.code = self.next_code
            self.next_code += 1
            new_node.endOfWord = True
            new_node.text = word
            current.children[word] = new_node
            return

        if last_match in current.children.keys():
            self._insertWord(word[len(last_match) :], current.children[last_match])
            return

        old_node_prefix, next_node = [
            (k, v) for (k, v) in current.children.items() if k.startswith(last_match)
        ][0]
        current.children[last_match] = self._split_node(last_match, next_node)
        del current.children[old_node_prefix]
        self._insertWord(word[len(last_match) :], current.children[last_match])
        current.endOfWord = True
        current.code = self.next_code
        self.next_code += 1

    def _split_node(self, prefix, node_descending):
        new_node = self.Node()
        new_node.code = self.next_code
        self.next_code += 1
        new_node.text = prefix
        node_descending.text = node_descending.text[len(prefix) :]
        new_node.children[node_descending.text] = node_descending
        return new_node

    def allWords(self, prefix, results):
        self._allWords(prefix, self.root, results)

    def _allWords(self, prefix, node, results):
        """
        Recursively call the loop
        Prefix will be prefix + current character
        Node will be position of char's child
        results are passed by reference to keep storing result

        Eventually, when we reach EOW, the prefix will have all the chars from starting and will be the word that we need. We add this word to the result
        """
        if node.endOfWord:
            results.append(prefix)
        for char in node.children.keys():
            # print char, node, node.children
            self._allWords(prefix + char, node.children[char], results)

    def searchWord(self, word):
        """
        Loop through chars of the word in the trie
        If char in word is not in trie.children(), return
        If char found, keep iterating
        After iteration for word is done, we should be at the end of word. If not, then word doesn't exist and we return false.
        """
        current = self.root
        search_result = True
        for char in word:
            if char in current.children.keys():
                pass
            else:
                search_result = False
                break
            current = current.children[char]
        if not current.endOfWord:
            search_result = False
        return search_result, current.code

    def getWordsWithPrefix(self, prefix, prefix_result):
        """
        We loop through charcters in the prefix along with trie
        If mismatch, return
        If no mismatch during iteration, we have reached the end of prefix. Now we need to get words from current to end with the previx that we passed. So call allWords with prefix
        """
        current = self.root
        for char in prefix:
            if char in current.children.keys():
                pass
            else:
                return
            current = current.children[char]
        self._allWords(prefix, current, prefix_result)


dic = Trie()
words = ["bed", "ben"]
words = [
    "joao",
    "jota",
    "joaos",
    "jotas",
    "beterraba",
    "j",
    "jabuticaba",
]
for word in words:
    dic.insertWord(word)

print(dic.root.children)

# results = []
# prefix = ""
# dic.allWords(prefix, results)
# # prefix will be added to every word found in the result, so we start with ''
# # results is empty, passed as reference so all results are stored in this list
# print("All words in trie: {}\n\n".format(results))

# search_word = "bomb"
# search_result = dic.searchWord(search_word)
# print("Search {} in {}: {}".format(search_word, words, search_result))

# search_word = "bomber"
# search_result = dic.searchWord(search_word)
# print("Search {} in {}: {}".format(search_word, words, search_result))

# prefix_result = []
# prefix = "be"
# dic.getWordsWithPrefix(prefix, prefix_result)
# print("\n\nWords starting with {}: {}".format(prefix, prefix_result))
# print(dic.root.children["b"].children["e"].children["d"].code)
