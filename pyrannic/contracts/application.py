from abc import ABC, abstractmethod

from fastapi import FastAPI

from pyrannic.contracts.container.container import ContainerInterface


class ApplicationInterface(ABC, FastAPI):
    @property
    @abstractmethod
    def base_path(self) -> str:
        """The base path for the Pyrannic application installation."""
        pass

    @property
    @abstractmethod
    def container(self) -> ContainerInterface:
        """The IoC container instance for the Pyrannic application."""
        pass
