from class_library import Library
from json_methods import read_json, write_json
from generate_id import generate_book_id, generate_user_id
import pytest
from errors import (
    NoBookIDError,
    NoUserIDError,
    UserWithBooksError,
    BorrowedBookError,
    NoKeywordError,
    KeywordNotFoundError,
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
    msg = library.add_new_book( '1984', 'George Orwell', 1949, 'Dystopian')
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
                'Release year: 1949, Genre: Dystopian fiction'
                )
    result = library.search_book_by_keyword(1984)
    assert result == (
                'ID: 1111, ' + 'Title: 1984, Author: George Orwell, ' +
                'Release year: 1949, Genre: Dystopian fiction'
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
