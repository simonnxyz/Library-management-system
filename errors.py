class EmptyTitleError(Exception):
    pass


class NoAuthorError(Exception):
    pass


class NoReleaseYearError(Exception):
    pass


class NoGenreError(Exception):
    pass


class EmptyNameError(Exception):
    pass


class ShortPasswordError(Exception):
    pass


class NoBookIDError(Exception):
    def __init__(self, book_id):
        super().__init__(f'Book ID {book_id} not found in the list of books')


class NoUserIDError(Exception):
    def __init__(self, user_id):
        super().__init__(f'User ID {user_id} not found in the list of users')


class BorrowedBookError(Exception):
    pass


class UserWithBooksError(Exception):
    pass
