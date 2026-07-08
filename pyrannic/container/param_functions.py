from typing import Any, Literal

from pyrannic.container import params


def Resolves(
    abstract: str | type | None = None,
    use_cache: bool = True,
    scope: Literal["function", "request"] | None = None,
) -> Any:
    return params.Resolves(
        dependency=abstract,
        use_cache=use_cache,
        scope=scope,
    )


def Singleton(
    abstract: str | type | None = None,
    use_cache: bool = True,
    scope: Literal["function", "request"] | None = None,
) -> Any:
    return params.Singleton(
        dependency=abstract,
        use_cache=use_cache,
        scope=scope,
    )


def Scoped(
    abstract: str | type | None = None,
    use_cache: bool = True,
    scope: Literal["function", "request"] | None = None,
) -> Any:
    return params.Scoped(
        dependency=abstract,
        use_cache=use_cache,
        scope=scope,
    )
