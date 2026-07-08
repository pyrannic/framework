from pydantic import Field

from pyrannic.config.configuration import Configuration


class Foo(Configuration):
    name: str = Field(default="Pyrannic")
    env: str = Field(default="production")
    debug: bool = Field(default=False)
    session_lifetime: int = Field(default=3600)
    cors_allowed_methods: list[str] = Field(default_factory=lambda: ["*"])
    allowed_ports: list[int] = Field(default_factory=lambda: [])
