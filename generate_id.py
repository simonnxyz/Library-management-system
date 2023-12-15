from random import randint
from class_book import Book
from class_user import User, Librarian
from json_methods import read_json


def generate_book_id():
    books = read_json('books.json')
    while True:
        random_id = randint(1000, 9999)
        all_ids = []
        for book_info in books:
            book = Book(**book_info)
            all_ids.append(book.id)
        if random_id not in all_ids:
            return random_id
        else:
            continue


def generate_user_id():
    users = read_json('users.json')
    while True:
        random_id = randint(2000, 9999)
        all_ids = []
        for user_info in users:
            user = User(**user_info)
            all_ids.append(user.id)
        if random_id not in all_ids:
            return random_id
        else:
            continue


def generate_librarian_id():
    librarians = read_json('librarians.json')
    while True:
        random_id = randint(1000, 1999)
        all_ids = []
        for librarian_info in librarians:
            librarian = Librarian(**librarian_info)
            all_ids.append(librarian.id)
        if random_id not in all_ids:
            return random_id
        else:
            continue
