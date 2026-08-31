from abc import abstractmethod


class AuthenticatableInterface:
    @abstractmethod
    def get_auth_identifier_name(self) -> str:
        pass

    @abstractmethod
    def get_auth_identifier(self) -> str:
        pass

    @abstractmethod
    def get_auth_password_name(self) -> str:
        pass

    @abstractmethod
    def get_auth_password(self) -> str:
        pass
