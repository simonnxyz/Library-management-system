class Book:
    def __init__(
            self,
            id: int,
            title: str,
            author: str,
            release_year: str,
            genre: str,
            loan_history=[],
            current_owner=None,
            extensions=3,
            reservations=[],
            ):
        self._id = id
        self._title = str(title)
        self._author = str(author)
        self._release_year = str(release_year)
        self._genre = str(genre)
        self._loan_history = loan_history
        self._current_owner = current_owner
        self._extensions = extensions
        self._reservations = reservations

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

    def dict_info(self):
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
        return ('ID: ' + str(self.id) +
                ', Title: ' + self.title +
                ', Author: ' + self.author +
                ', Release year: ' + self.release_year +
                ', Genre: ' + self.genre
                )
