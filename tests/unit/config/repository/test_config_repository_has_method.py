from pyrannic.contracts.config.respository import ConfigRepositoryInterface


def test_has_method(repository: ConfigRepositoryInterface):
    assert repository.has("app.name") is True
    assert repository.has("app.non_existent_key") is False


def test_with_hasattr(repository: ConfigRepositoryInterface):
    assert hasattr(repository, "app.name") is True
    assert hasattr(repository, "app.non_existent_key") is False
