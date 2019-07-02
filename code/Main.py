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
    global movie_ids_aux_arr
    my_list = []
    if len(trie.children) == 0 and prefix != '':
        my_list.append(prefix)
        movie_ids_aux_arr.append(trie.movie_id_if_finished)
    else:
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
        return False
    for char in prefix:
        char_found = False
        for child in node.children:
            if child.char == char:
                char_found = True
                node = child
                break
        if not char_found:
            return False
    return node


#  Hash Table related functions and classes
class MovieDetails(object):
    def __init__(self, movie_id, movie_genres, movie_name):
        self.genres = movie_genres
        self.movie_id = movie_id
        self.movie_name = movie_name
        self.rating_total = 0.0
        self.rating_number = 0
        self.user_rating = 0
        self.tags = []


def find_in_chaining_hash_table(hash_table, el):
    code = hash_code(el)
    if hash_table[code]:
        for movie_detail in hash_table[code]:
            if movie_detail.movie_id == el:
                return movie_detail
        return -1
    return -1


def find_by_genre_in_chaining_hash_table(hash_table, genre, min_rating_count):
    movie_bidimensional_list = [x for x in hash_table if len(x) > 0]
    aux_list = []
    formatted_genre = genre.replace("'", "")
    for movies in movie_bidimensional_list:
        for movie in movies:
            genres = movie.genres.split("|")
            if formatted_genre in genres and movie.rating_number >= min_rating_count:
                aux_list.append(movie)
    return aux_list


def find_by_tags_in_chaining_hash_table(hash_table, tags):
    movie_bidimensional_list = [x for x in hash_table if len(x) > 0]
    aux_list = []
    for movies in movie_bidimensional_list:
        for movie in movies:
            if all(tag in movie.tags for tag in tags):
                aux_list.append(movie)
    return aux_list


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


class UserMovieDetailsAux(object):
    def __init__(self, id, rating):
        self.movie_id = id
        self.user_rating = rating


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

# Miscellaneous


def bubble_sort(lst):
    elements = len(lst)-1
    ordered = False
    while not ordered:
        ordered = True
        for i in range(elements):
            if lst[i].rating_total > lst[i+1].rating_total:
                lst[i], lst[i+1] = lst[i+1], lst[i]
                ordered = False
    lst.reverse()
    return lst


def query_menu():
    query = input("Enter a query: ")
    query_function = query.split()[0]
    query_param = query.replace(query_function + " ", "")

    if query_function == "movie":
        global movie_ids_aux_arr
        global root
        global movie_hash_table
        movie_ids_aux_arr = []
        trie_prefix = find_prefix(root, query_param)
        if not trie_prefix:
            print('Movie not found')
        else:
            f = open("query_output.csv", "w+")
            writer = csv.writer(f)
            movies = list_words(trie_prefix, query_param)
            writer.writerow(['movieId', 'title', 'genres', 'rating', 'count'])
            for i, movie in enumerate(movies):
                movie_details = find_in_chaining_hash_table(movie_hash_table, int(movie_ids_aux_arr[i]))
                writer.writerow([movie_ids_aux_arr[i], movie, movie_details.genres, movie_details.rating_total, movie_details.rating_number])
            f.close()
            print('Query output file generated')
        query_menu()
    elif query_function == "user":
        user = user_tree.find(int(query_param))
        if not user:
            print('User not found')
        else:
            f = open("query_output.csv", "w+")
            writer = csv.writer(f)
            writer.writerow(['user_rating', 'title', 'global_rating', 'count'])
            for movie in user.rated_movies:
                writer.writerow([movie.user_rating, movie.movie_name, movie.rating_total, movie.rating_number])
            f.close()
            print('Query output file generated')
        query_menu()
    elif query_function == "tags":
        tags = query_param.replace("'", "").split()
        movie_by_tags = find_by_tags_in_chaining_hash_table(movie_hash_table, tags)
        mov = bubble_sort(movie_by_tags)
        if len(mov) == 0:
            print('Not found any movie with given tags')
        else:
            f = open("query_output.csv", "w+")
            writer = csv.writer(f)
            writer.writerow(['title', 'genres', 'rating', 'count'])
            for movie in mov:
                writer.writerow([movie.movie_name, movie.genres, movie.rating_total, movie.rating_number])
            f.close()
            print('Query output file generated')
        query_menu()
    else:
        if "top" in query_function:
            how_many = int(query_function[3:])
            # mudar na apresentacao
            movies_by_genre = find_by_genre_in_chaining_hash_table(movie_hash_table, query_param, 10)
            mov = bubble_sort(movies_by_genre)
            if len(mov) == 0:
                print('Not found any movie with given genre')
            else:
                f = open("query_output.csv", "w+")
                writer = csv.writer(f)
                writer.writerow(['title', 'genres', 'rating', 'count'])
                for i, movie in enumerate(mov):
                    if i < how_many:
                        writer.writerow([movie.movie_name, movie.genres, movie.rating_total, movie.rating_number])
                f.close()
                print('Query output file generated')
        else:
            print('Query function not found')
        query_menu()


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
        io.open("../inputs/rating.csv", "r", encoding="utf-8") as rating_csv,\
        io.open("../inputs/tag.csv", "r", encoding="utf-8") as tag_csv:
    movie_reader = csv.reader(movie_csv, delimiter=',')
    rating_reader = csv.reader(rating_csv, delimiter=',')
    tag_reader = csv.reader(tag_csv, delimiter=',')
    line_count = 0
    for i, row in enumerate(movie_reader):
        if i != 0:
            movie_id = row[0]
            title = row[1]
            genres = row[2]
            while len(movie_aux_arr) < int(movie_id):
                movie_aux_arr.append(None)
            movie_aux_arr.append(MovieDetails(int(movie_id), genres, title))
            add(root, title, movie_id)
    for i, row in enumerate(tag_reader):
        if i != 0:
            movie_id = int(row[1])
            tag = row[2]
            movie_aux_arr[movie_id].tags.append(tag)
    for i, row in enumerate(rating_reader):
        if i != 0:
            user_id = int(row[0])
            movie_id = int(row[1])
            rating = row[2]
            if len(user_aux_arr) <= user_id:
                while len(user_aux_arr) < user_id:
                    user_aux_arr.append(None)
                user_aux_arr.append(User(user_id))
            elif user_aux_arr[user_id] is None:
                user_aux_arr[user_id] = User(user_id)
            user_aux_arr[user_id].rated_movies.append(UserMovieDetailsAux(movie_id, float(rating)))
            movie_aux_arr[movie_id].rating_number += 1
            movie_aux_arr[movie_id].rating_total = movie_aux_arr[movie_id].rating_total + float(rating)

# for x in user_aux_arr:
#     if x is not None:
#         aux_list = []
#         for i, rated_movie in enumerate(x.rated_movies):
#             x.rated_movies[i] = movie_aux_arr[rated_movie.movie_id]
#             x.rated_movies[i].user_rating = rated_movie.user_rating
#         user_tree.insert(x)
movie_clean_arr = [x for x in movie_aux_arr if x is not None]
movie_hash_table = chaining_hash_table(movie_clean_arr)
end = time.time()
print(end - start)

query_menu()
