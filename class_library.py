from json_methods import read_json, write_json
from generate_id import (
    generate_book_id,
    generate_user_id,
    generate_librarian_id
)
from class_book import Book
from class_user import User, Librarian
from errors import (
    NoBookIDError,
    NoUserIDError,
    BorrowedBookError,
    UserWithBooksError,
    KeywordNotFoundError,
    GenresNotFoundError,
    UnavailableGenreError,
    NoKeywordError,
    NoLibrarianIDError,
)


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

    def remove_book(self, book_id: int):
        updated_books = []
        for book_info in self.books:
            if book_info["id"] != book_id:
                updated_books.append(book_info)
            elif book_info["id"] == book_id and book_info["current_owner"]:
                raise BorrowedBookError
        if updated_books == self.books:
            raise NoBookIDError(book_id)
        self._books = updated_books
        write_json('books.json', self.books)
        return f'The book ({book_id}) has been successfully removed.'

    def add_copy_of_book(self, book_id: int):
        book_copy = None
        for book_info in self.books:
            if book_info["id"] == book_id:
                book_copy = book_info
        if not book_copy:
            raise NoBookIDError(book_id)
        title = book_copy["title"]
        author = book_copy["author"]
        release_year = book_copy["release_year"]
        genre = book_copy["genre"]
        self.add_new_book(title, author, release_year, genre)
        return f'The copy of book ({book_id}) has been successfully added.'

    def search_book_by_keyword(self, keyword):
        if not keyword:
            raise NoKeywordError
        searches = []
        for book_info in self.books:
            if keyword in book_info.values():
                book = Book(**book_info)
                searches.append(str(book))
        if not searches:
            raise KeywordNotFoundError
        return '\n'.join(searches)

    def available_genres(self):
        genres = set()
        for book_info in self.books:
            genre = book_info["genre"]
            genres.add(genre)
        if not genres:
            raise GenresNotFoundError
        return list(genres)

    def search_book_by_genre(self, chosen_genre):
        if chosen_genre not in self.available_genres():
            raise UnavailableGenreError
        searches = []
        for book_info in self.books:
            if chosen_genre == book_info["genre"]:
                book = Book(**book_info)
                searches.append(str(book))
        return '\n'.join(searches)

    def add_new_user(self, name: str, password: str):
        id = generate_user_id()
        new_user = User(id, name, password)
        self._users.append(new_user.__dict__())
        write_json('users.json', self.users)

    def remove_user(self, user_id: int):
        updated_users = []
        for user_info in self.users:
            if user_info["id"] != user_id:
                updated_users.append(user_info)
            elif user_info["id"] == user_id and user_info["borrowed_books"]:
                raise UserWithBooksError
        if updated_users == self.users:
            raise NoUserIDError(user_id)
        self._users = updated_users
        write_json('users.json', self.users)

    def add_new_librarian(self, name: str, password: str):
        id = generate_librarian_id()
        new_librarian = Librarian(id, name, password)
        self._librarians.append(new_librarian.__dict__())
        write_json('librarians.json', self.librarians)

    def remove_librarian(self, librarian_id: int):
        updated_librarians = []
        for librarian_info in self.librarians:
            id = librarian_info["id"]
            if id != librarian_id:
                updated_librarians.append(librarian_info)
        if updated_librarians == self.librarians:
            raise NoLibrarianIDError(librarian_id)
        self._librarians = updated_librarians
        write_json('librarians.json', self.librarians)
