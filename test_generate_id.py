from generate_id import (
    generate_id,
    generate_book_id,
    generate_librarian_id,
    generate_user_id,
)


def test_generate_id(monkeypatch):
    def return_id(range1, range2): return 1111
    monkeypatch.setattr('generate_id.randint', return_id)
    assert generate_id(1000, 10000, []) == 1111


def test_generate_id_wrong(monkeypatch):
    def return_id(range1, range2): return 1111
    monkeypatch.setattr('generate_id.randint', return_id)
    assert not generate_id(1000, 10000, []) == 2222


def test_generate_book_id(monkeypatch):
    def return_id(range1, range2): return 1111
    monkeypatch.setattr('generate_id.randint', return_id)
    assert generate_book_id() == 1111


def test_generate_user_id(monkeypatch):
    def return_id(range1, range2): return 2222
    monkeypatch.setattr('generate_id.randint', return_id)
    assert generate_user_id() == 2222


def test_generate_librarian_id(monkeypatch):
    def return_id(range1, range2): return 1234
    monkeypatch.setattr('generate_id.randint', return_id)
    assert generate_librarian_id() == 1234
