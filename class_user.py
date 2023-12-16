from errors import (
    EmptyNameError,
    ShortPasswordError,
)


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

    def borrow_book(self):
        pass

    def return_book(self):
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
