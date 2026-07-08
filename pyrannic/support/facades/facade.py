from abc import update_abstractmethods
import inspect
from typing import Any, TypeVar, cast

from pyrannic.contracts.application import ApplicationInterface
from pyrannic.support.string import to_snake_case

T = TypeVar("T")


class Facade:
    _app: ApplicationInterface | None = None
    """The application instance being facaded."""

    def _call(self, name: str, *args: Any, **kwargs: Any) -> Any:
        instance = self._get_facade_root()
        return getattr(instance, name)(*args, **kwargs)

    def _property(self, name: str) -> Any:
        instance = self._get_facade_root()
        return getattr(instance, name)

    def _get_facade_root(self) -> Any:
        return self._resolve_facade_instance(self.facade_accessor)

    @property
    def facade_accessor(self) -> str:
        """Get the registered name of the component in the IoC container that this facade represents."""
        return to_snake_case(self.__class__.__name__)

    def _resolve_facade_instance(self, name: str) -> Any:
        return self.get_facade_application().container.instance(name)  # type: ignore

    @classmethod
    def set_facade_application(cls, app: ApplicationInterface) -> None:
        """Set the application instance."""
        cls._app = app

    @classmethod
    def get_facade_application(cls) -> ApplicationInterface:
        """Get the application instance behind the facade."""
        assert cls._app is not None, "Facade application instance has not been set."
        return cls._app


def facade(accessor_or_cls: type[T] | str) -> T:
    is_facade_accessor = isinstance(accessor_or_cls, str)

    def decorator(cls: type[T]) -> T:
        interface = cls.__mro__[0]

        if Facade not in cls.__mro__:
            cls = cast(type[T], type(cls.__name__, (Facade,) + cls.__mro__, {}))

        methods = inspect.getmembers(interface, predicate=inspect.isfunction)
        properties = inspect.getmembers(interface, predicate=inspect.isdatadescriptor)

        for name, attr in methods:
            if getattr(attr, "__isabstractmethod__", False):
                setattr(
                    cls,
                    name,
                    lambda self, *args, n=name, **kwargs: self._call(  # pyright: ignore[reportUnknownMemberType, reportUnknownLambdaType]
                        n,
                        *args,
                        **kwargs,
                    ),
                )

        for name, attr in properties:
            if getattr(attr, "__isabstractmethod__", False):
                setattr(cls, name, property(lambda self, n=name: self._property(n)))

        if is_facade_accessor:
            setattr(cls, "facade_accessor", property(lambda _: accessor_or_cls))

        update_abstractmethods(cls)

        return cls()

    return decorator if is_facade_accessor else decorator(accessor_or_cls)  # pyright: ignore[reportReturnType]
