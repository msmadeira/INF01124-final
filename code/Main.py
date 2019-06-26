import time
import io
import csv
import math


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
    return node.movie_id_if_finished


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


# Variables definition
hash_length = 27281
aux_arr = []
root = TrieNode('*')
start = time.time()

# Main logic

with io.open("../inputs/movie.csv", "r", encoding="utf-8") as movie_csv,\
        io.open("../inputs/rating.csv", "r", encoding="utf-8") as minirating_csv:
    movie_reader = csv.reader(movie_csv, delimiter=',')
    minirating_reader = csv.reader(minirating_csv, delimiter=',')
    line_count = 0
    for i, row in enumerate(movie_reader):
        if i != 0:
            movie_id = row[0]
            title = row[1]
            genres = row[2]
            while len(aux_arr) < int(movie_id):
                aux_arr.append(None)
            aux_arr.append(MovieDetails(genres))
            add(root, title, movie_id)
    for i, row in enumerate(minirating_reader):
        if i != 0:
            movie_id = row[1]
            rating = row[2]
            aux_arr[int(movie_id)].movie_id = int(movie_id)
            aux_arr[int(movie_id)].rating_number += 1
            aux_arr[int(movie_id)].rating_total = aux_arr[int(movie_id)].rating_total + float(rating)

clean_arr = [x for x in aux_arr if x is not None]
movie_hash_table = chaining_hash_table(clean_arr)
# print(find_prefix(root, 'Grumpier Old Men (1995)'))
# print(find_in_chaining_hash_table(movie_hash_table, 260).rating_number)
end = time.time()
print(end - start)
