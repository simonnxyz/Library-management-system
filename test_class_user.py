from class_user import User
from class_book import Book
from class_library import Library
from generate_id import generate_user_id, generate_book_id
from json_methods import write_json
import pytest
from datetime import date, timedelta
from errors import (
    EmptyNameError,
    ShortPasswordError,
    UsersBookError,
    BorrowedBookError,
    NoBookIDError,
    NotUsersBookError,
    ReservedBookError,
    NotEnoughExtensionsError,
    NoBookOwnerError,
    NotReservedError,
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
    assert user.reservations == []
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
    user = User(id, 'Jan Kowalski', 'haslo123', borrowing_history=[1234, 5678])
    assert user.borrowing_history == [1234, 5678]
    assert user.get_history() == 'Your history: 1234, 5678'


def test_user_get_hisotry_empty():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
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
            "reservations": [],
            "borrowing_history": []
        }


def test_user_history_append():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    user.history_append(1111)
    assert user.borrowing_history == [1111]


def test_user_history_append_more_books():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    user.history_append(1111)
    user.history_append(2222)
    assert user.borrowing_history == [1111, 2222]


def test_user_borrowed_append():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    user.borrowed_append(1111)
    assert user.borrowed_books == [1111]


def test_user_borrowed_append_more_books():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    user.borrowed_append(1111)
    user.borrowed_append(2222)
    assert user.borrowed_books == [1111, 2222]


def test_user_borrowed_remove():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    user.borrowed_append(1111)
    user.borrowed_remove(1111)
    assert user.borrowing_history == []


def test_user_reservations_append():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    user.reservations_append(1111)
    assert user.reservations == [1111]


def test_user_reservations_append_more_books():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    user.reservations_append(1111)
    user.reservations_append(2222)
    assert user.reservations == [1111, 2222]


def test_user_reservations_remove():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    user.reservations_append(1111)
    user.reservations_remove(1111)
    assert user.reservations == []


def test_user_change_password():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    assert user.password == 'haslo123'
    user.change_password('haslo321')
    assert user.password == 'haslo321'


def test_user_change_password_short():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    assert user.password == 'haslo123'
    with pytest.raises(ShortPasswordError):
        user.change_password('haslo')


def test_user_dict_update():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    library = Library()
    library.add_new_user(user)
    user.history_append(1111)
    library.update_data()
    assert library.users == [user.__dict__()]
    library.remove_user(id)


def test_user_borrow_book():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    id2 = generate_book_id()
    book = Book(id2, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    library = Library()
    library.add_new_user(user)
    library.add_new_book(book)
    user.borrow_book(id2)
    library.update_data()
    return_date = date.today() + timedelta(days=30)
    assert library.books == [{
        "id": id2,
        "title": "1984",
        "author": "George Orwell",
        "release_year": 1949,
        "genre": "Dystopian fiction",
        "loan_history": [id],
        "current_owner": id,
        "extensions": 3,
        "reservations": [],
        "return_date": str(return_date)
    }]
    assert library.users == [user.__dict__()]
    user.return_book(id2)
    library.update_data()
    library.remove_user(id)
    library.remove_book(id2)


def test_user_borrow_own_book():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    id2 = generate_book_id()
    book = Book(id2, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    library = Library()
    library.add_new_user(user)
    library.add_new_book(book)
    user.borrow_book(id2)
    library.update_data()
    with pytest.raises(UsersBookError):
        user.borrow_book(id2)
    user.return_book(id2)
    library.update_data()
    library.remove_user(id)
    library.remove_book(id2)


def test_user_borrow_borrowed_book():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    id2 = generate_user_id()
    user2 = User(id2, 'Adam Nowak', 'haslo123')
    library = Library()
    library.add_new_user(user)
    library.add_new_user(user2)
    id3 = generate_book_id()
    book = Book(id3, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    library.add_new_book(book)
    user.borrow_book(id3)
    with pytest.raises(BorrowedBookError):
        user2.borrow_book(id3)
    user.return_book(id3)
    library.update_data()
    library.remove_user(id)
    library.remove_user(id2)
    library.remove_book(id3)


def test_borrow_book_wrong_id():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    library = Library()
    library.add_new_user(user)
    with pytest.raises(NoBookIDError):
        user.borrow_book(1111)
    library.remove_user(id)


def test_user_use_extension():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    library = Library()
    library.add_new_user(user)
    id2 = generate_book_id()
    book = Book(id2, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    library.add_new_book(book)
    user.borrow_book(id2)
    library.update_data()
    user.use_extension(id2)
    library.update_data()
    return_date = date.today() + 2 * timedelta(days=30)
    assert library.books == [{
        "id": id2,
        "title": "1984",
        "author": "George Orwell",
        "release_year": 1949,
        "genre": "Dystopian fiction",
        "loan_history": [id],
        "current_owner": id,
        "extensions": 2,
        "reservations": [],
        "return_date": str(return_date)
    }]
    write_json('users.json', [])
    write_json('books.json', [])


def test_user_use_extension_not_owned_book():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    library = Library()
    library.add_new_user(user)
    with pytest.raises(NotUsersBookError):
        user.use_extension(1111)
    library.remove_user(id)


def test_user_use_extension_reserved_book():
    id = generate_user_id()
    id2 = generate_book_id()
    user = User(id,
                'Jan Kowalski',
                'haslo123',
                borrowed_books=[id2],
                borrowing_history=[id2])
    library = Library()
    library.add_new_user(user)
    book = Book(id2,
                '1984',
                'George Orwell',
                1949,
                'Dystopian fiction',
                loan_history=[2222],
                current_owner=2222,
                reservations=[3333],
                return_date="2024-04-15")
    library.add_new_book(book)
    library.update_data()
    with pytest.raises(ReservedBookError):
        user.use_extension(id2)
    write_json('users.json', [])
    write_json('books.json', [])


def test_user_use_extension_not_enough(monkeypatch):
    id = generate_user_id()
    id2 = generate_book_id()
    user = User(id,
                'Jan Kowalski',
                'haslo123',
                borrowed_books=[id2],
                borrowing_history=[id2])
    library = Library()
    library.add_new_user(user)
    book = Book(id2,
                '1984',
                'George Orwell',
                1949,
                'Dystopian fiction',
                loan_history=[2222],
                current_owner=2222,
                extensions=0,
                return_date="2024-04-15")
    library.add_new_book(book)
    library.update_data()
    with pytest.raises(NotEnoughExtensionsError):
        user.use_extension(id2)
    write_json('users.json', [])
    write_json('books.json', [])


def test_user_use_extension_wrong_id():
    id = generate_user_id()
    id2 = generate_book_id()
    user = User(id,
                'Jan Kowalski',
                'haslo123',
                borrowed_books=[id2],
                borrowing_history=[id2])
    library = Library()
    library.add_new_user(user)
    with pytest.raises(NoBookIDError):
        user.use_extension(id2)
    write_json('users.json', [])


def test_user_reserve_book():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    id2 = generate_user_id()
    user2 = User(id2, 'Adam Nowak', 'haslo123')
    library = Library()
    library.add_new_user(user)
    library.add_new_user(user2)
    id3 = generate_book_id()
    book = Book(id3, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    library.add_new_book(book)
    user.borrow_book(id3)
    user2.reserve_book(id3)
    library.update_data()
    return_date = date.today() + timedelta(days=30)
    assert library.books == [{
        "id": id3,
        "title": "1984",
        "author": "George Orwell",
        "release_year": 1949,
        "genre": "Dystopian fiction",
        "loan_history": [id],
        "current_owner": id,
        "extensions": 3,
        "reservations": [id2],
        "return_date": str(return_date)
    }]
    write_json('users.json', [])
    write_json('books.json', [])


def test_user_reserve_own_book():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    library = Library()
    library.add_new_user(user)
    id2 = generate_book_id()
    book = Book(id2, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    library.add_new_book(book)
    user.borrow_book(id2)
    with pytest.raises(UsersBookError):
        user.reserve_book(id2)
    write_json('users.json', [])
    write_json('books.json', [])


def test_user_reserve_not_borrowed_book():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    library = Library()
    library.add_new_user(user)
    id2 = generate_book_id()
    book = Book(id2, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    library.add_new_book(book)
    with pytest.raises(NoBookOwnerError):
        user.reserve_book(id2)
    write_json('users.json', [])
    write_json('books.json', [])


def test_user_reserve_book_wrong_id():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    library = Library()
    library.add_new_user(user)
    with pytest.raises(NoBookIDError):
        user.reserve_book(1111)
    write_json('users.json', [])
    write_json('books.json', [])


def test_user_cancel_reservation():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    id2 = generate_user_id()
    user2 = User(id2, 'Adam Nowak', 'haslo123')
    library = Library()
    library.add_new_user(user)
    library.add_new_user(user2)
    id3 = generate_book_id()
    book = Book(id3, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    library.add_new_book(book)
    user.borrow_book(id3)
    user2.reserve_book(id3)
    user2.cancel_reservation(id3)
    library.update_data()
    return_date = date.today() + timedelta(days=30)
    assert library.books == [{
        "id": id3,
        "title": "1984",
        "author": "George Orwell",
        "release_year": 1949,
        "genre": "Dystopian fiction",
        "loan_history": [id],
        "current_owner": id,
        "extensions": 3,
        "reservations": [],
        "return_date": str(return_date)
    }]
    write_json('users.json', [])
    write_json('books.json', [])


def test_user_cancel_missing_reservation():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    library = Library()
    library.add_new_user(user)
    id2 = generate_book_id()
    book = Book(id2, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    library.add_new_book(book)
    with pytest.raises(NotReservedError):
        user.cancel_reservation(id2)
    write_json('users.json', [])
    write_json('books.json', [])


def test_user_cancel_reservation_wrong_id():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    library = Library()
    library.add_new_user(user)
    with pytest.raises(NoBookIDError):
        user.cancel_reservation(1111)
    write_json('users.json', [])
    write_json('books.json', [])


def test_user_return_book():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    id2 = generate_book_id()
    book = Book(id2, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    library = Library()
    library.add_new_user(user)
    library.add_new_book(book)
    user.borrow_book(id2)
    user.return_book(id2)
    library.update_data()
    assert library.books == [{
        "id": id2,
        "title": "1984",
        "author": "George Orwell",
        "release_year": 1949,
        "genre": "Dystopian fiction",
        "loan_history": [id],
        "current_owner": None,
        "extensions": 0,
        "reservations": [],
        "return_date": None
    }]
    assert library.users == [{
        "id": id,
        "name": "Jan Kowalski",
        "password": "haslo123",
        "borrowed_books": [],
        "reservations": [],
        "borrowing_history": [id2]
    }]
    write_json('users.json', [])
    write_json('books.json', [])


def test_user_return_not_borrowed_book():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    library = Library()
    library.add_new_user(user)
    with pytest.raises(NotUsersBookError):
        user.return_book(1111)
    library.remove_user(id)


def test_user_return_missing_book():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    id2 = generate_book_id()
    book = Book(id2, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    library = Library()
    library.add_new_user(user)
    library.add_new_book(book)
    user.borrow_book(id2)
    library.update_data()
    with pytest.raises(NotUsersBookError):
        user.return_book(11111)
    write_json('users.json', [])
    write_json('books.json', [])


def test_user_return_reserved_book():
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    id2 = generate_user_id()
    user2 = User(id2, 'Adam Nowak', 'haslo123')
    library = Library()
    library.add_new_user(user)
    library.add_new_user(user2)
    id3 = generate_book_id()
    book = Book(id3, '1984', 'George Orwell', 1949, 'Dystopian fiction')
    library.add_new_book(book)
    user.borrow_book(id3)
    user2.reserve_book(id3)
    user.return_book(id3)
    library.update_data()
    return_date = date.today() + timedelta(days=30)
    assert library.books == [{
        "id": id3,
        "title": "1984",
        "author": "George Orwell",
        "release_year": 1949,
        "genre": "Dystopian fiction",
        "loan_history": [id, id2],
        "current_owner": id2,
        "extensions": 3,
        "reservations": [],
        "return_date": str(return_date)
    }]
    assert library.users == [{
        "id": id,
        "name": "Jan Kowalski",
        "password": "haslo123",
        "borrowed_books": [],
        "reservations": [],
        "borrowing_history": [id3]
        },
        {
        "id": id2,
        "name": "Adam Nowak",
        "password": "haslo123",
        "borrowed_books": [id3],
        "reservations": [],
        "borrowing_history": [id3]
    }]
    write_json('users.json', [])
    write_json('books.json', [])
