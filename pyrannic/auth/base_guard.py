from typing import Any, Self

from pyrannic.contracts import (
    AuthenticatableInterface,
    GuardInterface,
    UserProviderInterface,
)


class BaseGuard(GuardInterface[AuthenticatableInterface]):
    _user: AuthenticatableInterface | None = None
    _provider: UserProviderInterface | None = None

    @property
    def check(self) -> bool:
        return self._user is not None

    @property
    def is_guest(self) -> bool:
        return self._user is None

    @property
    def user(self) -> AuthenticatableInterface:
        if self._user is None:
            raise ValueError("No user is currently authenticated")

        return self._user

    @property
    def maybe_user(self) -> AuthenticatableInterface | None:
        return self._user

    @property
    def id(self) -> str:
        return self.user.get_auth_identifier()

    @property
    def maybe_id(self) -> str | None:
        return self._user.get_auth_identifier() if self._user else None

    def validate(self, credentials: dict[str, Any]) -> bool:
        return False

    @property
    def has_user(self) -> bool:
        return self._user is not None

    def set_user(self, user: AuthenticatableInterface) -> Self:
        self._user = user
        return self

    def set_provider(self, provider: UserProviderInterface) -> Self:
        self._provider = provider
        return self

    @property
    def provider(self) -> UserProviderInterface:
        if self._provider is None:
            raise ValueError("Provider has not been set")

        return self._provider
