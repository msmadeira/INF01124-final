class TrieNode(object):
    def __init__(self, char: str):
        self.char = char
        self.children = []
        # Is it the last character of the word.`
        # self.movie_id_if_finished = False
        self.word_finished = False
        # How many times this character appeared in the addition process
        self.counter = 1


def add(root, word: str):
    node = root
    for char in word:
        found_in_child = False
        # need improvement, could add an (new_word boolean to jump this unnecessary for in this case)
        for child in node.children:
            if child.char == char:
                child.counter += 1
                node = child
                found_in_child = True
                break
        if not found_in_child:
            new_node = TrieNode(char)
            node.children.append(new_node)
            node = new_node
    node.word_finished = True


def find_prefix(root, prefix: str):
    node = root
    if not root.children:
        return False, 0
    for char in prefix:
        char_found = False
        for child in node.children:
            if child.char == char:
                char_found = True
                node = child
                break
        if not char_found:
            return 0
    return node.counter


if __name__ == "__main__":
    root = TrieNode('*')
    add(root, "hackathon")
    add(root, 'hack')

    print(find_prefix(root, 'hac'))
    print(find_prefix(root, 'hack'))
    print(find_prefix(root, 'hackathon'))
    print(find_prefix(root, 'ha'))
    print(find_prefix(root, 'hammer'))