from pyrannic.contracts.application import ApplicationInterface
from pyrannic.contracts.config.respository import ConfigRepositoryInterface
from pyrannic.facades import Config


def test_get_facade_accessor():
    assert Config.facade_accessor == "config"  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]


def test_get_facade_root(application: ApplicationInterface):
    config: ConfigRepositoryInterface = application.container.instance("config")
    assert Config._get_facade_root() == config  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]


def test_config_interface_properties(application: ApplicationInterface):
    assert Config.all() is not None
    assert Config.has("app.name") is True
