class Trie:
    class Node:
        def __init__(self):
            self.children = {}
            self.endOfWord = False
            self.code = -1

    def __init__(self):
        self.root = self.Node()
        self.next_code = 0

    def insertWord(self, word):
        """
        Loop through characters in a word and keep adding them at a new node, linking them together
        If char already in node, pass
        Increment the current to the child with the character
        After the characters in word are over, mark current as EOW
        """
        current = self.root
        for char in word:
            if char in current.children.keys():
                pass
            else:
                current.children[char] = self.Node()
            current = current.children[char]
        current.endOfWord = True
        current.code = self.next_code
        self.next_code += 1

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
words = ["bed", "bedlam", "bond", "bomber", "bombay"]
for word in words:
    dic.insertWord(word)

results = []
prefix = ""
dic.allWords(prefix, results)
# prefix will be added to every word found in the result, so we start with ''
# results is empty, passed as reference so all results are stored in this list
print("All words in trie: {}\n\n".format(results))

search_word = "bomb"
search_result = dic.searchWord(search_word)
print("Search {} in {}: {}".format(search_word, words, search_result))

search_word = "bomber"
search_result = dic.searchWord(search_word)
print("Search {} in {}: {}".format(search_word, words, search_result))

prefix_result = []
prefix = "be"
dic.getWordsWithPrefix(prefix, prefix_result)
print("\n\nWords starting with {}: {}".format(prefix, prefix_result))
print(dic.root.children["b"].children["e"].children["d"].code)
