from pydantic import Field

from pyrannic.config.configuration import Configuration


class FooConfig(Configuration):
    name: str = Field(default="Pyrannic")
    env: str = Field(default="production")
    debug: bool = Field(default=False)


class FooBarConfig(Configuration):
    foo: str = Field(default="bar")
    bar: str = Field(default="foo")
