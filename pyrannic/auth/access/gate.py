import inspect
from collections.abc import Callable
from types import CoroutineType
from typing import Any, Optional, Self, Sequence, cast

import pyrannic.support.string as string
from pyrannic.auth import UnauthorizedException
from pyrannic.auth.access.response import Response
from pyrannic.contracts import (
    AuthorizableInterface,
    ContainerInterface,
    GateInterface,
)
from pyrannic.ioc import Resolves
from pyrannic.orm.abstract_model import COMMON_SUFFIXES_TO_REMOVE
from pyrannic.support.collections import li
from pyrannic.support.reflection import get_class


class Gate(GateInterface):
    _user: AuthorizableInterface | None = None
    _abilities: dict[str, Any] = {}
    _policies: dict[str, Any] = {}
    _container: ContainerInterface
    _guess_policy_names_callback: Callable[[str], str | list[str]] | None = None

    def __init__(
        self,
        container: Resolves[ContainerInterface],
        abilities: dict[str, Any] | None = None,
        policies: dict[str, Any] | None = None,
        # NOTE: We need to use Any as type-hint here because if we use AuthorizableInterface, it will cause an error in the dependency injection system from FastAPI.
        user: Optional[Any] = None,
        guess_policy_names_callback: Callable[[str], str | list[str]] | None = None,
    ) -> None:
        self._abilities = abilities or {}
        self._user = user
        self._policies = policies or {}
        self._container = container
        self._guess_policy_names_callback = guess_policy_names_callback

    def has(self, *abilities: str) -> bool:
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
            self._guess_policy_names_callback,
        )

    def set_user(self, user: AuthorizableInterface | None) -> Self:
        self._user = user
        return self

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
        return await self._call_auth_callback(ability, self.user, *args, **kwargs)

    async def _call_auth_callback(
        self,
        ability: str,
        user: AuthorizableInterface,
        *args: Any,
        **kwargs: Any,
    ) -> bool | Response:
        callback = await self._resolve_auth_callback(ability, *args)

        if len(args) > 0 and (isinstance(args[0], type) or isinstance(args[0], str)):
            args = args[1:]

        result = callback(user, *args, **kwargs)

        if inspect.isawaitable(result):
            result = await result

        return result

    async def _resolve_auth_callback(
        self,
        ability: str,
        *args: Any,
    ) -> Callable[..., CoroutineType[Any, Any, bool | Response] | bool | Response]:
        callback = await self._resolve_policy_callback_if_possible(ability, *args)

        if callback is None:
            callback = self._resolve_ability_callback_if_possible(ability)

        if callback is None:
            callback = self._default_callback

        return callback

    def _default_callback(self, *_: Any) -> bool:
        return False

    async def _resolve_policy_callback_if_possible(
        self,
        ability: str,
        *args: Any,
    ) -> Callable[..., CoroutineType[Any, Any, bool | Response]] | None:
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
        return self._abilities[ability] if ability in self._abilities else None

    def _resolve_policy_callback(
        self,
        ability: str,
        policy: object,
    ) -> Callable[..., CoroutineType[Any, Any, bool | Response]] | None:
        """Resolve the callback for a policy check."""

        method_name = self._format_ability_to_method(ability)
        callback: Callable[..., bool | Response] | None = getattr(
            policy, method_name, None
        )

        if callback is not None and callable(callback):

            async def resolve_callback(
                user: AuthorizableInterface, *args: Any, **kwargs: Any
            ) -> bool | Response:
                result = await self._call_policy_before(
                    policy, ability, user, *args, **kwargs
                )

                if result is not None:
                    return result

                result = callback(user, *args, **kwargs)

                if inspect.isawaitable(result):
                    result = await result

                return result

            return resolve_callback

        return None

    async def _call_policy_before(
        self,
        policy: object,
        ability: str,
        user: AuthorizableInterface,
        *args: Any,
        **kwargs: Any,
    ) -> bool | Response | None:
        before_method = getattr(policy, "before", None)

        if before_method is not None and callable(before_method):
            result = before_method(ability, user, *args, **kwargs)

            if inspect.isawaitable(result):
                result = await result

            return cast(bool | Response | None, result)

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

        for suffix in COMMON_SUFFIXES_TO_REMOVE:
            if model_name.endswith(suffix):
                model_name = model_name[: -len(suffix)]
                break

        policy = None

        if model_name in self._policies:
            policy = await self._resolve_policy(self._policies[model_name])

        if policy is None:
            names = self._guess_policy_names(model_name)

            for name in names:
                module_name, class_name = string.parse_module_class(name)
                policy = get_class(module_name, class_name=class_name)

                if policy is not None:
                    policy = await self._resolve_policy(policy)
                    break

        return policy

    async def _resolve_policy(self, policy: type[Any]) -> Any:
        return await self._container.resolve(policy)

    def _guess_policy_names(self, model_name: str) -> list[str]:
        if self._guess_policy_names_callback is not None:
            return li.wrap(self._guess_policy_names_callback(model_name))
        else:
            module_name = string.to_snake_case(model_name)
            model_name = string.to_pascal_case(model_name) + "Policy"

            return [
                f"app.policies.{module_name}.{model_name}",
                f"app.models.policies.{module_name}.{model_name}",
                f"app.auth.policies.{module_name}.{model_name}",
            ]

    def guess_policy_names_using(
        self,
        callback: Callable[[str], str | list[str]],
    ) -> Self:
        self._guess_policy_names_callback = callback
        return self
