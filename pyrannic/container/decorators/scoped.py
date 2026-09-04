from pyrannic.container import T


def scoped(cls: type[T]) -> type[T]:
    """Decorator to register a scoped binding in the container."""

    cls.__pyrannic_binding_type__ = "scoped"  # pyright: ignore[reportAttributeAccessIssue]

    return cls
