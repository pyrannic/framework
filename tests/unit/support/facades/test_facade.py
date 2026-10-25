from abc import ABC, abstractmethod
from unittest.mock import Mock

import pytest

from pyrannic.support.facades.facade import Facade, facade


class GenericInterface[T](ABC):
    @property
    @abstractmethod
    def value(self) -> T: ...

    @abstractmethod
    def echo(self, value: T, *, repeat: int = 1) -> T: ...


def test_generic_facade(monkeypatch: pytest.MonkeyPatch):
    root = Mock(spec=GenericInterface)
    root.value = "value"
    root.echo.return_value = "result"
    monkeypatch.setattr(Facade, "_get_facade_root", lambda _: root)  # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]

    @facade
    class GenericFacade(GenericInterface[str]):
        @property
        def facade_accessor(self) -> str:
            return "generic"

    assert isinstance(GenericFacade, GenericInterface)
    assert isinstance(GenericFacade, Facade)
    assert GenericFacade.facade_accessor == "generic"
    assert GenericFacade.value == "value"
    assert GenericFacade.echo("input", repeat=2) == "result"
    root.echo.assert_called_once_with("input", repeat=2)
