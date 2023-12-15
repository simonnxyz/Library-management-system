from class_library import Library
from json_methods import read_json, write_json
from generate_id import generate_book_id
import pytest
from errors import NoBookIDError


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
    info = library.add_new_book(
        '1984',
        'George Orwell',
        1949,
        'Dystopian fiction'
        )
    assert info == 'The book (1111) has been successfully added.'
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
    write_json('books.json', [])


def test_library_remove_book(monkeypatch):
    def return_id(range1, range2, object=[]): return 1111
    monkeypatch.setattr('generate_id.generate_id', return_id)
    library = Library()
    assert generate_book_id() == 1111
    library.add_new_book('1984', 'George Orwell', 1949, 'Dystopian fiction')
    info = library.remove_book(1111)
    assert info == 'The book (1111) has been successfully removed.'
    assert library.books == []


def test_remove_missing_book():
    library = Library()
    with pytest.raises(NoBookIDError):
        library.remove_book(1111)


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


def test_add_copy_of_missing_book():
    library = Library()
    with pytest.raises(NoBookIDError):
        library.add_copy_of_book(1111)
