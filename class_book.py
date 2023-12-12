class Book:
    def __init__(
            self,
            id: int,
            title: str,
            author: str,
            release_year: str,
            genre: str,
            loan_history=[],
            borrowed_by=None,
            extensions=3,
            reservations=[],
            ):
        self._id = id
        self._title = str(title)
        self._author = str(author)
        self._release_year = str(release_year)
        self._genre = str(genre)
        self._loan_history = loan_history
        self._borrowed_by = borrowed_by
        self._extensions = extensions
        self._reservations = reservations