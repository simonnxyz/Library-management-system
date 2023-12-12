class User:
    def __init__(
            self: str,
            id: str,
            name: str,
            password: str,
            borrowed_books=[],
            ):
        self._id = id
        self._name = name
        self._password = password
        self._borrowed_books = borrowed_books

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
