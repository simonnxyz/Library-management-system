from random import randint
from class_book import Book
from class_user import User, Librarian
from json_methods import read_json


def generate_id(min_range, max_range, objects):
    while True:
        random_id = randint(min_range, max_range)
        all_ids = [object.id for object in objects]
        if random_id not in all_ids:
            return random_id


def generate_book_id():
    books = read_json('books.json')
    return generate_id(1000, 9999, [Book(**book_info) for book_info in books])


def generate_user_id():
    users = read_json('users.json')
    return generate_id(2000, 9999, [User(**user_info) for user_info in users])


def generate_librarian_id():
    libs = read_json('librarians.json')
    return generate_id(1000, 1999, [Librarian(**lib_info) for lib_info in libs])
