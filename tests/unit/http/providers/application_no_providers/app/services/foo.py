from abc import ABC, abstractmethod

from pyrannic.ioc import Resolve


class FooServiceInterface(ABC):
    @abstractmethod
    def get_app_name(self) -> str:
        pass


class FooService(FooServiceInterface):
    def __init__(self):
        self.app_name = "FastApp"

    def get_app_name(self) -> str:
        return self.app_name


class FooService2(FooServiceInterface):
    def __init__(self):
        self.app_name = "PyrannicApp!!"

    def get_app_name(self) -> str:
        return self.app_name


class BarService:
    def __init__(self, foo: Resolve[FooServiceInterface]):
        self.foo = foo
