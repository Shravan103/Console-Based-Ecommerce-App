from model.admin import Admin
from model.regular_user import RegularUser
from service.user_service import UserService
from exceptions.invalid_credentials_exception import InvalidCredentialsException


def test_regular_user_role():
    user = RegularUser(
        name="Test User",
        email="test@example.com",
        password="test123"
    )

    assert user.get_role() == "REGULAR_USER"


def test_admin_role():
    admin = Admin(
        name="Admin",
        email="admin@example.com",
        password="admin123"
    )

    assert admin.get_role() == "ADMIN"


def test_register_user_creates_regular_user(monkeypatch):
    service = UserService()

    class FakeDAO:
        def get_user_by_email(self, email):
            return None

        def add_user(self, user):
            user.user_id = 1
            return user

    service.user_dao = FakeDAO()

    user = service.register_user(
        "Test User",
        "test@example.com",
        "test123"
    )

    assert isinstance(user, RegularUser)
    assert user.get_role() == "REGULAR_USER"


def test_invalid_login(monkeypatch):
    service = UserService()

    class FakeDAO:
        def get_user_by_email(self, email):
            return None

    service.user_dao = FakeDAO()

    try:
        service.login_user(
            "wrong@example.com",
            "wrong"
        )
        assert False
    except InvalidCredentialsException:
        assert True
