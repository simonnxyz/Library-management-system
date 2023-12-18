class EmptyTitleError(Exception):
    def __str__(self):
        return 'The title cannot be empty.'


class NoAuthorError(Exception):
    def __str__(self):
        return 'Author name is required.'


class NoReleaseYearError(Exception):
    def __str__(self):
        return 'Release year is required.'


class NoGenreError(Exception):
    def __str__(self):
        return 'Genre information is required.'


class EmptyNameError(Exception):
    def __str__(self):
        return 'Your name cannot be empty.'


class ShortPasswordError(Exception):
    def __str__(self):
        return 'Minimum password length is 6 characters.'


class NoBookIDError(Exception):
    def __init__(self, book_id):
        super().__init__(f'Book ID {book_id} not found in the list of books.')


class NoUserIDError(Exception):
    def __init__(self, user_id):
        super().__init__(f'User ID {user_id} not found in the list of users.')


class BorrowedBookError(Exception):
    def __str__(self):
        return 'Cannot remove borrowed book.'


class UserWithBooksError(Exception):
    def __str__(self):
        return 'Cannot remove user with books.'


class KeywordNotFoundError(Exception):
    def __str__(self):
        return 'No books found matching the provided keyword.'


class NoKeywordError(Exception):
    def __str__(self):
        return 'Keyword is required'


class UnavailableGenreError(Exception):
    def __str__(self):
        return 'Chosen genre is not available in our library.'


class GenresNotFoundError(Exception):
    def __str__(self):
        return 'No genres found in the list of books.'


class NoLibrarianIDError(Exception):
    def __init__(self, id):
        super().__init__(f'Librarian ID {id} not found in the list of users.')


class UnavailableAuthorError(Exception):
    def __str__(self):
        return 'Chosen author is not available in our library.'


class AuthorsNotFoundError(Exception):
    def __str__(self):
        return 'No authors found in the list of books.'


class UnavailableYearError(Exception):
    def __str__(self):
        return 'Chosen release year is not available in our library.'


class YearsNotFoundError(Exception):
    def __str__(self):
        return 'No release years found in the list of books.'


class NoBooksError(Exception):
    def __str__(self):
        return 'Currently our library has no books.'


class NoUsersError(Exception):
    def __str__(self):
        return 'Currently our library has no users.'


class UsersBookError(Exception):
    def __str__(self):
        return 'You are the current owner'


class NegativeExtensionsError(Exception):
    pass
