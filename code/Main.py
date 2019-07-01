import time
import io
import csv
import math
import sys
sys.setrecursionlimit(10000)


# Trie related functions and classes
class TrieNode(object):
    def __init__(self, char: str):
        self.char = char
        self.children = []
        self.movie_id_if_finished = 0
        self.word_finished = False


def add(root, word, movie_id):
    node = root
    new_word = False
    for char in word:
        found_in_child = False
        if not new_word:
            for child in node.children:
                if child.char == char:
                    node = child
                    found_in_child = True
                    break
        if not found_in_child:
            new_word = True
            new_node = TrieNode(char)
            node.children.append(new_node)
            node = new_node
    node.movie_id_if_finished = movie_id


def list_words(trie, prefix=''):
    movie_ids_aux_arr = []
    my_list = []
    for k, v in enumerate(trie.children):
        if v.movie_id_if_finished == 0:
            for el in list_words(v):
                my_list.append(prefix + v.char + el)
        else:
            my_list.append(v.char)
            movie_ids_aux_arr.append(v.movie_id_if_finished)
    return my_list


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
    if node.movie_id_if_finished != 0:
        return node.movie_id_if_finished
    else:
        return node


#  Hash Table related functions and classes
class MovieDetails(object):
    def __init__(self, movie_genres):
        self.genres = movie_genres
        self.rating_total = 0.0
        self.rating_number = 0
        self.movie_id = 0


def find_in_chaining_hash_table(hash_table, el):
    code = hash_code(el)
    if hash_table[code]:
        for movie_detail in hash_table[code]:
            if movie_detail.movie_id == el:
                return movie_detail
        return -1
    return -1


def chaining_hash_table(lst):
    hash_table = [[] for i in range(hash_length)]
    for movie_detail in lst:
        code = hash_code(movie_detail.movie_id)
        if movie_detail.rating_number > 0:
            movie_detail.rating_total = movie_detail.rating_total / movie_detail.rating_number
        hash_table[code].append(movie_detail)
    return hash_table


def hash_code(k):
    return math.floor(k % hash_length)


# Free structure functions and classes
class User(object):
    def __init__(self, id):
        self.id = id
        self.rated_movies = []


class Node(object):
    def __init__(self, d):
        self.data = d
        self.left = None
        self.right = None

    def insert(self, d):
        if self.data.id == d.id:
            return False
        elif d.id < self.data.id:
            if self.left:
                return self.left.insert(d)
            else:
                self.left = Node(d)
                return True
        else:
            if self.right:
                return self.right.insert(d)
            else:
                self.right = Node(d)
                return True

    def find(self, id):
        if self.data.id == id:
            return self.data
        elif id < self.data.id and self.left:
            return self.left.find(id)
        elif id > self.data.id and self.right:
            return self.right.find(id)
        return False


class BST(object):
    def __init__(self):
        self.root = None

    def insert(self, d):
        if self.root:
            return self.root.insert(d)
        else:
            self.root = Node(d)
            return True

    def find(self, d):
        if self.root:
            return self.root.find(d)
        else:
            return False


# Variables definition
hash_length = 27281
movie_ids_aux_arr = []
movie_aux_arr = []
user_aux_arr = []
user_tree = BST()
user_clean_arr = []
root = TrieNode('*')
start = time.time()

# Main logic

with io.open("../inputs/movie.csv", "r", encoding="utf-8") as movie_csv,\
        io.open("../inputs/minirating.csv", "r", encoding="utf-8") as rating_csv:
    movie_reader = csv.reader(movie_csv, delimiter=',')
    rating_reader = csv.reader(rating_csv, delimiter=',')
    line_count = 0
    for i, row in enumerate(movie_reader):
        if i != 0:
            movie_id = row[0]
            title = row[1]
            genres = row[2]
            while len(movie_aux_arr) < int(movie_id):
                movie_aux_arr.append(None)
            movie_aux_arr.append(MovieDetails(genres))
            add(root, title, movie_id)
    for i, row in enumerate(rating_reader):
        if i != 0:
            user_id = int(row[0])
            movie_id = int(row[1])
            rating = row[2]
            if len(user_aux_arr) <= user_id:
                while len(user_aux_arr) < user_id:
                    user_aux_arr.append(None)
                user_aux_arr.append(User(user_id))
            else:
                user_aux_arr[user_id] = User(user_id)
            user_aux_arr[user_id].rated_movies.append(movie_id)
            movie_aux_arr[movie_id].movie_id = movie_id
            movie_aux_arr[movie_id].rating_number += 1
            movie_aux_arr[movie_id].rating_total = movie_aux_arr[movie_id].rating_total + float(rating)

for x in user_aux_arr:
    if x is not None:
        x.rated_movies = list(map(lambda index: movie_aux_arr[index], x.rated_movies))
        user_tree.insert(x)
# print(user_tree.find(48644).rated_movies[0].genres)
movie_clean_arr = [x for x in movie_aux_arr if x is not None]
movie_hash_table = chaining_hash_table(movie_clean_arr)
# print(find_in_chaining_hash_table(movie_hash_table, 260).rating_number)
end = time.time()
print(end - start)

query = input("Enter a query: ")
query_function = query.split()[0]
query_param = query.replace(query_function + " ", "")

if query_function == "movie":
    print(list_words(find_prefix(root, query_param), query_param))
    print(movie_ids_aux_arr)
