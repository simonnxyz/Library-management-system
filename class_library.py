from json_methods import read_json, write_json
from generate_id import generate_book_id
from class_book import Book


class Library:
    def __init__(self):
        self._books = read_json('books.json')
        self._users = read_json('users.json')
        self._librarians = read_json('librarians.json')

    @property
    def books(self):
        return self._books

    @property
    def users(self):
        return self._users

    @property
    def librarians(self):
        return self._librarians

    def add_new_book(
            self,
            title: str,
            author: str,
            release_year: int,
            genre: str,
            ):
        id = generate_book_id()
        new_book = Book(id, title, author, release_year, genre)
        self._books.append(new_book.__dict__)
        write_json('books.json', self.books)
        return f'The book ({id}) has been successfully added.'
