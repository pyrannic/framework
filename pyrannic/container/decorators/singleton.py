from pyrannic.container.container import T


def singleton(cls: type[T]) -> type[T]:
    """Decorator to register a singleton binding in the container."""

    setattr(cls, "__pyrannic_binding_type__", "singleton")

    return cls
