from errors import (
    EmptyTitleError,
    NoAuthorError,
    NoReleaseYearError,
    NoGenreError,
)
from datetime import date, timedelta


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
            return_date=None,
            ):
        if not title:
            raise EmptyTitleError
        if not author:
            raise NoAuthorError
        if not release_year:
            raise NoReleaseYearError
        if not genre:
            raise NoGenreError
        self._id = id
        self._title = title
        self._author = author
        self._release_year = release_year
        self._genre = genre
        self._loan_history = loan_history or []
        self._current_owner = current_owner
        self._extensions = extensions
        self._reservations = reservations or []
        self._return_date = return_date

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

    @property
    def return_date(self):
        return self._return_date

    def set_extensions(self, new_extensions):
        self._extensions = new_extensions

    def set_owner(self, new_owner):
        # dodac testy
        self._current_owner = new_owner

    def add_reservation(self, reservation):
        # dodac testy
        self._reservations.append(reservation)

    def remove_first_reservation(self):
        # dodac testy
        removed = self._reservations.pop(0)
        return removed

    def history_append(self, loan):
        # dodac testy
        self._loan_history.append(loan)

    def set_return_date(self):
        self._return_date = date.today()

    def extend_return_date(self):
        self._return_date += timedelta(days=30)

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
            "reservations": self.reservations,
            "return_date": self.return_date
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
                ', Genre: ' + self.genre +
                ', Owner: ' + str(self.current_owner) +
                ', Return date: ' + str(self.return_date)
                )
