from class_library import Library
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
)


def test_create_library():
    library = Library()
    assert library.books == read_json('books.json')
    assert library.users == read_json('users.json')
    assert library.librarians == read_json('librarians.json')


def test_library_add_new_book(monkeypatch):
    def return_id(range1, range2, object=[]): return 1111
    monkeypatch.setattr('generate_id.generate_id', return_id)
    library = Library()
    assert generate_book_id() == 1111
    library.add_new_book('1984', 'George Orwell', 1949, 'Dystopian fiction')
    assert library.books == [{
            "id": 1111,
            "title": '1984',
            "author": 'George Orwell',
            "release_year": 1949,
            "genre": "Dystopian fiction",
            "loan_history": [],
            "current_owner": None,
            "extensions": 0,
            "reservations": []
        }]
    library.remove_book(1111)


def test_library_add_new_book_message(monkeypatch):
    def return_id(range1, range2, object=[]): return 1111
    monkeypatch.setattr('generate_id.generate_id', return_id)
    library = Library()
    assert generate_book_id() == 1111
    msg = library.add_new_book('1984', 'George Orwell', 1949, 'Dystopian')
    assert msg == 'The book (1111) has been successfully added.'
    library.remove_book(1111)


def test_library_remove_book(monkeypatch):
    def return_id(range1, range2, object=[]): return 1111
    monkeypatch.setattr('generate_id.generate_id', return_id)
    library = Library()
    assert generate_book_id() == 1111
    library.add_new_book('1984', 'George Orwell', 1949, 'Dystopian fiction')
    info = library.remove_book(1111)
    assert info == 'The book (1111) has been successfully removed.'
    assert library.books == []


def test_library_remove_missing_book():
    library = Library()
    with pytest.raises(NoBookIDError):
        library.remove_book(1111)


def test_library_remove_borrowed_book():
    book = [{
            "id": 1111,
            "title": '1984',
            "author": 'George Orwell',
            "release_year": 1949,
            "genre": "Dystopian fiction",
            "loan_history": [],
            "current_owner": 1234,
            "extensions": 0,
            "reservations": []
            }]
    write_json('books.json', book)
    library = Library()
    with pytest.raises(BorrowedBookError):
        library.remove_book(1111)
    write_json('books.json', [])


def test_library_add_copy_of_book(monkeypatch):
    def return_id(range1, range2, object=[]): return 1111
    monkeypatch.setattr('generate_id.generate_id', return_id)
    library = Library()
    assert generate_book_id() == 1111
    library.add_new_book('1984', 'George Orwell', 1949, 'Dystopian fiction')
    def return_id2(range1, range2, object=[]): return 2222
    monkeypatch.setattr('generate_id.generate_id', return_id2)
    assert generate_book_id() == 2222
    info = library.add_copy_of_book(1111)
    assert info == 'The copy of book (1111) has been successfully added.'
    assert library.books == [
        {
            "id": 1111,
            "title": '1984',
            "author": 'George Orwell',
            "release_year": 1949,
            "genre": "Dystopian fiction",
            "loan_history": [],
            "current_owner": None,
            "extensions": 0,
            "reservations": []
        },
        {
            "id": 2222,
            "title": '1984',
            "author": 'George Orwell',
            "release_year": 1949,
            "genre": "Dystopian fiction",
            "loan_history": [],
            "current_owner": None,
            "extensions": 0,
            "reservations": []
        }]
    library.remove_book(1111)
    library.remove_book(2222)


def test_library_add_copy_of_missing_book():
    library = Library()
    with pytest.raises(NoBookIDError):
        library.add_copy_of_book(1111)


def test_library_add_user(monkeypatch):
    def return_id(range1, range2, object=[]): return 2222
    monkeypatch.setattr('generate_id.generate_id', return_id)
    library = Library()
    assert generate_user_id() == 2222
    library.add_new_user('Jan Kowalski', 'haslo123')
    assert library.users == [{
            "id": 2222,
            "name": 'Jan Kowalski',
            "password": 'haslo123',
            "borrowed_books": [],
            "borrowing_history": []
        }]
    library.remove_user(2222)


def test_library_remove_user(monkeypatch):
    def return_id(range1, range2, object=[]): return 2222
    monkeypatch.setattr('generate_id.generate_id', return_id)
    library = Library()
    assert generate_user_id() == 2222
    library.add_new_user('Jan Kowalski', 'haslo123')
    library.remove_user(2222)
    assert library.users == []


def test_library_remove_missing_user():
    library = Library()
    with pytest.raises(NoUserIDError):
        library.remove_user(2222)


def test_library_remove_user_with_books():
    user = [{
            "id": 2222,
            "name": 'Jan Kowalski',
            "password": 'haslo123',
            "borrowed_books": [1234],
            "borrowing_history": []
            }]
    write_json('users.json', user)
    library = Library()
    with pytest.raises(UserWithBooksError):
        library.remove_user(2222)
    write_json('users.json', [])


def test_library_search_book_by_keyword(monkeypatch):
    def return_id(range1, range2, object=[]): return 1111
    monkeypatch.setattr('generate_id.generate_id', return_id)
    library = Library()
    assert generate_book_id() == 1111
    library.add_new_book('1984', 'George Orwell', 1949, 'Dystopian fiction')
    result = library.search_book_by_keyword('George')
    assert result == (
                'ID: 1111, ' + 'Title: 1984, Author: George Orwell, ' +
                'Release year: 1949, Genre: Dystopian fiction, ' +
                'Owner: None'
                )
    result = library.search_book_by_keyword(1984)
    assert result == (
                'ID: 1111, ' + 'Title: 1984, Author: George Orwell, ' +
                'Release year: 1949, Genre: Dystopian fiction, ' +
                'Owner: None'
                )
    library.remove_book(1111)


def test_library_search_book_by_missing_keyword():
    library = Library()
    with pytest.raises(NoKeywordError):
        library.search_book_by_keyword('')


def test_library_search_book_by_keyword_not_found(monkeypatch):
    def return_id(range1, range2, object=[]): return 1111
    monkeypatch.setattr('generate_id.generate_id', return_id)
    library = Library()
    assert generate_book_id() == 1111
    library.add_new_book('1984', 'George Orwell', 1949, 'Dystopian fiction')
    with pytest.raises(KeywordNotFoundError):
        library.search_book_by_keyword('harry potter')
    library.remove_book(1111)


def test_library_available_genres():
    library = Library()
    library.add_new_book('1984', 'George Orwell', 1949, 'Dystopian fiction')
    library.add_new_book(
        'The Plague',
        'Albert Camus',
        1947,
        'Philosophical novel'
        )
    assert library.available_genres() == [
        'Dystopian fiction',
        'Philosophical novel'
        ]
    write_json('books.json', [])


def test_library_available_genres_empty():
    library = Library()
    with pytest.raises(GenresNotFoundError):
        library.available_genres()


def test_library_search_by_gerne(monkeypatch):
    library = Library()
    library.add_new_book(
        'The Plague',
        'Albert Camus',
        1947,
        'Philosophical novel'
        )

    def return_id(range1, range2, object=[]): return 1111
    monkeypatch.setattr('generate_id.generate_id', return_id)
    library.add_new_book('1984', 'George Orwell', 1949, 'Dystopian fiction')
    assert library.available_genres() == [
        'Philosophical novel',
        'Dystopian fiction'
        ]
    result = library.search_book_by_genre('Dystopian fiction')
    assert result == (
                'ID: ' + '1111' + ', '
                'Title: 1984, Author: George Orwell, ' +
                'Release year: 1949, Genre: Dystopian fiction, ' +
                'Owner: None'
                )
    write_json('books.json', [])


def test_library_search_by_wrong_genre():
    library = Library()
    library.add_new_book(
        'The Plague',
        'Albert Camus',
        1947,
        'Philosophical novel'
        )
    library.add_new_book('1984', 'George Orwell', 1949, 'Dystopian fiction')
    assert library.available_genres() == [
        'Philosophical novel',
        'Dystopian fiction'
        ]
    with pytest.raises(UnavailableGenreError):
        library.search_book_by_genre('Science fiction')
    write_json('books.json', [])


def test_library_add_librarian(monkeypatch):
    def return_id(range1, range2, object=[]): return 1111
    monkeypatch.setattr('generate_id.generate_id', return_id)
    library = Library()
    assert generate_librarian_id() == 1111
    library.add_new_librarian('Adam Nowak', 'admin123')
    assert library.librarians == [{
            "id": 1111,
            "name": 'Adam Nowak',
            "password": 'admin123',
        }]
    library.remove_librarian(1111)


def test_library_remove_librarian(monkeypatch):
    def return_id(range1, range2, object=[]): return 1111
    monkeypatch.setattr('generate_id.generate_id', return_id)
    library = Library()
    assert generate_librarian_id() == 1111
    library.add_new_librarian('Adam Nowak', 'admin123')
    library.remove_librarian(1111)
    assert library.librarians == []


def test_library_remove_missing_librarian():
    library = Library()
    with pytest.raises(NoLibrarianIDError):
        library.remove_librarian(2222)


def test_library_available_authors():
    library = Library()
    library.add_new_book('1984', 'George Orwell', 1949, 'Dystopian fiction')
    library.add_new_book(
        'The Plague',
        'Albert Camus',
        1947,
        'Philosophical novel'
        )
    assert library.available_authors() == [
        'George Orwell',
        'Albert Camus'
        ]
    write_json('books.json', [])


def test_library_available_authors_empty():
    library = Library()
    with pytest.raises(AuthorsNotFoundError):
        library.available_authors()


def test_library_search_by_author(monkeypatch):
    library = Library()
    library.add_new_book(
        'The Plague',
        'Albert Camus',
        1947,
        'Philosophical novel'
        )

    def return_id(range1, range2, object=[]): return 1111
    monkeypatch.setattr('generate_id.generate_id', return_id)
    library.add_new_book('1984', 'George Orwell', 1949, 'Dystopian fiction')
    assert library.available_authors() == [
        'Albert Camus',
        'George Orwell'
        ]
    result = library.search_book_by_author('George Orwell')
    assert result == (
                'ID: ' + '1111' + ', '
                'Title: 1984, Author: George Orwell, ' +
                'Release year: 1949, Genre: Dystopian fiction, ' +
                'Owner: None'
                )
    write_json('books.json', [])


def test_library_search_by_wrong_author():
    library = Library()
    library.add_new_book(
        'The Plague',
        'Albert Camus',
        1947,
        'Philosophical novel'
        )
    library.add_new_book('1984', 'George Orwell', 1949, 'Dystopian fiction')
    assert library.available_authors() == [
        'Albert Camus',
        'George Orwell'
        ]
    with pytest.raises(UnavailableAuthorError):
        library.search_book_by_author('Henryk Sienkiewicz')
    write_json('books.json', [])
