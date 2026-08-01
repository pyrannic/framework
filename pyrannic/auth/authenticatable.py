from pyrannic.contracts.auth import AuthenticatableInterface


class Authenticatable(AuthenticatableInterface):
    """
    A base class for authenticatable entities.
    """

    def get_auth_identifier_name(self) -> str:
        return "id"

    def get_auth_identifier(self) -> str:
        return str(getattr(self, self.get_auth_identifier_name()))

    def get_auth_password_name(self) -> str:
        return "password"

    def get_auth_password(self) -> str:
        return str(getattr(self, self.get_auth_password_name()))
