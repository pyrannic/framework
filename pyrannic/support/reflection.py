from abc import ABC
from collections.abc import Callable
import importlib
from inspect import getmembers, isclass, isabstract, isfunction
from types import ModuleType, UnionType, get_original_bases
from typing import Any, Union, get_origin, get_type_hints

from pydantic._internal._generics import get_args

from pyrannic.support.string import to_pascal_case


def is_optional(cls: type, property: str) -> bool:
    """
    Check if a property is optional in a class.
    If the property is not defined, we consider it optional by default.
    """

    property_hints = get_type_hints(cls).get(property, None)

    # If the property is not defined, we consider it optional by default.
    if property_hints is None:
        return True

    origin = get_origin(property_hints)
    is_optional = False

    if origin is Union or origin is UnionType:
        is_optional = type(None) in get_args(property_hints)

    return is_optional


def is_interface(cls: object) -> bool:
    """Check if a class is an interface."""
    if isclass(cls) and ABC in cls.__bases__:
        return True

    return isabstract(cls)


def get_generic_type(instance_or_class: object | type, generic_index: int = 0) -> type:
    """Get the generic type of a class or instance."""

    # Check if instance_or_class has the __orig_class__ attribute, which it is the generic type that we are searching.
    # Check container.py, _resolve_generic method, for more context.
    if hasattr(instance_or_class, "__orig_class__"):
        instance_or_class = getattr(instance_or_class, "__orig_class__")
    else:
        if not isclass(instance_or_class):
            instance_or_class = type(instance_or_class)

        classes = get_original_bases(instance_or_class)
        instance_or_class = classes[generic_index]

    args = get_args(instance_or_class)
    size = len(args)

    if size == 0:
        raise ValueError(
            f"Generic type not found for {instance_or_class.__class__.__name__} at index {generic_index}"  # pyright: ignore[reportUnknownMemberType]
        )

    return args[0]


def get_functions(
    module: ModuleType,
    predicate: Callable[[str], bool] | None = None,
) -> list[tuple[str, Any]]:
    """Returns a list of functions in a given module that match the specified predicate."""
    return getmembers(
        module,
        lambda member: (
            isfunction(member) and (predicate(member.__name__) if predicate else True)
        ),
    )


def get_class(
    module: str | ModuleType,
    *,
    class_name: str | None = None,
    class_suffix: str | None = None,
) -> type | None:
    """Returns the specified class from the given module."""

    try:
        module = _import_module_if_needed(module)
    except Exception:
        return None

    if class_name is None:
        class_name = to_pascal_case(module.__name__.split(".")[-1])

        if class_suffix and not class_name.endswith(class_suffix):
            class_name += class_suffix

    class_ = getattr(module, class_name, None)

    return class_ if isclass(class_) else None


def get_classes(
    modules: list[str] | list[ModuleType],
    *,
    class_name: str | None = None,
    class_suffix: str = "",
) -> list[type]:
    """Returns a list of classes with the given suffix from the given modules."""

    classes: list[type] = []

    for module in modules:
        class_ = get_class(module, class_name=class_name, class_suffix=class_suffix)

        if class_ is not None:
            classes.append(class_)

    return classes


def get_attr(
    module: str | ModuleType,
    attr_name: str,
    default: Any = None,
) -> Any:
    """Returns the specified attribute from the given module."""

    try:
        module = _import_module_if_needed(module)
        return getattr(module, attr_name, default)
    except Exception:
        pass

    return default


def get_attrs(
    modules: list[str] | list[ModuleType],
    attr_name: str,
    default: Any = None,
) -> list[Any]:
    """Returns a list of attrs with the given name from the specified modules."""

    attrs: list[Any] = []

    for module in modules:
        attr = get_attr(module, attr_name, default)

        if attr is not None:
            attrs.append(attr)

    return attrs


def _import_module_if_needed(module: str | ModuleType) -> ModuleType:
    """Imports the module if it is a string, otherwise returns the module."""
    if isinstance(module, str):
        module = module.replace("\\", "/").replace("/", ".").replace(".py", "")
        module = importlib.import_module(module)

    return module
