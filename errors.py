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


class EmptyPasswordError(Exception):
    def __str__(self):
        return 'Your password cannot be empty.'


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
        return 'This book is currently borrowed.'


class UserWithBooksError(Exception):
    def __str__(self):
        return 'Cannot remove user with books.'


class KeywordNotFoundError(Exception):
    def __str__(self):
        return 'Nothing found matching the provided keyword.'


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


class UsersBookError(Exception):
    def __str__(self):
        return 'You are the current owner.'


class NegativeExtensionsError(Exception):
    def __str__(self):
        return 'Used extensions cannot be negative.'


class NotUsersBookError(Exception):
    def __str__(self):
        return 'You are not the current owner.'


class NotEnoughExtensionsError(Exception):
    def __str__(self):
        return 'You have run out of extensions.'


class ReservedBookError(Exception):
    def __str__(self):
        return 'You cannot use the extension, the book has been reserved.'


class NoBookOwnerError(Exception):
    def __str__(self):
        return 'You do not need to reserve this book. It has no owner'


class NotReservedError(Exception):
    def __str__(self):
        return 'You did not reserve that book'


class WrongPasswordError(Exception):
    def __str__(self):
        return 'Incorrect password.'


class WrongIDError(Exception):
    def __str__(self):
        return 'The given ID not found.'


class RemoveYourselfError(Exception):
    def __str__(self):
        return 'You cannot remove yourself.'


class DoubleReservationBookError(Exception):
    def __str__(self):
        return 'You have already reserved this book.'
