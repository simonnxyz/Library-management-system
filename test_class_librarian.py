from class_user import Librarian
from generate_id import generate_librarian_id


def test_generate_user_id(monkeypatch):
    def return_id(range1, range2):
        return 1111
    monkeypatch.setattr('generate_id.randint', return_id)
    id = generate_librarian_id()
    librarian = Librarian(id, 'Jan Kowalski', 'haslo123')
    assert librarian.id == 1111
