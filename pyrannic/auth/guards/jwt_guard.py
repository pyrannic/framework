from typing import Any

import jwt

from pyrannic.auth.unauthorized_exception import UnauthorizedException
from pyrannic.contracts import ConfigRepositoryInterface, UserProviderInterface
from pyrannic.ioc import Resolves, scoped

from .bearer_guard import BearerGuard


@scoped
class JwtGuard(BearerGuard):
    def __init__(
        self,
        user_provider: Resolves[UserProviderInterface],
        config: Resolves[ConfigRepositoryInterface],
    ):
        super().__init__(user_provider)
        self._config = config
        self._jwks_client = None

    async def authenticate(self, token: str) -> None:
        payload = self.decode(token)

        if self.validate(token, payload):
            user = await self.provider.retrieve_by_credentials(payload)

            if user and self.provider.validate_credentials(user, token):
                self.set_user(user)

    @property
    def jwks_client(self) -> jwt.PyJWKClient:
        if self._jwks_client is None:
            jwks_url = self._config.get("auth.guards.jwt.jwks_url")

            if not jwks_url:
                raise RuntimeError(
                    "\n\n"
                    "JWKS URL is not configured for JWT guard. Please check your configuration:"
                    "\n"
                    "  - You can set it as an environment variable. For example:\n"
                    "        JWT_JWKS_URL='https://example.com/.well-known/jwks.json'\n"
                    "\n"
                    "  - Or, in your auth.py config file, you can set it like this:\n"
                    "       class AuthConfig(Configuration):\n"
                    "           guards: GuardsConfig = Field(default=GuardsConfig(\n"
                    "               jwt=JwtGuardConfig(jwks_url='https://example.com/.well-known/jwks.json')\n"
                    "           ))\n"
                    "\n\n"
                )

            self._jwks_client = jwt.PyJWKClient(jwks_url)

        return self._jwks_client

    def decode(self, token: str) -> dict[str, Any]:
        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(token)
            verify: list[str] = self._config.list(
                "auth.guards.jwt.verify",
                default=["exp", "iss", "aud", "sub", "nbf", "iat", "jti"],
            )

            payload = jwt.decode(
                token,
                signing_key,
                algorithms=self._config.list(
                    "auth.guards.jwt.algorithms",
                    default=["RS256"],
                ),
                options={
                    "verify_signature": self._config.bool(
                        "auth.guards.jwt.verify_signature", default=True
                    ),
                    "strict_aud": self._config.bool(
                        "auth.guards.jwt.strict_audience",
                        default=False,
                    ),
                    "require": self._config.list("auth.guards.jwt.require", default=[]),
                    "verify_aud": "aud" in verify,
                    "verify_exp": "exp" in verify,
                    "verify_iss": "iss" in verify,
                    "verify_sub": "sub" in verify,
                    "verify_nbf": "nbf" in verify,
                    "verify_iat": "iat" in verify,
                    "verify_jti": "jti" in verify,
                },
                audience=self._config.get("auth.guards.jwt.audience"),
                subject=self._config.optional_str("auth.guards.jwt.subject"),
                issuer=self._config.optional_str("auth.guards.jwt.issuer"),
                leeway=self._config.float("auth.guards.jwt.leeway", 0),
            )

            return payload
        except jwt.PyJWTError as e:
            raise self.unauthorized_exception(str(e)) from e

    def validate(self, token: str, payload: dict[str, Any]) -> bool:
        return True

    def unauthorized_exception(self, message: str) -> UnauthorizedException:
        # https://www.rfc-editor.org/info/rfc6750/#section-3.1
        header = {
            "realm": self._config.str("app.name"),
            "error": "invalid_token",
            "error_description": message,
        }

        return UnauthorizedException(
            message=f"JWT validation failed: {message}",
            headers={
                "WWW-Authenticate": f"{self.model.scheme.title()} "
                + ",  ".join(f'{k}="{v}"' for k, v in header.items())
            },
        )
