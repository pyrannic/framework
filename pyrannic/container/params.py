import inspect
from collections.abc import Callable
from typing import Any, Literal, cast, get_origin

from fastapi.params import Depends

from pyrannic.container.decorators.singleton import singleton
from pyrannic.container.decorators.scoped import scoped
from pyrannic.contracts.http.request import RequestInterface


class Resolves(Depends):
    def __init__(
        self,
        dependency: str | type | Callable[..., Any] | None = None,
        use_cache: bool = True,
        scope: Literal["function", "request"] | None = None,
    ):
        if (
            isinstance(dependency, str)
            or inspect.isclass(dependency)
            or inspect.isclass(get_origin(dependency))
        ):
            dependency = self.wrap_dependency(dependency)  # pyright: ignore[reportArgumentType]

        super().__init__(dependency=dependency, use_cache=use_cache, scope=scope)

    @classmethod
    def wrap_dependency(cls, abstract: str | type) -> Callable[..., Any]:
        async def dependency(request: RequestInterface) -> Any:
            return cast(Any, await request.app.container.resolve(abstract, request))

        return dependency


class Singleton(Resolves):
    def __init__(
        self,
        dependency: str | type | Callable[..., Any] | None = None,
        use_cache: bool = True,
        scope: Literal["function", "request"] | None = None,
    ):
        super().__init__(dependency=dependency, use_cache=use_cache, scope=scope)

    @classmethod
    def wrap_dependency(cls, abstract: str | type) -> Callable[..., Any]:
        if not isinstance(abstract, str):
            abstract = cast(type, singleton(abstract))

        return super().wrap_dependency(abstract)


class Scoped(Resolves):
    def __init__(
        self,
        dependency: str | type | Callable[..., Any] | None = None,
        use_cache: bool = True,
        scope: Literal["function", "request"] | None = None,
    ):
        super().__init__(dependency=dependency, use_cache=use_cache, scope=scope)

    @classmethod
    def wrap_dependency(cls, abstract: str | type) -> Callable[..., Any]:
        if not isinstance(abstract, str):
            abstract = cast(type, scoped(abstract))

        return super().wrap_dependency(abstract)
