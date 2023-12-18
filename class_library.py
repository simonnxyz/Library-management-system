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
)


class Library:
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

    def update_data(self):
        self._books = read_json('books.json')
        self._users = read_json('users.json')
        self._librarians = read_json('librarians.json')

    def add_new_book(self, new_book: Book):
        self._books.append(new_book.__dict__())
        write_json('books.json', self.books)
        return f'The book ({new_book.id}) has been successfully added.'

    def remove_book(self, book_id: int):
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

    def add_copy_of_book(self, book_id: int, new_id: int):
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

    def search_book_by_keyword(self, keyword):
        if not keyword:
            raise NoKeywordError
        searches = []
        for book_info in self.books:
            values = list(book_info.values())
            for value in values:
                if str(keyword).lower() in str(value).lower():
                    book = Book(**book_info)
                    searches.append(str(book))
        if not searches:
            raise KeywordNotFoundError
        return '\n'.join(searches)

    def available_genres(self):
        genres = []
        for book_info in self.books:
            if book_info["genre"] not in genres:
                genres.append(book_info["genre"])
        if not genres:
            raise GenresNotFoundError
        return genres

    def search_book_by_genre(self, chosen_genre):
        if chosen_genre not in self.available_genres():
            raise UnavailableGenreError
        searches = []
        for book_info in self.books:
            if chosen_genre == book_info["genre"]:
                book = Book(**book_info)
                searches.append(str(book))
        return '\n'.join(searches)

    def available_authors(self):
        authors = []
        for book_info in self.books:
            if book_info["author"] not in authors:
                authors.append(book_info["author"])
        if not authors:
            raise AuthorsNotFoundError
        return authors

    def search_book_by_author(self, chosen_author):
        if chosen_author not in self.available_authors():
            raise UnavailableAuthorError
        searches = []
        for book_info in self.books:
            if chosen_author == book_info["author"]:
                book = Book(**book_info)
                searches.append(str(book))
        return '\n'.join(searches)

    def available_years(self):
        years = []
        for book_info in self.books:
            if book_info["release_year"] not in years:
                years.append(book_info["release_year"])
        if not years:
            raise YearsNotFoundError
        return years

    def search_book_by_year(self, chosen_year):
        if chosen_year not in self.available_years():
            raise UnavailableYearError
        searches = []
        for book_info in self.books:
            if chosen_year == book_info["release_year"]:
                book = Book(**book_info)
                searches.append(str(book))
        return '\n'.join(searches)

    def add_new_user(self, new_user: User):
        self._users.append(new_user.__dict__())
        write_json('users.json', self.users)

    def remove_user(self, user_id: int):
        updated_users = []
        for user_info in self.users:
            if user_info["id"] != user_id:
                updated_users.append(user_info)
            elif user_info["id"] == user_id and user_info["borrowed_books"]:
                raise UserWithBooksError
        if updated_users == self.users:
            raise NoUserIDError(user_id)
        self._users = updated_users
        write_json('users.json', self.users)

    def add_new_librarian(self, new_librarian: Librarian):
        self._librarians.append(new_librarian.__dict__())
        write_json('librarians.json', self.librarians)

    def remove_librarian(self, librarian_id: int):
        updated_librarians = []
        for librarian_info in self.librarians:
            id = librarian_info["id"]
            if id != librarian_id:
                updated_librarians.append(librarian_info)
        if updated_librarians == self.librarians:
            raise NoLibrarianIDError(librarian_id)
        self._librarians = updated_librarians
        write_json('librarians.json', self.librarians)

    def get_books_stats(self):
        if not self.books:
            raise NoBooksError
        stats = ['Title - loans']
        for book_info in self.books:
            book = Book(**book_info)
            stats.append(f'{book.title} - {len(book.loan_history)}')
        return '\n'.join(stats)

    def get_users_stats(self):
        if not self.users:
            raise NoUsersError
        stats = ['Name - loans']
        for user_info in self.users:
            user = User(**user_info)
            stats.append(f'{user.name} - {len(user.borrowing_history)}')
        return '\n'.join(stats)
