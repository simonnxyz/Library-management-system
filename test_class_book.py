from class_book import Book
from generate_id import generate_book_id
import pytest
from class_library import Library
from datetime import date, timedelta
from errors import (
    EmptyTitleError,
    NoAuthorError,
    NoReleaseYearError,
    NoGenreError,
    NegativeExtensionsError,
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
    assert book.return_date is None


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
            "reservations": [],
            "return_date": None
        }


def test_book_str():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    assert str(book) == (
                'ID: ' + str(id) + ', '
                'Title: 1984, Author: George Orwell, ' +
                'Release year: 1949, Genre: Dystopian fiction, ' +
                'Owner: None, ' + 'Return date: None'
                )


def test_book_dict_update():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    library = Library()
    library.add_new_book(book)
    book.history_append(1111)
    library.update_data()
    assert library.books == [{
            "id": id,
            "title": '1984',
            "author": 'George Orwell',
            "release_year": 1949,
            "genre": "Dystopian fiction",
            "loan_history": [1111],
            "current_owner": None,
            "extensions": 0,
            "reservations": [],
            "return_date": None
        }]
    library.remove_book(id)


def test_book_set_extensions():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    assert book.extensions == 0
    book.set_extensions(3)
    assert book.extensions == 3


def test_book_set_negative_extensions():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    assert book.extensions == 0
    with pytest.raises(NegativeExtensionsError):
        book.set_extensions(-1)


def test_remove_extension():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    book.set_extensions(3)
    assert book.extensions == 3
    book.remove_extension()
    assert book.extensions == 2


def test_remove_extension_negative():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    assert book.extensions == 0
    with pytest.raises(NegativeExtensionsError):
        book.remove_extension()


def test_book_set_owner():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    assert book.current_owner is None
    book.set_owner(2222)
    assert book.current_owner == 2222


def test_book_add_reservation():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    assert book.reservations == []
    book.add_reservation(2222)
    assert book.reservations == [2222]
    book.add_reservation(3333)
    assert book.reservations == [2222, 3333]


def test_book_remove_reservation():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    assert book.reservations == []
    book.add_reservation(2222)
    assert book.reservations == [2222]
    book.remove_reservation(2222)
    assert book.reservations == []


def test_book_remove_first_reservation():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    book.add_reservation(2222)
    book.add_reservation(3333)
    assert book.reservations == [2222, 3333]
    book.remove_first_reservation()
    assert book.reservations == [3333]


def test_book_history_append():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    assert book.loan_history == []
    book.history_append(2222)
    assert book.loan_history == [2222]


def test_book_set_return_dates_default():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    assert book.return_date is None
    book.set_return_date()
    assert book.return_date == date.today() + timedelta(days=30)


def test_book_set_return_dates_none():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    assert book.return_date is None
    book.set_return_date(None)
    assert book.return_date is None


def test_book_extend_return_date():
    id = generate_book_id()
    book = Book(id, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    book.set_return_date()
    assert book.return_date == date.today() + timedelta(days=30)
    book.extend_return_date()
    assert book.return_date == date.today() + 2 * timedelta(days=30)
