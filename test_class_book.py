from class_book import Book
from generate_id import generate_book_id
import pytest
from errors import (
    EmptyTitleError,
    NoAuthorError,
    NoReleaseYearError,
    NoGenreError,
)


def test_generate_book_id(monkeypatch):
    def return_id(range1, range2): return 1111
    monkeypatch.setattr('generate_id.randint', return_id)
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    assert book.id == 1111


def test_book():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    assert book.id == id
    assert book.title == '1984'
    assert book.author == 'George Orwell'
    assert book.release_year == 1949
    assert book.genre == 'Dystopian fiction'
    assert book.loan_history == []
    assert book.current_owner is None
    assert book.extensions == 0
    assert book.reservations == []


def test_book_empty_title():
    with pytest.raises(EmptyTitleError):
        Book(generate_book_id(), '', 'George Orwell', 1949, 'Dystopian f.')


def test_book_no_author():
    with pytest.raises(NoAuthorError):
        Book(generate_book_id(), '1984', '', 1949, 'Dystopian f.')


def test_book_no_release_year():
    with pytest.raises(NoReleaseYearError):
        Book(generate_book_id(), '1984', 'George Orwell', '', 'Dystopian f.')


def test_book_no_genre():
    with pytest.raises(NoGenreError):
        Book(generate_book_id(), '1984', 'George Orwell', 1949, '')


def test_book_set_reservations():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    assert book.extensions == 0
    book.set_extensions(3)
    assert book.extensions == 3


def test_book_dict():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    assert book.__dict__() == {
            "id": id,
            "title": '1984',
            "author": 'George Orwell',
            "release_year": 1949,
            "genre": "Dystopian fiction",
            "loan_history": [],
            "current_owner": None,
            "extensions": 0,
            "reservations": []
        }


def test_book_str():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    assert str(book) == (
                'ID: ' + str(id) + ', '
                'Title: 1984, Author: George Orwell, ' +
                'Release year: 1949, Genre: Dystopian fiction'
                )
