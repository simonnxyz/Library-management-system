from class_user import User
from generate_id import generate_user_id


def test_generate_user_id(monkeypatch):
    def return_id(range1, range2):
        return 2222
    monkeypatch.setattr('generate_id.randint', return_id)
    id = generate_user_id()
    user = User(id, 'Jan Kowalski', 'haslo123')
    assert user.id == 2222
