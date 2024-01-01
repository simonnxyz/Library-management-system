from json_methods import read_json, write_json
from class_book import Book
from class_user import User, Librarian
from errors import (
    NoBookIDError,
    NoUserIDError,
    BorrowedBookError,
    UserWithBooksError,
    KeywordNotFoundError,
    GenresNotFoundError,
    UnavailableGenreError,
    NoKeywordError,
    NoLibrarianIDError,
    UnavailableAuthorError,
    AuthorsNotFoundError,
    YearsNotFoundError,
    UnavailableYearError,
    NoBooksError,
    NoUsersError,
    WrongPasswordError,
    RemoveYourselfError,
)


class Library:
    """
    Library class representing a library with books, users, and librarians.
    Reads books, users, and librarians data from JSON files.
    """
    def __init__(self):
        self._books = read_json('books.json')
        self._users = read_json('users.json')
        self._librarians = read_json('librarians.json')

    @property
    def books(self):
        return self._books

    @property
    def users(self):
        return self._users

    @property
    def librarians(self):
        return self._librarians

    def login_role_check(self, id: int, password: str):
        """
        Check the login credentials for a user or librarian.
        """
        for user_info in self.users:
            if user_info["id"] == id:
                if user_info["password"] != password:
                    raise WrongPasswordError
                return user_info
        for librarian_info in self.librarians:
            if librarian_info["id"] == id:
                if librarian_info["password"] != password:
                    raise WrongPasswordError
                return librarian_info

    def update_data(self):
        """
        Update library data by re-reading information from JSON files.
        """
        self._books = read_json('books.json')
        self._users = read_json('users.json')
        self._librarians = read_json('librarians.json')

    def add_new_book(self, new_book: Book) -> str:
        """
        Add a new book to the library.
        """
        self._books.append(new_book.__dict__())
        write_json('books.json', self.books)
        return f'The book ({new_book.id}) has been successfully added.'

    def remove_book(self, book_id: int) -> str:
        """
        Remove a book from the library.
        """
        updated_books = []
        for book_info in self.books:
            if book_info["id"] != book_id:
                updated_books.append(book_info)
            elif book_info["id"] == book_id and book_info["current_owner"]:
                raise BorrowedBookError
        if updated_books == self.books:
            raise NoBookIDError(book_id)
        self._books = updated_books
        write_json('books.json', self.books)
        return f'The book ({book_id}) has been successfully removed.'

    def add_copy_of_book(self, book_id: int, new_id: int) -> str:
        """
        Add a copy of an existing book to the library.
        """
        book_copy = None
        for book_info in self.books:
            if book_info["id"] == book_id:
                book_copy = book_info
        if not book_copy:
            raise NoBookIDError(book_id)
        title = book_copy["title"]
        author = book_copy["author"]
        release_year = book_copy["release_year"]
        genre = book_copy["genre"]
        book = Book(new_id, title, author, release_year, genre)
        self.add_new_book(book)
        return f'The copy of book ({book_id}) has been successfully added.'

    def search_book_by_keyword(self, keyword: str) -> str:
        """
        Search for books in the library by a keyword.
        """
        if not keyword:
            raise NoKeywordError
        searches = []
        for book_info in self.books:
            values = list(book_info.values())
            for value in values:
                if str(keyword).lower() in str(value).lower():
                    book = Book(**book_info)
                    searches.append(str(book))
                    break
        if not searches:
            raise KeywordNotFoundError
        return '\n'.join(searches)

    def available_genres(self):
        """
        Get a list of available genres in the library.
        """
        genres = [book_info["genre"] for book_info in self.books]
        if not genres:
            raise GenresNotFoundError
        return genres

    def search_book_by_genre(self, chosen_genre: str) -> str:
        """
        Search for books in the library by genre.
        """
        if chosen_genre not in self.available_genres():
            raise UnavailableGenreError
        searches = []
        for book_info in self.books:
            if chosen_genre == book_info["genre"]:
                book = Book(**book_info)
                searches.append(str(book))
        return '\n'.join(searches)

    def available_authors(self):
        """
        Get a list of available authors in the library.
        """
        authors = [book_info["author"] for book_info in self.books]
        if not authors:
            raise AuthorsNotFoundError
        return authors

    def search_book_by_author(self, chosen_author: str) -> str:
        """
        Search for books in the library by author.
        """
        if chosen_author not in self.available_authors():
            raise UnavailableAuthorError
        searches = []
        for book_info in self.books:
            if chosen_author == book_info["author"]:
                book = Book(**book_info)
                searches.append(str(book))
        return '\n'.join(searches)

    def available_years(self):
        """
        Get a list of available release years in the library.
        """
        years = [str(book_info["release_year"]) for book_info in self.books]
        if not years:
            raise YearsNotFoundError
        return years

    def search_book_by_year(self, chosen_year: str) -> str:
        """
        Search for books in the library by release year.
        """
        if chosen_year not in self.available_years():
            raise UnavailableYearError
        searches = []
        for book_info in self.books:
            if chosen_year == str(book_info["release_year"]):
                book = Book(**book_info)
                searches.append(str(book))
        return '\n'.join(searches)

    def add_new_user(self, new_user: User):
        """
        Add a new user to the library.
        """
        self._users.append(new_user.__dict__())
        write_json('users.json', self.users)

    def remove_user(self, user_id: int):
        """
        Remove a user from the library.
        """
        updated_users = []
        for user_info in self.users:
            borrowed = user_info["borrowed_books"]
            reserved = user_info["reservations"]
            if user_info["id"] != user_id:
                updated_users.append(user_info)
            elif user_info["id"] == user_id and (borrowed or reserved):
                raise UserWithBooksError
        if updated_users == self.users:
            raise NoUserIDError(user_id)
        self._users = updated_users
        write_json('users.json', self.users)

    def add_new_librarian(self, new_librarian: Librarian):
        """
        Add a new librarian to the library.
        """
        self._librarians.append(new_librarian.__dict__())
        write_json('librarians.json', self.librarians)

    def remove_librarian(self, remove_id: int, librarian_id: int):
        """
        Remove a librarian from the library.
        """
        if librarian_id == remove_id:
            raise RemoveYourselfError
        updated_librarians = []
        for librarian_info in self.librarians:
            id = librarian_info["id"]
            if id != remove_id:
                updated_librarians.append(librarian_info)
        if updated_librarians == self.librarians:
            raise NoLibrarianIDError(remove_id)
        self._librarians = updated_librarians
        write_json('librarians.json', self.librarians)

    def get_books_stats(self):
        """
        Get statistics on the number of times each book has been borrowed.
        """
        if not self.books:
            raise NoBooksError
        stats = {}
        for book_info in self.books:
            book = Book(**book_info)
            stats[f'{book.title} ({book.id})'] = len(book.loan_history)
        return stats

    def get_users_stats(self):
        """
        Get statistics on the number of books borrowed by each user.
        """
        if not self.users:
            raise NoUsersError
        stats = {}
        for user_info in self.users:
            user = User(**user_info)
            stats[f'{user.name} ({user.id})'] = len(user.borrowing_history)
        return stats

    def available_books_info(self) -> str:
        """
        Get information on all available books in the library.
        """
        info = []
        for book_info in self.books:
            book = Book(**book_info)
            info.append(str(book))
        return '\n'.join(info)

    def users_librarians(self) -> str:
        """
        Get information on all users and librarians in the library.
        """
        users_librarians = []
        for user_info in self.users:
            user = User(**user_info)
            users_librarians.append(user.search_info())
        for librarian_info in self.librarians:
            librarian = Librarian(**librarian_info)
            users_librarians.append(librarian.search_info())
        return '\n'.join(users_librarians)

    def search_user(self, keyword) -> str:
        """
        Search for users or librarians in the library by a keyword.
        """
        if not keyword:
            raise NoKeywordError
        searches = []
        for user_info in self.users:
            values = (user_info["id"], user_info["name"])
            for value in values:
                if str(keyword).lower() in str(value).lower():
                    user = User(**user_info)
                    searches.append(user.search_info())
                    break
        for librarian_info in self.librarians:
            values = (librarian_info["id"], librarian_info["name"])
            for value in values:
                if str(keyword).lower() in str(value).lower():
                    librarian = Librarian(**librarian_info)
                    searches.append(librarian.search_info())
                    break
        if not searches:
            raise KeywordNotFoundError
        return '\n'.join(searches)
