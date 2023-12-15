from json_methods import read_json, write_json
from generate_id import generate_book_id
from class_book import Book
from errors import NoBookIDError


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
        self._books.append(new_book.__dict__())
        write_json('books.json', self.books)
        return f'The book ({id}) has been successfully added.'

    def remove_book(
            self,
            book_id: int, 
            ):
        updated_books = []
        for book_info in self.books:
            if book_info["id"] != book_id:
                updated_books.append(book_info)
        if updated_books == self.books:
            raise NoBookIDError(book_id)
        self._books = updated_books
        write_json('books.json', self.books)
        return f'The book ({book_id}) has been successfully removed.'
