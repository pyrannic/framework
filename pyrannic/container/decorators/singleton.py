from pyrannic.container import T


def singleton(cls: type[T]) -> type[T]:
    """Decorator to register a singleton binding in the container."""

    cls.__pyrannic_binding_type__ = "singleton"  # pyright: ignore[reportAttributeAccessIssue]

    return cls
