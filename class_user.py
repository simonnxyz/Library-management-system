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