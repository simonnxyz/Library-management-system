from class_user import User
from generate_id import generate_user_id
import pytest
from errors import (
    EmptyNameError,
    ShortPasswordError,
)


def test_generate_user_id(monkeypatch):
    def return_id(range1, range2):
        return 2222
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


def test_user_empty_name():
    with pytest.raises(EmptyNameError):
        User(generate_user_id(), '', 'haslo123')


def test_user_short_password():
    with pytest.raises(ShortPasswordError):
        User(generate_user_id(), 'Jan Kowalski', 'haslo')
