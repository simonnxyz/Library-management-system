from errors import (
    EmptyNameError,
    EmptyPasswordError,
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
    Attributes:
    - id: The user's ID (ID range: 2000 - 9999).
    - name: The user's name.
    - password: The user's password.
    - borrowed_books: List of book IDs currently borrowed by the user.
    - reservations: List of book IDs reserved by the user.
    - borrowing_history: List of book IDs the user has borrowed in the past.
    """
    def __init__(
            self: str,
            id: int,
            name: str,
            password: str,
            borrowed_books=None,
            reservations=None,
            borrowing_history=None,
            ):
        if not name:
            raise EmptyNameError
        if not password:
            raise EmptyPasswordError
        if len(password) < 6:
            raise ShortPasswordError
        self._id = id
        self._name = name
        self._password = password
        self._borrowed_books = borrowed_books or []
        self._reservations = reservations or []
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
    def reservations(self):
        return self._reservations

    @property
    def borrowing_history(self):
        return self._borrowing_history

    def change_password(self, new_password: str):
        """
        Changes the user's password.
        """
        if len(new_password) < 6:
            raise ShortPasswordError
        self._password = new_password
        self.dict_update()

    def dict_update(self):
        """
        Updates the user's information in the JSON file.
        """
        users = read_json("users.json")
        for index, user_info in enumerate(users):
            if user_info["id"] == self.id:
                users[index].update(self.__dict__())
                break
        write_json('users.json', users)

    def history_append(self, book_id: int):
        """
        Appends a book ID to the user's borrowing history.
        """
        self._borrowing_history.append(book_id)
        self.dict_update()

    def borrowed_append(self, book_id: int):
        """
        Adds a book ID to the list of books currently borrowed by the user.
        """
        self._borrowed_books.append(book_id)
        self.dict_update()

    def borrowed_remove(self, book_id: int):
        """
        Removes a book ID from the list of books
        currently borrowed by the user.
        """
        self._borrowed_books.remove(book_id)
        self.dict_update()

    def reservations_append(self, book_id: int):
        """
        Adds a book ID to the list of reservations made by the user.
        """
        self._reservations.append(book_id)
        self.dict_update()

    def reservations_remove(self, book_id: int):
        """
        Removes a book ID from the list of reservations made by the user.
        """
        self._reservations.remove(book_id)
        self.dict_update()

    def get_borrowed_books(self):
        """
        Returns the list of books currently borrowed by the user.
        """
        info = 'You do not have any books at the moment.'
        if not self.borrowed_books:
            return info
        else:
            books = []
            for book_id in self.borrowed_books:
                for book_info in read_json('books.json'):
                    if book_info["id"] == book_id:
                        book = Book(**book_info)
                        books.append(book.borrow_info())
            return books

    def get_history(self):
        """
        Returns the list of books that the user has borrowed in the past.
        """
        info = 'You have not borrowed any books yet.'
        if not self.borrowing_history:
            return info
        else:
            books = []
            for book_id in self.borrowing_history:
                for book_info in read_json('books.json'):
                    if book_info["id"] == book_id:
                        book = Book(**book_info)
                        books.append(book.history_info())
            return books

    def get_reservations(self):
        """
        Returns the list of books that the user has reserved.
        """
        info = 'You do not have any reservations at the moment.'
        if not self.reservations:
            return info
        else:
            books = []
            for book_id in self.reservations:
                for book_info in read_json('books.json'):
                    if book_info["id"] == book_id:
                        book = Book(**book_info)
                        books.append(book.reservation_info(self.id))
            return books

    def borrow_book(self, book_id: int):
        """
        Borrows a book with the given book ID.
        """
        books = read_json('books.json')
        title = None
        for book_info in books:
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
                title = book.title
                break
        if books == read_json('books.json'):
            raise NoBookIDError(book_id)
        self.history_append(book_id)
        self.borrowed_append(book_id)
        return f"You have successfully borrowed the book '{title}'."

    def use_extension(self, book_id: int):
        """
        Extends the return date for a borrowed book.
        """
        if book_id not in self.borrowed_books:
            raise NotUsersBookError
        books = read_json('books.json')
        for book_info in books:
            if book_info["id"] == book_id:
                book = Book(**book_info)
                if book.reservations:
                    raise ReservedBookError
                if book.extensions < 1:
                    raise NotEnoughExtensionsError
                book.remove_extension()
                book.extend_return_date()
                break
        if books == read_json('books.json'):
            raise NoBookIDError(book_id)
        return "You have successfully extended the reservation."

    def reserve_book(self, book_id: int):
        """
        Reserves a book with the given book ID.
        """
        books = read_json('books.json')
        title = None
        for book_info in books:
            if book_info["id"] == book_id:
                book = Book(**book_info)
                if book.current_owner == self.id:
                    raise UsersBookError
                if not book.current_owner:
                    raise NoBookOwnerError
                book.add_reservation(self.id)
                title = book.title
                break
        if books == read_json('books.json'):
            raise NoBookIDError(book_id)
        self.reservations_append(book.id)
        return f"You have successfully reserved the book '{title}'."

    def cancel_reservation(self, book_id: int):
        """
        Cancels a reservation for a book with the given book ID.
        """
        books = read_json('books.json')
        users = read_json('users.json')
        title = None
        for book_info in books:
            if book_info["id"] == book_id:
                book = Book(**book_info)
                if self.id not in book.reservations:
                    raise NotReservedError
                book.remove_reservation(self.id)
                self.reservations_remove(book.id)
                title = book.title
        if users == read_json('users.json'):
            raise NoBookIDError(book_id)
        return ('You have successfully canceled' +
                f" the reservation for the book '{title}'.")

    def return_book(self, book_id: int):
        """
        Returns a borrowed book with the given book ID.
        """
        if book_id not in self.borrowed_books:
            raise NotUsersBookError
        books = read_json('books.json')
        title = None
        for book_info in books:
            if book_info["id"] == book_id:
                book = Book(**book_info)
                book.set_owner(None)
                book.set_extensions(0)
                book.set_return_date(None)
                title = book.title
                if book.reservations:
                    removed = book.remove_first_reservation()
                    for user_info in read_json('users.json'):
                        if user_info["id"] == removed:
                            rm_user = User(**user_info)
                            rm_user.borrow_book(book_id)
                            rm_user.reservations_remove(book_id)
        if books == read_json('books.json'):
            raise NoBookIDError(book_id)
        self.borrowed_remove(book_id)
        return f"You have returned the book {title}. Thank you!"

    def search_info(self):
        """
        Returns a string representation of the user's information.
        """
        list = ', '.join(map(str, self.borrowed_books))
        borrowed = list if self.borrowed_books else None
        list2 = ', '.join(map(str, self.reservations))
        reservations = list2 if self.reservations else None
        list3 = ', '.join(map(str, self.borrowing_history))
        history = list3 if self.borrowing_history else None
        return [self.id,
                self.name,
                self.password,
                borrowed,
                reservations,
                history
                ]

    def __dict__(self):
        """
        Returns a dictionary representation of the user's attributes.
        """
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "borrowed_books": self.borrowed_books,
            "reservations": self.reservations,
            "borrowing_history": self.borrowing_history,
        }


class Librarian(User):
    """
    Librarian class representing a library employee.
    Attributes:
    - id: The librarian's ID (ID range: 1000 - 1999.).
    - name: The librarian's name.
    - password: The librarian's password.
    """
    def __init__(
            self,
            id: int,
            name: str,
            password: str,
            ):
        super().__init__(id, name, password)

    def __dict__(self):
        """
        Returns a dictionary representation of the librarian's attributes.
        """
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
        }

    def search_info(self):
        """
        Returns a string representation of the librarian's information.
        """
        return [self.id,
                self.name,
                self.password,
                ]
