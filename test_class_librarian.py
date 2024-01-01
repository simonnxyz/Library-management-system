from class_user import Librarian
from generate_id import generate_librarian_id
import pytest
from errors import (
    EmptyNameError,
    ShortPasswordError,
)


def test_generate_librarian_id(monkeypatch):
    def return_id(range1, range2): return 1111
    monkeypatch.setattr('generate_id.randint', return_id)
    id = generate_librarian_id()
    librarian = Librarian(id, 'Adam Nowak', 'admin123')
    assert librarian.id == 1111


def test_librarian():
    id = generate_librarian_id()
    librarian = Librarian(id, 'Adam Nowak', 'admin123')
    assert librarian.id == id
    assert librarian.name == 'Adam Nowak'
    assert librarian.password == 'admin123'


def test_librarian_empty_name():
    with pytest.raises(EmptyNameError):
        Librarian(generate_librarian_id(), '', 'haslo123')


def test_librarian_short_password():
    with pytest.raises(ShortPasswordError):
        Librarian(generate_librarian_id(), 'Adam Nowak', 'admin')


def test_librarian_dict():
    id = generate_librarian_id()
    librarian = Librarian(id, 'Adam Nowak', 'admin123')
    assert librarian.__dict__() == {
            "id": id,
            "name": 'Adam Nowak',
            "password": 'admin123',
        }


def test_librarian_search_info():
    id = generate_librarian_id()
    librarian = Librarian(id, 'Adam Nowak', 'admin123')
    assert librarian.search_info() == (
                'ID: ' + str(id) +
                ', Name: ' + 'Adam Nowak' +
                ', Password: ' + 'admin123')
