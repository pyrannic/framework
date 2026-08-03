from tests.unit.auth.conftest import User


def test_authenticatable_methods():
    user = User(id=1, password="secret")

    assert user.get_auth_identifier_name() == "id"
    assert user.get_auth_identifier() == "1"
    assert user.get_auth_password_name() == "password"
    assert user.get_auth_password() == "secret"
