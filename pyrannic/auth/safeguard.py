from collections.abc import Callable
from typing import Any, cast

from fastapi import Depends, Request
from fastapi.security.base import SecurityBase

from pyrannic.auth.authenticatable import AuthenticatableInterface
from pyrannic.contracts.auth.access.authorizable import AuthorizableInterface
from pyrannic.contracts.auth.access.gate import GateInterface
from pyrannic.contracts.auth.guard import GuardInterface
from pyrannic.ioc import Resolves


def Authenticate():
    return Depends(Safeguard())


class Safeguard(SecurityBase):
    _security_model: SecurityBase | None = None

    def __init__(self) -> None:
        if self._security_model:
            self.model = self._security_model.model
            self.scheme_name = self._security_model.scheme_name
        else:
            raise RuntimeError(
                "\n\n"
                "No security model has been set. Please use Safeguard.use_security_model() to set one.\n"
                "You can do that in any ServiceProvider's register() method, e.g.:\n\n"
                "       class AppServiceProvider(ServiceProvider):\n"
                "            def register(self) -> None:\n"
                "               Safeguard.use_security_model(HTTPBearer())\n"
                "\n"
                "You can use any security model that inherits from fastapi.security.base.SecurityBase, e.g. HTTPBearer, OAuth2PasswordBearer, etc.\n"
                "If you are using a custom security model, make sure it inherits from SecurityBase and implements the __call__ method.\n"
                "\n"
                "For more information, see the FastAPI documentation on security:\n"
                "   - https://fastapi.tiangolo.com/tutorial/security/\n"
                "   - https://fastapi.tiangolo.com/advanced/security/\n"
                "\n\n"
            )

    @classmethod
    def use_security_model(cls, security_model: SecurityBase) -> None:
        cls._security_model = security_model

    @classmethod
    def get_security_model(cls) -> SecurityBase | None:
        return cls._security_model

    async def __call__(
        self,
        request: Request,
        guard: Resolves[GuardInterface[AuthenticatableInterface]],
        gate: Resolves[GateInterface],
    ) -> Any:
        # Resolve the user from the guard and set it in the gate.
        gate.set_user(cast(AuthorizableInterface | None, guard.maybe_user))

        callable = cast(Callable[..., Any], self._security_model)
        return await callable(request) if self._security_model else None
