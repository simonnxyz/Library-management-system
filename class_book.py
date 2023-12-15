from errors import (
    EmptyTitleError,
    NoAuthorError,
    NoReleaseYearError,
    NoGenreError,
)


class Book:
    """
    Book class representing a book in the library.
    ID range: 1000 - 9999.
    """
    def __init__(
            self,
            id: int,
            title: str,
            author: str,
            release_year: int,
            genre: str,
            loan_history=None,
            current_owner=None,
            extensions=0,
            reservations=None,
            ):
        if not title:
            raise EmptyTitleError('The title cannot be empty')
        if not author:
            raise NoAuthorError('Author name is required')
        if not release_year:
            raise NoReleaseYearError('Release year is required')
        if not genre:
            raise NoGenreError('Genre information is required')
        self._id = id
        self._title = str(title)
        self._author = str(author)
        self._release_year = release_year
        self._genre = str(genre)
        self._loan_history = loan_history or []
        self._current_owner = current_owner
        self._extensions = extensions
        self._reservations = reservations or []

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def release_year(self):
        return self._release_year

    @property
    def genre(self):
        return self._genre

    @property
    def loan_history(self):
        return self._loan_history

    @property
    def current_owner(self):
        return self._current_owner

    @property
    def extensions(self):
        return self._extensions

    @property
    def reservations(self):
        return self._reservations

    def set_extensions(self, new_extensions):
        self._extensions = new_extensions

    def __dict__(self):
        """
        Returns a dictionary representation of the book's attributes.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "release_year": self.release_year,
            "genre": self.genre,
            "loan_history": self.loan_history,
            "current_owner": self.current_owner,
            "extensions": self.extensions,
            "reservations": self.reservations
        }

    def __str__(self):
        """
        Return a string representation of the book's basic information.
        """
        return (
                'ID: ' + str(self.id) +
                ', Title: ' + self.title +
                ', Author: ' + self.author +
                ', Release year: ' + str(self.release_year) +
                ', Genre: ' + self.genre
                )
