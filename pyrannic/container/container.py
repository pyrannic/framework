import inspect
from collections.abc import Callable
from contextlib import AsyncExitStack
from types import FunctionType
from typing import Any, Awaitable, TypeVar, cast, get_args, get_origin

from fastapi import Request
from fastapi.concurrency import run_in_threadpool
from fastapi.dependencies.models import Dependant
from fastapi.dependencies.utils import (
    SolvedDependency,
    get_dependant,
    solve_dependencies,
)
from fastapi.exceptions import RequestValidationError
from fastapi.types import DependencyCacheKey

from pyrannic.container.contextual_binding_builder import ContextualBindingBuilder
from pyrannic.contracts.application import ApplicationInterface
from pyrannic.contracts.container.container import ContainerInterface
from pyrannic.contracts.container.contextual_binding_builder import (
    ContextualBindingBuilderInterface,
)
from pyrannic.support.reflection import is_interface

T = TypeVar("T")


class Binding:
    def __init__(
        self,
        concrete: Callable[..., Any],
        shared: bool = False,
    ) -> None:
        self.concrete = concrete
        self.shared = shared


class Container(ContainerInterface):
    _app: ApplicationInterface
    """ The application instance """

    _abstracts: dict[str, type]
    """ A mapping of abstract keys to their original types """

    _bindings: dict[str, Binding]
    """ The container's bindings """

    _instances: dict[str, Any]
    """ The container's shared instances """

    _resolved: dict[str, bool]
    """ A dict of the types that have been resolved """

    _aliases: dict[str, str | type]
    """ The registered type aliases """

    _scoped_instances: list[str]
    """ The container's scoped instances """

    _contextual: dict[str, dict[str, Binding]]
    """ The contextual binding map """

    _build_stack: list[str]
    """ The stack of concretions currently being built """

    _dependency_cache: dict[DependencyCacheKey, Any]
    """ The cache for resolved dependencies, used by FastAPI's dependency resolution system """

    def __init__(self, app: ApplicationInterface):
        self._app = app
        self._abstracts = {}
        self._bindings = {}
        self._instances = {}
        self._resolved = {}
        self._scoped_instances = []
        self._aliases = {}
        self._contextual = {}
        self._build_stack = []
        self._dependency_cache = {}

    def _abstract_to_str(self, abstract: str | type) -> str:
        if isinstance(abstract, str):
            return abstract
        else:
            origin = get_origin(abstract)

            # For Generic types, e.g., Repository[Model]
            if origin is not None:
                abstract_name = f"{abstract.__qualname__}[{', '.join(arg.__name__ for arg in get_args(abstract))}]"
                abstract_class = origin
            else:
                abstract_name = abstract.__qualname__
                abstract_class = abstract

            key = f"{abstract_name}:{inspect.getfile(abstract_class)}"
            self._abstracts[key] = abstract

            return key

    def bind(
        self,
        abstract: str | type,
        concrete: type[Any] | Callable[..., Any],
        shared: bool = False,
    ) -> None:
        abstract = self._abstract_to_str(abstract)
        self._drop_stale_instances(abstract)

        if inspect.isclass(concrete):
            concrete = self._get_closure(concrete)

        if not isinstance(concrete, FunctionType):
            raise RequestValidationError(["Concrete must be a class or a callable"])

        self._bindings[abstract] = Binding(concrete, shared)

    def bind_if(
        self,
        abstract: str | type,
        concrete: type[Any] | Callable[..., Any],
        shared: bool = False,
    ) -> None:
        if not self.is_bound(abstract):
            self.bind(abstract, concrete, shared)

    def scoped(
        self,
        abstract: str | type,
        concrete: type[Any] | Callable[..., Any],
    ) -> None:
        self._scoped_instances.append(self._abstract_to_str(abstract))
        self.singleton(abstract, concrete)

    def scoped_if(
        self,
        abstract: str | type,
        concrete: type[Any] | Callable[..., Any],
    ) -> None:
        if not self.is_bound(abstract):
            self.scoped(abstract, concrete)

    def singleton(
        self,
        abstract: str | type,
        concrete: type[Any] | Callable[..., Any],
    ) -> None:
        self.bind(abstract, concrete, True)

    def singleton_if(
        self,
        abstract: str | type,
        concrete: type[Any] | Callable[..., Any],
    ) -> None:
        if not self.is_bound(abstract):
            self.singleton(abstract, concrete)

    def instance(self, abstract: str | type[T], instance: T | None = None) -> T:
        if instance is None:
            abstract = self.get_alias(abstract)
            instance = self._instances.get(abstract)

            if not instance:
                raise ValueError(f"No instance found for {abstract}")

            return instance
        else:
            abstract = self._abstract_to_str(abstract)
            self._drop_stale_instances(abstract)
            self._instances[abstract] = instance

            return instance

    def add_contextual_binding(
        self,
        concrete: type,
        abstract: str | type,
        implementation: type | Callable[..., Any],
    ) -> None:
        abstract_key = self._abstract_to_str(abstract)
        concrete_key = self._abstract_to_str(concrete)

        if concrete_key not in self._contextual:
            self._contextual[concrete_key] = {}

        if inspect.isclass(implementation):
            implementation = self._get_closure(implementation)

        self._contextual[concrete_key][abstract_key] = Binding(implementation)

    def when(self, concrete: type | list[type]) -> ContextualBindingBuilderInterface:
        return ContextualBindingBuilder(self, concrete)

    def is_bound(self, abstract: str | type) -> bool:
        abstract = self._abstract_to_str(abstract)
        return (
            abstract in self._bindings
            or abstract in self._instances
            or self.is_alias(abstract)
        )

    async def make(
        self,
        abstract: str | type[T],
        *args: Any,
        request: Request | None = None,
        **kwargs: Any,
    ) -> T:
        return await self.resolve(abstract, *args, request=request, **kwargs)

    async def resolve(
        self,
        abstract: str | type[T],
        *args: Any,
        request: Request | None = None,
        **kwargs: Any,
    ) -> T:
        binding_key = self.get_alias(abstract)
        concrete = self._get_contextual_concrete(binding_key)
        needs_contextual_build = bool(concrete)

        self._build_stack.append(binding_key)

        try:
            if not concrete and binding_key in self._instances:
                return self._instances[binding_key]

            if not concrete:
                concrete = self._get_concrete(abstract)

            instance = concrete(self._app, request, *args, **kwargs)

            if inspect.isawaitable(instance):
                instance = await instance

            if self.is_shared(abstract):
                self._instances[binding_key] = instance

            return instance
        finally:
            if not needs_contextual_build:
                self._resolved[binding_key] = True
            self._build_stack.pop()

    def is_shared(self, abstract: str | type[T]) -> bool:
        """Determine if a given type is shared."""

        binding_key = self._abstract_to_str(abstract)

        if binding_key in self._instances:
            return True

        if binding_key in self._bindings and self._bindings[binding_key].shared:
            return True

        binding_type = self._get_binding_type(abstract)

        if binding_type == "scoped" and binding_key not in self._scoped_instances:
            self._scoped_instances.append(binding_key)

        return True if binding_type in ("singleton", "scoped") else False

    def _get_binding_type(self, abstract: str | type[T]) -> str | None:
        if isinstance(abstract, str):
            abstract_class = self._abstracts.get(abstract)
        else:
            abstract_class = abstract

        if abstract_class:
            binding_type = getattr(abstract_class, "__pyrannic_binding_type__", None)
        else:
            binding_type = None

        return binding_type

    def _get_contextual_concrete(self, abstract: str) -> Callable[..., Any] | None:
        last_concrete = self._build_stack[-1] if self._build_stack else None

        if last_concrete and last_concrete in self._contextual:
            contextual_bindings = self._contextual[last_concrete]
            if abstract in contextual_bindings:
                return contextual_bindings[abstract].concrete

        return None

    def _get_concrete(self, abstract: str | type[T]) -> Callable[..., Any]:
        concrete: Callable[..., Any]
        binding_key = self._abstract_to_str(abstract)

        if binding_key not in self._bindings:
            if isinstance(abstract, str):
                raise RequestValidationError([f"No binding found for key {abstract}"])
            elif is_interface(abstract):
                raise RequestValidationError(
                    [f"No binding found for interface {abstract.__name__}"]
                )
            else:
                concrete = self._get_closure(abstract)
        else:
            concrete = self._bindings[binding_key].concrete

        return concrete

    async def call(
        self,
        callback: type[T] | Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> T:
        return await self._resolve(callback, self._app, *args, **kwargs)

    def resolved(self, abstract: str | type[T]) -> bool:
        abstract = self.get_alias(abstract)
        return abstract in self._instances or abstract in self._resolved

    def set_alias(self, abstract: str | type, alias: str | type) -> None:
        abstract_key = self._abstract_to_str(abstract)
        alias_key = self._abstract_to_str(alias)

        if alias_key == abstract_key:
            raise ValueError(f"{abstract} cannot be aliased to itself.")

        self._aliases[alias_key] = abstract

    def is_alias(self, alias: str | type) -> bool:
        alias = self._abstract_to_str(alias)
        return alias in self._aliases

    def get_alias(self, abstract: str | type) -> str:
        """Get the alias for an abstract if available"""
        abstract = self._abstract_to_str(abstract)

        return (
            self.get_alias(self._aliases[abstract])
            if self.is_alias(abstract)
            else abstract
        )

    def flush(self) -> None:
        self._abstracts.clear()
        self._bindings.clear()
        self._instances.clear()
        self._aliases.clear()
        self._scoped_instances.clear()
        self._dependency_cache.clear()

    def forget_scoped_instances(self) -> None:
        """Clear all of the scoped instances from the container."""
        for abstract in self._scoped_instances:
            if abstract in self._instances:
                del self._instances[abstract]

    def _drop_stale_instances(self, abstract: str) -> None:
        """Drop all of the stale instances and aliases."""
        if abstract in self._instances:
            del self._instances[abstract]

        if abstract in self._bindings:
            del self._bindings[abstract]

        if abstract in self._aliases:
            del self._aliases[abstract]

    def _get_closure(
        self,
        concrete: type[T],
    ) -> Callable[[ApplicationInterface, Request], Awaitable[T]]:
        async def closure(
            app: ApplicationInterface,
            request: Request,
            *args: Any,
            **kwargs: Any,
        ) -> T:
            origin = get_origin(concrete)

            if origin is not None and inspect.isclass(origin):
                return await self._resolve_generic(
                    concrete,
                    origin,
                    app,
                    request,
                    *args,
                    **kwargs,
                )

            return await self._resolve(concrete, app, request, *args, **kwargs)

        return closure

    async def _solve_dependencies(
        self,
        request: Request,
        dependant: Dependant,
    ) -> SolvedDependency:
        return await solve_dependencies(
            request=request,
            dependant=dependant,
            embed_body_fields=False,
            dependency_cache=self._dependency_cache,
            # TODO: Remove async_exit_stack, no longer used.
            async_exit_stack=cast(AsyncExitStack, None),
        )

    async def _resolve_generic(
        self,
        generic: Any,
        origin: type[T],
        app: ApplicationInterface,
        request: Request | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> T:
        # Add the __orig_class__ attribute to the origin class so that we can retrieve the generic type later.
        # For example, if we have a generic class Repository[Model], we can retrieve the Model type later by accessing the __orig_class__ attribute.
        # This is necessary because FastAPI's dependency injection system does not support generic types out of the box.
        setattr(origin, "__orig_class__", generic)
        instance = await self._resolve(origin, app, request, *args, **kwargs)

        try:
            setattr(instance, "__orig_class__", generic)
        except Exception:  # pragma: no cover
            pass

        return instance

    async def _resolve(
        self,
        callback: type[T] | Callable[..., Any],
        app: ApplicationInterface,
        request: Request | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> T:
        dependant = get_dependant(path="/", call=callback, scope="function")

        if not request:
            async with AsyncExitStack() as context_manager:
                request = self._fallback_request(app, context_manager)
                dependencies = await self._solve_dependencies(request, dependant)

                return await self._resolve_dependant(
                    dependant,
                    dependencies,
                    *args,
                    **kwargs,
                )
        else:
            dependencies = await self._solve_dependencies(request, dependant)

            return await self._resolve_dependant(
                dependant,
                dependencies,
                *args,
                **kwargs,
            )

    # https://stackoverflow.com/a/78279023
    # https://github.com/fastapi/fastapi/discussions/7720
    async def _resolve_dependant(
        self,
        dependant: Dependant,
        dependencies: SolvedDependency,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        assert dependant.call  # For types

        errors = self._validate_errors(dependencies.errors, *args, **kwargs)

        if bool(errors):
            raise RequestValidationError(errors)

        if inspect.iscoroutinefunction(dependant.call):
            result = await dependant.call(*args, **dependencies.values, **kwargs)
        else:
            result = await run_in_threadpool(
                dependant.call,
                *args,
                **dependencies.values,
                **kwargs,
            )

        return result

    def _validate_errors(
        self,
        errors: list[Any],
        *args: Any,
        **kwargs: Any,
    ) -> list[Any]:
        if not bool(errors):
            return []

        error_counter = 0
        valid_errors: list[Any] = []
        length = len(args)

        for error in errors:
            loc = error.get("loc", [])
            attr = loc[-1] if loc else None

            if (
                attr != "kwargs"
                and attr != "args"
                and attr not in kwargs
                and length <= error_counter
            ):
                valid_errors.append(error)
                error_counter += 1

        return valid_errors

    def _fallback_request(
        self, app: ApplicationInterface, context_manager: AsyncExitStack
    ) -> Request:
        """Generate a fallback request to be used when no request is available in the context of resolution."""
        return Request(
            {
                "app": app,
                "type": "http",
                "method": "GET",
                "path": "/",
                "headers": [],
                "query_string": b"",
                "fastapi_inner_astack": context_manager,
                "fastapi_function_astack": context_manager,
            }
        )
