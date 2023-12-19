from errors import (
    EmptyNameError,
    ShortPasswordError,
    NoBookIDError,
    BorrowedBookError,
    UsersBookError,
    NotUsersBookError,
    NotEnoughExtensionsError,
    ReservedBookError,
    NoBookOwnerError,
    NotReservedError,
)
from class_book import Book
from json_methods import read_json, write_json


class User:
    """
    User class representing a library reader.
    ID range: 2000 - 9999.
    """
    def __init__(
            self: str,
            id: int,
            name: str,
            password: str,
            borrowed_books=None,
            borrowing_history=None,
            ):
        if not name:
            raise EmptyNameError
        if len(password) < 6:
            raise ShortPasswordError
        self._id = id
        self._name = name
        self._password = password
        self._borrowed_books = borrowed_books or []
        self._borrowing_history = borrowing_history or []

    @property
    def name(self):
        return self._name

    @property
    def password(self):
        return self._password

    @property
    def id(self):
        return self._id

    @property
    def borrowed_books(self):
        return self._borrowed_books

    @property
    def borrowing_history(self):
        return self._borrowing_history

    def history_append(self, book_id):
        self._borrowing_history.append(book_id)

    def borrowed_append(self, book_id):
        self._borrowed_books.append(book_id)

    def borrowed_remove(self, book_id):
        self._borrowed_books.remove(book_id)

    def get_borrowed_books(self):
        """
        Returns the list of book IDs currently borrowed by the user.
        """
        info = 'You do not have any books at the moment.'
        if not self.borrowed_books:
            return info
        else:
            books = ', '.join(str(id) for id in self.borrowed_books)
            return f'You have borrowed: {books}'

    def get_history(self):
        """
        Returns the list of book IDs that the user has borrowed in the past.
        """
        info = 'You have not borrowed any books yet.'
        if not self.borrowing_history:
            return info
        else:
            history = ', '.join(str(id) for id in self.borrowing_history)
            return f'Your history: {history}'

    def borrow_book(self, book_id):
        books = read_json('books.json')
        for index, book_info in enumerate(books):
            if book_info["id"] == book_id:
                book = Book(**book_info)
                if book.id in self.borrowed_books:
                    raise UsersBookError
                if book.current_owner:
                    raise BorrowedBookError('')
                book.set_owner(self.id)
                book.set_extensions(3)
                book.set_return_date()
                book.history_append(self.id)
                self.history_append(book_id)
                self.borrowed_append(book_id)
                books[index].update(book.__dict__())
                break
        if books == read_json('books.json'):
            raise NoBookIDError(book_id)
        users = read_json('users.json')
        for user_info in users:
            if user_info["id"] == self.id:
                user_info["borrowed_books"] = self.borrowed_books
                user_info["borrowing_history"] = self.borrowing_history
                break
        write_json('users.json', users)
        write_json('books.json', books)

    def use_extension(self, book_id):
        if book_id not in self.borrowed_books:
            raise NotUsersBookError
        books = read_json('books.json')
        for index, book_info in enumerate(books):
            if book_info["id"] == book_id:
                book = Book(**book_info)
                if book.reservations:
                    raise ReservedBookError
                if book.extensions < 1:
                    raise NotEnoughExtensionsError
                book.remove_extension()
                book.extend_return_date()
                books[index].update(book.__dict__())
        if books == read_json('books.json'):
            raise NoBookIDError(book_id)
        write_json('books.json', books)

    def reserve_book(self, book_id):
        books = read_json('books.json')
        for index, book_info in enumerate(books):
            if book_info["id"] == book_id:
                book = Book(**book_info)
                if book.current_owner == self.id:
                    raise UsersBookError
                if not book.current_owner:
                    raise NoBookOwnerError
                book.add_reservation(self.id)
                books[index].update(book.__dict__())
        if books == read_json('books.json'):
            raise NoBookIDError(book_id)
        write_json('books.json', books)

    def cancel_reservation(self, book_id):
        books = read_json('books.json')
        for index, book_info in enumerate(books):
            if book_info["id"] == book_id:
                book = Book(**book_info)
                if self.id not in book.reservations:
                    raise NotReservedError
                book.remove_reservation(self.id)
                books[index].update(book.__dict__())
        if books == read_json('books.json'):
            raise NoBookIDError(book_id)
        write_json('books.json', books)

    def return_book(self, book_id):
        if book_id not in self.borrowed_books:
            raise NotUsersBookError
        books = read_json('books.json')
        for index, book_info in enumerate(books):
            if book_info["id"] == book_id:
                book = Book(**book_info)
                if book.reservations:
                    removed = book.remove_first_reservation()
                    book.set_owner(removed)
                    book.set_extensions(3)
                    book.history_append(removed)
                    for user_info in read_json('users.json'):
                        if user_info["id"] == removed:
                            pass

    def __str__(self):
        """
        Returns a welcome message with the user's name and ID.
        """
        return f'Welcome to our library, {self.name}! Your ID is {self.id}'

    def __dict__(self):
        """
        Returns a dictionary representation of the user's attributes.
        """
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "borrowed_books": self.borrowed_books,
            "borrowing_history": self.borrowing_history,
        }


class Librarian(User):
    """
    Librarian class representing a library employee.
    ID range: 1000 - 1999.
    """
    def __init__(
            self,
            id: int,
            name: str,
            password: str,
            ):
        super().__init__(id, name, password)

    def __str__(self):
        """
        Returns a welcome message with the librarians's name and ID.
        """
        return f'Welcome, {self.name}! (Librarian) Your ID is {self.id}'

    def __dict__(self):
        """
        Returns a dictionary representation of the librarians's attributes.
        """
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
        }
