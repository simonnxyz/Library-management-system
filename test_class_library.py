from class_library import Library
from class_book import Book
from class_user import User, Librarian
from json_methods import read_json, write_json
from generate_id import (
    generate_book_id,
    generate_user_id,
    generate_librarian_id
)
import pytest
from errors import (
    NoBookIDError,
    NoUserIDError,
    UserWithBooksError,
    BorrowedBookError,
    NoKeywordError,
    KeywordNotFoundError,
    GenresNotFoundError,
    UnavailableGenreError,
    NoLibrarianIDError,
    UnavailableAuthorError,
    AuthorsNotFoundError,
    YearsNotFoundError,
    UnavailableYearError,
    NoBooksError,
    NoUsersError,
)


def test_create_library():
    library = Library()
    assert library.books == read_json('books.json')
    assert library.users == read_json('users.json')
    assert library.librarians == read_json('librarians.json')


def test_library_add_new_book():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    library = Library()
    library.add_new_book(book)
    assert library.books == [{
            "id": id,
            "title": '1984',
            "author": 'George Orwell',
            "release_year": 1949,
            "genre": "Dystopian fiction",
            "loan_history": [],
            "current_owner": None,
            "extensions": 0,
            "reservations": [],
            "return_date": None
        }]
    library.remove_book(id)


def test_library_add_new_book_message():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    library = Library()
    msg = library.add_new_book(book)
    assert msg == f'The book ({id}) has been successfully added.'
    library.remove_book(id)


def test_library_remove_book():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    library = Library()
    library.add_new_book(book)
    info = library.remove_book(id)
    assert info == f'The book ({id}) has been successfully removed.'
    assert library.books == []


def test_library_remove_missing_book():
    library = Library()
    with pytest.raises(NoBookIDError):
        library.remove_book(1111)


def test_library_remove_borrowed_book():
    id = generate_book_id()
    book = Book(id,
                '1984',
                'George Orwell',
                1949,
                'Dystopian fiction',
                current_owner=2222)
    library = Library()
    library.add_new_book(book)
    with pytest.raises(BorrowedBookError):
        library.remove_book(id)
    write_json('books.json', [])


def test_library_add_copy_of_book():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    library = Library()
    library.add_new_book(book)
    id2 = generate_book_id()
    info = library.add_copy_of_book(id, id2)
    assert info == f'The copy of book ({id}) has been successfully added.'
    assert library.books == [
        {
            "id": id,
            "title": '1984',
            "author": 'George Orwell',
            "release_year": 1949,
            "genre": "Dystopian fiction",
            "loan_history": [],
            "current_owner": None,
            "extensions": 0,
            "reservations": [],
            "return_date": None
        },
        {
            "id": id2,
            "title": '1984',
            "author": 'George Orwell',
            "release_year": 1949,
            "genre": "Dystopian fiction",
            "loan_history": [],
            "current_owner": None,
            "extensions": 0,
            "reservations": [],
            "return_date": None
        }]
    library.remove_book(id)
    library.remove_book(id2)


def test_library_add_copy_of_missing_book():
    library = Library()
    with pytest.raises(NoBookIDError):
        library.add_copy_of_book(1111, 2222)


def test_library_add_user():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    library = Library()
    library.add_new_user(user)
    assert library.users == [{
            "id": id,
            "name": 'Jan Kowalski',
            "password": 'haslo123',
            "borrowed_books": [],
            "reservations": [],
            "borrowing_history": []
        }]
    library.remove_user(id)


def test_library_remove_user():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    library = Library()
    library.add_new_user(user)
    library.remove_user(id)
    assert library.users == []


def test_library_remove_missing_user():
    library = Library()
    with pytest.raises(NoUserIDError):
        library.remove_user(2222)


def test_library_remove_user_with_books():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123', borrowed_books=[1234])
    library = Library()
    library.add_new_user(user)
    with pytest.raises(UserWithBooksError):
        library.remove_user(id)
    write_json('users.json', [])


def test_library_search_book_by_keyword():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    library = Library()
    library.add_new_book(book)
    result = library.search_book_by_keyword('George')
    info = (
            f'ID: {id}, ' + 'Title: 1984, Author: George Orwell, ' +
            'Release year: 1949, Genre: Dystopian fiction, ' +
            'Owner: None, ' + 'Return date: None'
    )
    assert result == info
    result = library.search_book_by_keyword(1984)
    assert result == info
    library.remove_book(id)


def test_library_search_book_by_missing_keyword():
    library = Library()
    with pytest.raises(NoKeywordError):
        library.search_book_by_keyword('')


def test_library_search_book_by_keyword_not_found(monkeypatch):
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    library = Library()
    library.add_new_book(book)
    with pytest.raises(KeywordNotFoundError):
        library.search_book_by_keyword('harry potter')
    library.remove_book(id)


def test_library_available_genres():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    id2 = generate_book_id()
    book2 = Book(id2, 'The Plague', 'A. Camus', 1947, 'Philosophical novel')
    library = Library()
    library.add_new_book(book)
    library.add_new_book(book2)
    assert library.available_genres() == [
        'Dystopian fiction',
        'Philosophical novel'
        ]
    library.remove_book(id)
    library.remove_book(id2)


def test_library_available_genres_empty():
    library = Library()
    with pytest.raises(GenresNotFoundError):
        library.available_genres()


def test_library_search_by_gerne(monkeypatch):
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    id2 = generate_book_id()
    book2 = Book(id2, 'The Plague', 'A. Camus', 1947, 'Philosophical novel')
    library = Library()
    library.add_new_book(book2)
    library.add_new_book(book)
    assert library.available_genres() == [
        'Philosophical novel',
        'Dystopian fiction'
        ]
    result = library.search_book_by_genre('Dystopian fiction')
    assert result == (
                'ID: ' + str(id) + ', '
                'Title: 1984, Author: George Orwell, ' +
                'Release year: 1949, Genre: Dystopian fiction, ' +
                'Owner: None, ' + 'Return date: None'
                )
    library.remove_book(id)
    library.remove_book(id2)


def test_library_search_by_wrong_genre():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    id2 = generate_book_id()
    book2 = Book(id2, 'The Plague', 'A. Camus', 1947, 'Philosophical novel')
    library = Library()
    library.add_new_book(book2)
    library.add_new_book(book)
    assert library.available_genres() == [
        'Philosophical novel',
        'Dystopian fiction'
        ]
    with pytest.raises(UnavailableGenreError):
        library.search_book_by_genre('Science fiction')
    library.remove_book(id)
    library.remove_book(id2)


def test_library_add_librarian(monkeypatch):
    id = generate_librarian_id()
    librarian = Librarian(id, 'Adam Nowak', 'admin123')
    library = Library()
    library.add_new_librarian(librarian)
    assert library.librarians == [{
            "id": id,
            "name": 'Adam Nowak',
            "password": 'admin123',
        }]
    library.remove_librarian(id)


def test_library_remove_librarian(monkeypatch):
    id = generate_librarian_id()
    librarian = Librarian(id, 'Adam Nowak', 'admin123')
    library = Library()
    library.add_new_librarian(librarian)
    library.remove_librarian(id)
    assert library.librarians == []


def test_library_remove_missing_librarian():
    library = Library()
    with pytest.raises(NoLibrarianIDError):
        library.remove_librarian(2222)


def test_library_available_authors():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    id2 = generate_book_id()
    book2 = Book(id2, 'The Plague', 'A. Camus', 1947, 'Philosophical novel')
    library = Library()
    library.add_new_book(book2)
    library.add_new_book(book)
    assert library.available_authors() == [
        'A. Camus',
        'George Orwell'
        ]
    library.remove_book(id)
    library.remove_book(id2)


def test_library_available_authors_empty():
    library = Library()
    with pytest.raises(AuthorsNotFoundError):
        library.available_authors()


def test_library_search_by_author(monkeypatch):
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    id2 = generate_book_id()
    book2 = Book(id2, 'The Plague', 'A. Camus', 1947, 'Philosophical novel')
    library = Library()
    library.add_new_book(book2)
    library.add_new_book(book)
    assert library.available_authors() == [
        'A. Camus',
        'George Orwell'
        ]
    result = library.search_book_by_author('George Orwell')
    assert result == (
                'ID: ' + str(id) + ', '
                'Title: 1984, Author: George Orwell, ' +
                'Release year: 1949, Genre: Dystopian fiction, ' +
                'Owner: None, ' + 'Return date: None'
                )
    library.remove_book(id)
    library.remove_book(id2)


def test_library_search_by_wrong_author():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    id2 = generate_book_id()
    book2 = Book(id2, 'The Plague', 'A. Camus', 1947, 'Philosophical novel')
    library = Library()
    library.add_new_book(book2)
    library.add_new_book(book)
    assert library.available_authors() == [
        'A. Camus',
        'George Orwell'
        ]
    with pytest.raises(UnavailableAuthorError):
        library.search_book_by_author('Henryk Sienkiewicz')
    library.remove_book(id)
    library.remove_book(id2)


def test_library_available_years():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    id2 = generate_book_id()
    book2 = Book(id2, 'The Plague', 'A. Camus', 1947, 'Philosophical novel')
    library = Library()
    library.add_new_book(book2)
    library.add_new_book(book)
    assert library.available_years() == [1947, 1949]
    library.remove_book(id)
    library.remove_book(id2)


def test_library_available_years_empty():
    library = Library()
    with pytest.raises(YearsNotFoundError):
        library.available_years()


def test_library_search_by_year(monkeypatch):
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    id2 = generate_book_id()
    book2 = Book(id2, 'The Plague', 'A. Camus', 1947, 'Philosophical novel')
    library = Library()
    library.add_new_book(book2)
    library.add_new_book(book)
    assert library.available_years() == [1947, 1949]
    result = library.search_book_by_year(1949)
    assert result == (
                'ID: ' + str(id) + ', '
                'Title: 1984, Author: George Orwell, ' +
                'Release year: 1949, Genre: Dystopian fiction, ' +
                'Owner: None, ' + 'Return date: None'
                )
    library.remove_book(id)
    library.remove_book(id2)


def test_library_search_by_wrong_year():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    id2 = generate_book_id()
    book2 = Book(id2, 'The Plague', 'A. Camus', 1947, 'Philosophical novel')
    library = Library()
    library.add_new_book(book2)
    library.add_new_book(book)
    assert library.available_years() == [1947, 1949]
    with pytest.raises(UnavailableYearError):
        library.search_book_by_year(1999)
    library.remove_book(id)
    library.remove_book(id2)


def test_library_get_books_stats():
    id = generate_book_id()
    book = Book(id,
                '1984',
                'George Orwell',
                1949,
                'Dystopian fiction',
                loan_history=[2222, 3333])
    id2 = generate_book_id()
    book2 = Book(
        id2,
        'The Plague',
        'A. Camus', 1947,
        'Philosophical novel',
        loan_history=[4444])
    library = Library()
    library.add_new_book(book2)
    library.add_new_book(book)
    msg = 'Title - loans\n' + 'The Plague - 1\n' + '1984 - 2'
    assert library.get_books_stats() == msg
    library.remove_book(id)
    library.remove_book(id2)


def test_library_get_books_stats_empty():
    library = Library()
    with pytest.raises(NoBooksError):
        library.get_books_stats()


def test_library_get_users_stats():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123', borrowing_history=[1111, 2222])
    id2 = generate_user_id()
    user2 = User(id2, 'Adam Nowak', 'haslo123', borrowing_history=[3333])
    library = Library()
    library.add_new_user(user)
    library.add_new_user(user2)
    msg = 'Name - loans\n' + 'Jan Kowalski - 2\n' + 'Adam Nowak - 1'
    assert library.get_users_stats() == msg
    library.remove_user(id)
    library.remove_user(id2)


def test_library_get_users_stats_empty():
    library = Library()
    with pytest.raises(NoUsersError):
        library.get_users_stats()
