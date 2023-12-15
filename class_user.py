from errors import (
    EmptyNameError,
    ShortPasswordError,
)


class User:
    def __init__(
            self: str,
            id: str,
            name: str,
            password: str,
            borrowed_books=[],
            books_history=[],
            ):
        if not name:
            raise EmptyNameError('Your name cannot be empty')
        if len(password) < 6:
            raise ShortPasswordError('Minimum password length is 6 characters')
        self._id = id
        self._name = name
        self._password = password
        self._borrowed_books = borrowed_books
        self._books_history = books_history

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
    def books_history(self):
        return self._books_history

    def get_borrowed_books(self):
        info = 'You do not have any books at the moment.'
        if not self.borrowed_books:
            return info
        else:
            books = ', '.join(str(id) for id in self.borrowed_books)
            return f'You have borrowed: {books}'

    def get_history(self):
        info = 'You have not borrowed any books yet.'
        if not self.books_history:
            return info
        else:
            history = ', '.join(str(id) for id in self.books_history)
            return f'Your history: {history}'

    def borrow_book(self):
        pass

    def return_book(self):
        pass

    def __str__(self):
        return f'Welcome to our library, {self.name}! Your ID is {self.id}'

    def __dict__(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "borrowed_books": self.borrowed_books,
            "books_history": self.books_history,
        }


class Librarian(User):
    def __init__(
            self,
            id: int,
            name: str,
            password: str,
            ):
        super().__init__(id, name, password)

    def __str__(self):
        return f'Welcome, {self.name} (Librarian)! Your ID is {self.id}'

    def __dict__(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
        }
