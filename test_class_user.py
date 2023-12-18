from class_user import User
from class_book import Book
from class_library import Library
from generate_id import generate_user_id
from json_methods import read_json, write_json
import pytest
from errors import (
    EmptyNameError,
    ShortPasswordError,
    UsersBookError,
    BorrowedBookError,
    NoBookIDError,
    NotUsersBookError,
    ReservedBookError,
    NotEnoughExtensionsError,
)


def test_generate_user_id(monkeypatch):
    def return_id(range1, range2): return 2222
    monkeypatch.setattr('generate_id.randint', return_id)
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    assert user.id == 2222


def test_user():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    assert user.id == id
    assert user.name == 'Jan Kowalski'
    assert user.password == 'haslo123'
    assert user.borrowed_books == []
    assert user.borrowing_history == []


def test_user_empty_name():
    with pytest.raises(EmptyNameError):
        User(generate_user_id(), '', 'haslo123')


def test_user_short_password():
    with pytest.raises(ShortPasswordError):
        User(generate_user_id(), 'Jan Kowalski', 'haslo')


def test_user_get_borrowed_books():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123', [1234, 5678])
    assert user.borrowed_books == [1234, 5678]
    assert user.get_borrowed_books() == 'You have borrowed: 1234, 5678'


def test_user_get_borrowed_books_empty():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    assert user.borrowed_books == []
    info = 'You do not have any books at the moment.'
    assert user.get_borrowed_books() == info


def test_user_get_hisotry():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123', [], [1234, 5678])
    assert user.borrowing_history == [1234, 5678]
    assert user.get_history() == 'Your history: 1234, 5678'


def test_user_get_hisotry_empty():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123', [], [])
    assert user.borrowing_history == []
    assert user.get_history() == 'You have not borrowed any books yet.'


def test_user_login_info():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    info = f'Welcome to our library, Jan Kowalski! Your ID is {id}'
    assert str(user) == info


def test_user_dict():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    assert user.__dict__() == {
            "id": id,
            "name": 'Jan Kowalski',
            "password": 'haslo123',
            "borrowed_books": [],
            "borrowing_history": []
        }


def test_user_borrow_book(monkeypatch):
    library = Library()
    def return_id(range1, range2, object=[]): return 2222
    monkeypatch.setattr('generate_id.generate_id', return_id)
    library.add_new_user('Jan Kowalski', 'haslo123')
    def return_id2(range1, range2, object=[]): return 1111
    monkeypatch.setattr('generate_id.generate_id', return_id2)
    library.add_new_book('1984', 'George Orwell', 1949, 'Dystopian fiction')
    users = read_json('users.json')
    for user_info in users:
        if user_info["id"] == 2222:
            user = User(**user_info)
    user.borrow_book(1111)
    books = read_json('books.json')
    for book_info in books:
        if book_info["id"] == 1111:
            book = Book(**book_info)
    library.update_data()
    assert library.books == [{
        "id": 1111,
        "title": "1984",
        "author": "George Orwell",
        "release_year": 1949,
        "genre": "Dystopian fiction",
        "loan_history": [2222],
        "current_owner": 2222,
        "extensions": 3,
        "reservations": [],
        "return_date": str(book.return_date)
    }]
    assert library.users == [{
        "id": 2222,
        "name": "Jan Kowalski",
        "password": "haslo123",
        "borrowed_books": [1111],
        "borrowing_history": [1111]
    }]
    write_json('users.json', [])
    write_json('books.json', [])


def test_user_borrow_own_book(monkeypatch):
    library = Library()
    def return_id(range1, range2, object=[]): return 2222
    monkeypatch.setattr('generate_id.generate_id', return_id)
    library.add_new_user('Jan Kowalski', 'haslo123')
    def return_id2(range1, range2, object=[]): return 1111
    monkeypatch.setattr('generate_id.generate_id', return_id2)
    library.add_new_book('1984', 'George Orwell', 1949, 'Dystopian fiction')
    users = read_json('users.json')
    for user_info in users:
        if user_info["id"] == 2222:
            user = User(**user_info)
    user.borrow_book(1111)
    with pytest.raises(UsersBookError):
        user.borrow_book(1111)
    write_json('users.json', [])
    write_json('books.json', [])


def test_user_borrow_borrowed_book(monkeypatch):
    library = Library()
    def return_id(range1, range2, object=[]): return 2222
    monkeypatch.setattr('generate_id.generate_id', return_id)
    library.add_new_user('Jan Kowalski', 'haslo123')
    def return_id2(range1, range2, object=[]): return 3333
    monkeypatch.setattr('generate_id.generate_id', return_id2)
    library.add_new_user('Adam Nowak', 'haslo321')
    def return_id3(range1, range2, object=[]): return 1111
    monkeypatch.setattr('generate_id.generate_id', return_id3)
    library.add_new_book('1984', 'George Orwell', 1949, 'Dystopian fiction')
    users = read_json('users.json')
    for user_info in users:
        if user_info["id"] == 2222:
            user1 = User(**user_info)
        elif user_info["id"] == 3333:
            user2 = User(**user_info)
    user1.borrow_book(1111)
    with pytest.raises(BorrowedBookError):
        user2.borrow_book(1111)
    write_json('users.json', [])
    write_json('books.json', [])


def test_borrow_book_wrong_id(monkeypatch):
    library = Library()
    def return_id(range1, range2, object=[]): return 2222
    monkeypatch.setattr('generate_id.generate_id', return_id)
    library.add_new_user('Jan Kowalski', 'haslo123')
    users = read_json('users.json')
    for user_info in users:
        if user_info["id"] == 2222:
            user = User(**user_info)
    with pytest.raises(NoBookIDError):
        user.borrow_book(1111)
    write_json('users.json', [])


def test_user_use_extension(monkeypatch):
    library = Library()
    def return_id(range1, range2, object=[]): return 2222
    monkeypatch.setattr('generate_id.generate_id', return_id)
    library.add_new_user('Jan Kowalski', 'haslo123')
    def return_id2(range1, range2, object=[]): return 1111
    monkeypatch.setattr('generate_id.generate_id', return_id2)
    library.add_new_book('1984', 'George Orwell', 1949, 'Dystopian fiction')
    users = read_json('users.json')
    for user_info in users:
        if user_info["id"] == 2222:
            user = User(**user_info)
    user.borrow_book(1111)
    library.update_data()
    user.use_extension(1111)
    library.update_data()
    books = read_json('books.json')
    for book_info in books:
        if book_info["id"] == 1111:
            book = Book(**book_info)
    library.update_data()
    assert library.books == [{
        "id": 1111,
        "title": "1984",
        "author": "George Orwell",
        "release_year": 1949,
        "genre": "Dystopian fiction",
        "loan_history": [2222],
        "current_owner": 2222,
        "extensions": 2,
        "reservations": [],
        "return_date": str(book.return_date)
    }]
    write_json('users.json', [])
    write_json('books.json', [])


def test_user_use_extension_not_owned_book(monkeypatch):
    library = Library()
    def return_id(range1, range2, object=[]): return 2222
    monkeypatch.setattr('generate_id.generate_id', return_id)
    library.add_new_user('Jan Kowalski', 'haslo123')
    users = read_json('users.json')
    for user_info in users:
        if user_info["id"] == 2222:
            user = User(**user_info)
    with pytest.raises(NotUsersBookError):
        user.use_extension(1111)
    write_json('users.json', [])


def test_user_use_extension_reserved_book():
    library = Library()
    user_info = {
        "id": 2222,
        "name": "Jan Kowalski",
        "password": "haslo123",
        "borrowed_books": [1111],
        "borrowing_history": [1111]
    }
    write_json('users.json', [user_info])
    book = {
        "id": 1111,
        "title": "1984",
        "author": "George Orwell",
        "release_year": 1949,
        "genre": "Dystopian fiction",
        "loan_history": [2222],
        "current_owner": 2222,
        "extensions": 3,
        "reservations": [3333],
        "return_date": "2024-04-15"
    }
    write_json('books.json', [book])
    library.update_data()
    user = User(**user_info)
    with pytest.raises(ReservedBookError):
        user.use_extension(1111)
    write_json('users.json', [])
    write_json('books.json', [])


def test_user_use_extension_not_enough(monkeypatch):
    library = Library()
    user_info = {
        "id": 2222,
        "name": "Jan Kowalski",
        "password": "haslo123",
        "borrowed_books": [1111],
        "borrowing_history": [1111]
    }
    write_json('users.json', [user_info])
    book = {
        "id": 1111,
        "title": "1984",
        "author": "George Orwell",
        "release_year": 1949,
        "genre": "Dystopian fiction",
        "loan_history": [2222],
        "current_owner": 2222,
        "extensions": 0,
        "reservations": [],
        "return_date": "2024-04-15"
    }
    write_json('books.json', [book])
    library.update_data()
    user = User(**user_info)
    with pytest.raises(NotEnoughExtensionsError):
        user.use_extension(1111)
    write_json('users.json', [])
    write_json('books.json', [])


def test_user_use_extension_wrong_id():
    library = Library()
    user_info = {
        "id": 2222,
        "name": "Jan Kowalski",
        "password": "haslo123",
        "borrowed_books": [1111],
        "borrowing_history": [1111]
    }
    write_json('users.json', [user_info])
    library.update_data()
    user = User(**user_info)
    with pytest.raises(NoBookIDError):
        user.use_extension(1111)
    write_json('users.json', [])
