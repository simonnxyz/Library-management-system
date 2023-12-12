from random import randint
from class_book import Book
from json_methods import read_json


def create_book_id():
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
