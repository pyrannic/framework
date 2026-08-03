from collections.abc import Callable
from typing import Any, Optional, Self, Sequence, cast

import pyrannic.support.string as string
from pyrannic.auth import UnauthorizedException
from pyrannic.auth.access.response import Response
from pyrannic.contracts import (
    AuthenticatableInterface,
    AuthorizableInterface,
    ContainerInterface,
    GateInterface,
    GuardInterface,
)
from pyrannic.ioc import Resolves
from pyrannic.support.reflection import get_class

_SUFFIXES_TO_REMOVE = ["Model", "Entity", "Schema", "Table"]


class Gate(GateInterface):
    _user: AuthorizableInterface | None = None
    _abilities: dict[str, Any] = {}
    _policies: dict[str, Any] = {}
    _container: ContainerInterface

    def __init__(
        self,
        container: Resolves[ContainerInterface],
        abilities: dict[str, Any] = {},
        policies: dict[str, Any] = {},
        # NOTE: We need to use Any as type-hint here because if we use AuthorizableInterface, it will cause an error in the dependency injection system from FastAPI.
        user: Optional[Any] = None,
    ) -> None:
        self._abilities = abilities
        self._policies = policies
        self._container = container
        self._user = user

    def has(self, *abilities: str | Sequence[str]) -> bool:
        for ability in abilities:
            if ability not in self._abilities:
                return False

        return True

    async def allows(
        self,
        abilities: str | Sequence[str],
        *args: Any,
        **kwargs: Any,
    ) -> bool:
        return await self.check(abilities, *args, **kwargs)

    async def denies(
        self,
        abilities: str | Sequence[str],
        *args: Any,
        **kwargs: Any,
    ) -> bool:
        return not await self.check(abilities, *args, **kwargs)

    async def check(
        self,
        abilities: str | Sequence[str],
        *args: Any,
        **kwargs: Any,
    ) -> bool:
        if isinstance(abilities, str):
            abilities = [abilities]

        for ability in abilities:
            if not (await self._inspect(ability, *args, **kwargs)).allowed:
                return False

        return True

    async def any(
        self,
        abilities: str | Sequence[str],
        *args: Any,
        **kwargs: Any,
    ) -> bool:
        if isinstance(abilities, str):
            abilities = [abilities]

        for ability in abilities:
            if (await self._inspect(ability, *args, **kwargs)).allowed:
                return True

        return False

    async def none(
        self,
        abilities: str | Sequence[str],
        *args: Any,
        **kwargs: Any,
    ) -> bool:
        return not await self.any(abilities, *args, **kwargs)

    async def authorize(
        self,
        ability: str,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        return (await self._inspect(ability, *args, **kwargs)).authorize()

    def for_user(self, user: AuthorizableInterface) -> Self:
        return self.__class__(
            self._container,
            self._abilities,
            self._policies,
            user,
        )

    @property
    def user(self) -> AuthorizableInterface:
        if self._user is None:
            raise UnauthorizedException()

        return self._user

    def define_ability(self, ability: str, callback: Callable[..., bool]) -> Self:
        self._abilities[ability] = callback
        return self

    def define_policy(self, model: type[Any], policy: type[Any]) -> Self:
        self._policies[model.__name__] = policy
        return self

    async def _inspect(self, ability: str, *args: Any, **kwargs: Any) -> Response:
        try:
            result = await self._raw(ability, *args, **kwargs)

            if isinstance(result, Response):
                return result

            return Response.allow() if result else Response.deny()
        except UnauthorizedException as e:
            return Response(False, str(e), None)

    async def _raw(self, ability: str, *args: Any, **kwargs: Any) -> bool | Response:
        return await self._call_auth_callback(self.user, ability, *args, **kwargs)

    async def _call_auth_callback(
        self,
        user: AuthorizableInterface,
        ability: str,
        *args: Any,
        **kwargs: Any,
    ) -> bool:
        callback = await self._resolve_auth_callback(ability, *args)

        if len(args) > 0 and isinstance(args[0], type):
            args = args[1:]

        return callback(user, *args, **kwargs)

    async def _resolve_auth_callback(
        self,
        ability: str,
        *args: Any,
    ) -> Callable[..., bool]:
        callback = await self._resolve_policy_callback_if_possible(ability, *args)

        if callback is None:
            callback = self._resolve_ability_callback_if_possible(ability)

        if callback is None:
            callback = self._default_callback

        return callback

    def _default_callback(self, _: Any) -> bool: ...

    async def _resolve_policy_callback_if_possible(
        self,
        ability: str,
        *args: Any,
    ) -> Callable[..., bool] | None:
        callback = None

        if len(args) > 0:
            policy = await self._get_policy_for(args[0])

            if policy is not None:
                callback = self._resolve_policy_callback(ability, policy)

        return callback

    def _resolve_ability_callback_if_possible(
        self,
        ability: str,
    ) -> Callable[..., bool] | None:
        if ability in self._abilities:
            return self._abilities[ability]

    def _resolve_policy_callback(
        self,
        ability: str,
        policy: object,
    ) -> Callable[..., bool] | None:
        """Resolve the callback for a policy check."""

        method_name = self._format_ability_to_method(ability)

        if callable(getattr(policy, method_name, None)):
            return getattr(policy, method_name)

        return None

    def _format_ability_to_method(self, ability: str) -> str:
        return string.to_snake_case(ability)

    async def _get_policy_for(self, model: type | object | str) -> Any | None:
        if isinstance(model, str):
            model_name = model
        elif isinstance(model, type):
            model_name = model.__name__
        else:
            model_name = type(model).__name__

        for suffix in _SUFFIXES_TO_REMOVE:
            if model_name.endswith(suffix):
                model_name = model_name[: -len(suffix)]
                break

        policy = None

        if model_name in self._policies:
            policy = await self._resolve_policy(self._policies[model_name])

        # TODO - Add support to register policies using decarators.

        if policy is None:
            modules = self._guess_policy_module_paths(model_name)
            for module_path in modules:
                policy = get_class(module_path, class_suffix="Policy")

                if policy is not None:
                    policy = await self._resolve_policy(policy)
                    break

        return policy

    async def _resolve_policy(self, policy: type[Any]) -> Any:
        return await self._container.resolve(policy)

    def _guess_policy_module_paths(self, model_name: str) -> list[str]:
        model_name = string.to_snake_case(model_name)

        return [
            f"app.policies.{model_name}",
            f"app.models.policies.{model_name}",
            f"app.auth.policies.{model_name}",
        ]

    async def __ioc_call__(
        self, guard: Resolves[GuardInterface[AuthenticatableInterface]]
    ) -> None:
        self._user = cast(AuthorizableInterface, guard.maybe_user)
        self._container.instance(GateInterface, self)
