from typing import Any, Callable

from fastapi import Depends

from .safeguard import Safeguard


def SafeguardWith(security_model: Callable[..., Any] | None = None) -> Any:
    print(f"SafeguardWith called with security_model: {Safeguard.get_security_model()}")

    return (
        Safeguard.get_security_model()
        if not security_model
        else Depends(security_model)
    )


NeedsSafeguard = Depends(SafeguardWith(), use_cache=False)
