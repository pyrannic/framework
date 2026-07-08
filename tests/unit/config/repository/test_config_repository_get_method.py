import pytest

from pyrannic.contracts.config.respository import ConfigRepositoryInterface


def test_get_method(repository: ConfigRepositoryInterface):
    assert repository.get("app.name") == "MyApp"
    assert repository.get("app.non_existent_key") is None
    assert repository.get("app.non_existent_key", "default") == "default"


def test_with_getattr(repository: ConfigRepositoryInterface):
    assert getattr(repository, "app.name") == "MyApp"
    assert getattr(repository, "app.non_existent_key", "default") == "default"
    assert getattr(repository, "non_existent_key", "default") == "default"

    with pytest.raises(AttributeError) as exc_info:
        getattr(repository, "app.non_existent_key")

    error = str(exc_info.value)
    assert "'ConfigRepository' has no attribute 'app.non_existent_key'" in error


def test_optional_string(repository: ConfigRepositoryInterface):
    assert repository.optional_string("app.name") == "MyApp"
    assert repository.optional_string("app.non_existent_key") is None
    assert repository.optional_string("app.non_existent_key", "default") == "default"


def test_string(repository: ConfigRepositoryInterface):
    assert repository.string("app.name") == "MyApp"
    assert repository.string("app.non_existent_key") == ""
    assert repository.string("app.non_existent_key", "default") == "default"


def test_optional_float(repository: ConfigRepositoryInterface):
    assert repository.optional_float("foo.float") == 3.14
    assert repository.optional_float("foo.non_existent_key") is None
    assert repository.optional_float("foo.non_existent_key", 1.23) == 1.23


def test_float(repository: ConfigRepositoryInterface):
    assert repository.float("foo.float") == 3.14
    assert repository.float("foo.non_existent_key") == 0.0
    assert repository.float("foo.non_existent_key", 1.23) == 1.23


def test_optional_list(repository: ConfigRepositoryInterface):
    assert repository.optional_list("foo.list") == [1, 2, 3]
    assert repository.optional_list("foo.non_existent_key") is None
    assert repository.optional_list("foo.non_existent_key", [4, 5, 6]) == [4, 5, 6]


def test_list(repository: ConfigRepositoryInterface):
    assert repository.list("foo.list") == [1, 2, 3]
    assert repository.list("foo.non_existent_key") == []
    assert repository.list("foo.non_existent_key", [4, 5, 6]) == [4, 5, 6]
